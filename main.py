#!/usr/bin/env python3
import sys

import argparse
import dotenv
import openai


class AI:
    def __init__(self, key: str):
        if key:
            dotenv.set_key('.env', 'API_KEY', key)
        try:
            openai.api_key = dict(dotenv.dotenv_values())['API_KEY']
            if not openai.api_key:
                raise KeyError
        except KeyError:
            print("[x] Saved OpenAI API key not found. Pass it by the -k flag.")
            raise SystemExit


    @staticmethod
    def request_text(prompt: str, temp: float) -> str:
        return openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            temperature=temp
        )["choices"][0]["text"]

    @staticmethod
    def request_image(prompt: str, n: int) -> str:
        res = "\n"
        response = openai.Image.create(
            prompt=prompt,
            n=n,
            size='1024x1024'
        )['data']

        for i, img in enumerate(response):
            res += f"{i + 1}. {img['url']}\n"

        return res


def set_flags(interact_mode: bool = False) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ais" if not interact_mode else None,
        epilog='Pass no arguments to enter interactive mode. Print exit or quit to exit from interactive mode.',
        exit_on_error=False,
    )

    parser.add_argument(
        '-t', '--temp', '--temperature',
        nargs=1,
        default=0.2,
        type=float,
        required=False,
        help="When -i flag is passed; The temperature determines how greedy the generative model is.",
        metavar='temperature',
        dest='temp',
    )

    parser.add_argument(
        '-k', '--key',
        type=str,
        required=False,
        help='Overwrite OpenAI API key in script environment variables.',
        metavar='OpenAI API key',
        dest='api_key'
    )

    parser.add_argument(
        '-i', '--generate_image',
        action='store_true',
        help='Generate image by prompt.',
        dest='img_request'
    )

    parser.add_argument(
        '-n',
        # nargs=1,
        type=int,
        required=False,
        default=1,
        help='When -i flag is passed; Specify the number of images to be generated (from 1 to 10, default 1)',
        metavar='images number',
        dest='img_number'
    )

    parser.add_argument(
        nargs='*',
        type=str,
        help="The prompt is your query.",
        metavar='prompt',
        dest='prompt',
    )
    return parser


def parse_args(parser, args):
    try:
        config = parser.parse_args(args)
    except (argparse.ArgumentError, SystemExit) as err:
        print("Command unrecognized:", err, "\nWrite -h to see usage or exit to exit")


def ai_request(config, ai: AI):
    try:
        if config.img_request:
            print("[Query | Image]", config.prompt)
            # TODO: add link shorter
            print("[AI | URL]", ai.request_image(config.prompt, config.img_number))

        else:
            if not (0. <= config.temp <= 1.):
                config.temp = 0.2
                print("The temperature only accepts floating point numbers from 0 to 1. Value 0.2 specified instead.")

            print("[Query]", config.prompt)
            print("[AI]", ai.request_text(config.prompt, config.temp))
    except openai.error.InvalidRequestError as err:
        print("[x]", err)


def main() -> None:
    parser = set_flags()

    try:
        config = parser.parse_args()
    except (argparse.ArgumentError, SystemExit) as err:
        print(f"Command unrecognized: {err}\n{parser.print_help()}")
        raise SystemExit

    config.prompt = ' '.join(config.prompt)

    # Inline mode
    if config.prompt:
        ai_request(config, AI(config.api_key))

    # Interactive mode
    else:
        print("You are in interactive mode.")
        parser = set_flags(interact_mode=True)

        while True:
            # TODO: maybe this is not the best practice, but i'll refactor it later
            args = input('# ').split()
            if '-h' in args or '--help' in args:
                parser.print_help()
                continue

            try:
                config = parser.parse_args(args)
            except (argparse.ArgumentError, SystemExit) as err:
                print("Command unrecognized:", err, "\nWrite -h to see usage or exit to exit")
                continue

            config.prompt = ' '.join(config.prompt)

            if config.prompt in ('exit', 'quit'):
                raise SystemExit
            elif not config.prompt and config.api_key:
                AI(config.api_key)
            elif not config.prompt:
                print("[x] You should write any prompt.")
            else:
                ai_request(config, AI(config.api_key))


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        sys.exit('Program exited')
