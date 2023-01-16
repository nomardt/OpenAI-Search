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
        '-p', '--prompt',
        nargs='+',
        type=str,
        required=True,
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


def main():
    config = parse_args()

    openai.api_key = "ENTER_YOUR_API" if config.api_key is None else config.api_key

    if not (0. <= config.temp <= 1.):
        config.temp = 0.2
        print("The temperature only accepts floating point numbers from 0 to 1. Value 0.2 specified instead.")

    config.prompt = ' '.join(config.prompt)

    print("[Query]", config.prompt)
    print("[AI]", ai_request(config.prompt, config.temp))


if __name__ == '__main__':
    main()
