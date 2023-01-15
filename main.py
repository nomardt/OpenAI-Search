#!/usr/bin/env python3
import sys
import openai


def request(prompt, temp):
    return openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        temperature=temp
    )


def main():
    openai.api_key = "ENTER_YOUR_API"

    # Getting the prompt
    try:
        prompt = sys.argv[1]

    except IndexError:
        print('Usage: ais "Your Search Query" [OPTIONAL: temperature]')

    # Getting the amount of randomness
    try:
        temp = float(sys.argv[2])

        if temp > 1 or temp < 0:
            print("The amount of randomness can only be between values 0 and 1!")
            raise TypeError

    except (TypeError, IndexError, ValueError):
        print("Please enter a value between 0 and 1 next time. Value 0.2 specified instead.")
        temp = 0.2

    response = request(prompt, temp)
    print(response["choices"][0]["text"])


if __name__ == '__main__':
    main()
