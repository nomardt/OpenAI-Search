#!/usr/bin/env python3
import sys

import argparse
import dotenv
import openai


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ais",
        epilog='Pass no arguments to enter interactive mode (coming soon)'
    )

    parser.add_argument(
        '-t', '--temp', '--temperature',
        nargs=1,
        default=0.2,
        type=float,
        required=False,
        help="When -i flag is passed. The temperature determines how greedy the generative model is.",
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
        nargs=1,
        type=int,
        required=False,
        default=1,
        help='When -i flag is passed; Specify the number of images to be generated (from 1 to 10, default 1)',
        metavar='images number',
        dest='img_number'
    )

    parser.add_argument(
        nargs='+',
        type=str,
        help="The prompt is your query.",
        metavar='prompt',
        dest='prompt',
    )

    return parser.parse_args()


# TODO: create class
def ai_request_text(prompt: str, temp: float) -> str:
    return openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        temperature=temp
    )["choices"][0]["text"]


def ai_request_image(prompt: str, n: int) -> str:
    return openai.Image.create(
        prompt=prompt,
        n=n,
        size='1024x1024'
    )["data"][0]["url"]


def main():
    config = parse_args()

    if config.api_key:
        dotenv.set_key('.env', 'API_KEY', config.api_key)

    openai.api_key = dotenv.dotenv_values('.env')['API_KEY']

    config.prompt = ' '.join(config.prompt)

    if config.img_request:
        print("[Query | Image]", config.prompt)
        # TODO: add link shorter
        print("[AI | URL]", ai_request_image(config.prompt, config.img_number))

    else:
        if not (0. <= config.temp <= 1.):
            config.temp = 0.2
            print("The temperature only accepts floating point numbers from 0 to 1. Value 0.2 specified instead.")

        print("[Query]", config.prompt)
        print("[AI]", ai_request_text(config.prompt, config.temp))


if __name__ == '__main__':
    main()
