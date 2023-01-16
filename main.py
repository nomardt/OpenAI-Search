#!/usr/bin/env python3
import sys

import argparse
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
        help="The temperature determines how greedy the generative model is.",
        metavar='temperature',
        dest='temp',
    )

    parser.add_argument(
        '-k', '--key',
        type=str,
        required=False,
        help='Write or overwrite OpenAI API key in script environment variables.',
        metavar='OpenAI API key',
        dest='api_key'
    )

    parser.add_argument(
        '-i', '--generate_image',
        type=str,
        required=False,
        help='Change the mode to image generation.',
        metavar='generate_image',
        dest='generate_image'
    )

    parser.add_argument(
        '-n',
        type=int,
        required=False,
        help='WORKS ONLY WITH -i; Specify the number of images to be generated',
        metavar='n',
        dest='n'
    )

    parser.add_argument(
        nargs='+',
        type=str,
        help="The prompt is your query.",
        metavar='prompt',
        dest='prompt',
    )

    return parser.parse_args()


def ai_request(prompt: str, temp: float) -> str:
    return openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        temperature=temp
    )["choices"][0]["text"]

def ai_request_image(prompt: str, n: int) -> str:
    return openai.Completion.create(
        prompt=prompt,
        n=n,
        size='1024x1024'
    )["data"][0]["url"]

def main():
    config = parse_args()

    if generate_image:
        if not n:
            n = 1

        print(ai_request_image(generate_image, n))

    else:
        if not (0. <= config.temp <= 1.):
            config.temp = 0.2
            print("The temperature only accepts floating point numbers from 0 to 1. Value 0.2 specified instead.")

        config.prompt = ' '.join(config.prompt)

        print("[Query]", config.prompt)
        print("[AI]", ai_request(config.prompt, config.temp))


if __name__ == '__main__':
    main()
