import argparse
import sys
from typing import Sequence

import openai
import dotenv
from loguru import logger as log
from pynput import keyboard


class AI:
    """
    This class initializes the API key when an instance is created.
    Using class methods, you can send appropriate requests to OpanAI
    """

    def __init__(self, config: argparse.Namespace):
        self.config = config

        if self.config.api_key:
            dotenv.set_key('.env', 'API_KEY', self.config.api_key)
            log.info("API key saved.")

        try:
            openai.api_key = dict(dotenv.dotenv_values())['API_KEY']
            if not openai.api_key:
                raise KeyError

        except KeyError:
            log.critical("[x] Saved OpenAI API key not found. Pass it by the -k flag.")
            raise SystemExit

    def _request_text(self) -> None:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=self.config.prompt,
            max_tokens=1024,
            temperature=self.config.temp
        )["choices"][0]["text"].strip()

        log.response(response)

    def _request_image(self) -> None:
        res = "\n"
        response = openai.Image.create(
            prompt=self.config.prompt,
            n=self.config.img_number,
            size='1024x1024'
        )['data']

        for i, img in enumerate(response):
            res += f"{i + 1}. {img['url']}\n"

        log.response(res)

    def request(self) -> None:
        try:
            if self.config.img_request:
                self._request_image()
            else:
                self._request_text()

        except openai.error.InvalidRequestError as err:
            log.error("[x]", err)


class ArgsNamespace:
    def __new__(cls,
                source: Sequence[str] | str | None = None,
                interactive_mode: bool = False) -> argparse.Namespace:
        """
        Return namespace of arguments.
        :param source: A string with arguments or a sequence of arguments.
        If None, the value will be determined from `sys.argv`.
        :param interactive_mode:
        :return: Namespace of arguments or `False` if help message requested.
        """

        cls = argparse.ArgumentParser(
            prog='ais' if not interactive_mode else '',
            epilog='Pass no arguments to enter interactive mode. Print exit or quit to end the interactive session.',
            exit_on_error=True,
        )

        cls.add_argument(
            '-t', '--temp', '--temperature',
            nargs=1,
            default=[0.2, ],
            type=float,
            required=False,
            help='When no flag is passed; The temperature determines how greedy the generative model is.',
            metavar='temperature',
            dest='temp',
        )

        cls.add_argument(
            '-k', '--key',
            type=str,
            required=False,
            help='Overwrite OpenAI API key in .env.',
            metavar='OpenAI API key',
            dest='api_key'
        )

        cls.add_argument(
            '-i', '--generate_image',
            action='store_true',
            help='Generate image by prompt.',
            dest='img_request'
        )

        cls.add_argument(
            '-n',
            type=int,
            required=False,
            default=1,
            help='When -i flag is passed; Specify the number of images to be generated (from 1 to 10, default 1)',
            metavar='images number',
            dest='img_number'
        )

        cls.add_argument(
            nargs='*',
            type=str,
            help='The prompt is your query.',
            metavar='prompt',
            dest='prompt',
        )

        cls.add_argument(
            '-d', '--debug',
            action='store_true',
            help='Enable debugging mode.',
            dest='debug'
        )

        if isinstance(source, str):
            source = source.split()

        try:
            log.debug(f'Parsing arguments from {source}')
            namespace = cls.parse_args(source)

        except SystemExit as err:
            log.error(
                f"Command unrecognized. Status code: {err}\n"
                f"{cls.format_usage()}"
                f"Try '{'' if interactive_mode else 'ais '}-h' for more information."
            )
            return argparse.Namespace()

        else:
            namespace.prompt = ' '.join(namespace.prompt).lstrip()
            namespace.temp = namespace.temp[0]

            if not (0. <= namespace.temp <= 1.):
                namespace.temp = 0.2
                log.warning(
                    "The temperature only accepts floating point numbers from 0 to 1. Value 0.2 specified instead."
                )

            return namespace


class _CustomCounter:
    """
    The class allows you to cyclically and randomly increment and decrement the list index.
    Spinning up is decrementing value and spinning down is incrementing.
    :param vol: Volume of counter.
    """
    def __init__(self, vol: int):
        if vol < 0:
            raise ValueError("Volume must be a natural number")

        self.vol = vol
        self.val = -1

    def __int__(self):
        return self.val

    def _spin_up(self):
        if self.val < 0 and abs(self.val) >= self.vol:
            self.val = 0
        else:
            self.val -= 1

    def _spin_down(self):
        self.val += 1
        if self.val >= self.vol:
            self.val *= -1

    def spin(self, key):
        if key == keyboard.Key.up:
            self._spin_up()

        elif key == keyboard.Key.down:
            self._spin_down()


class InputListener:
    """
    The class extends the capabilities of the input function.
    The listen method listens for the keys pressed by the user and returns the result.
    """
    def __init__(self, previous_inputs: list[str] | None = None):
        self._previous_inputs = previous_inputs
        if self._previous_inputs is not None:
            self._previous_inputs.append('')
            self._result: str = ''
            self._i = _CustomCounter(len(self._previous_inputs))

    def listen(self) -> str:
        if self._previous_inputs is None:
            return input("> ")

        def _on_press(key) -> None:
            if key in (keyboard.Key.up, keyboard.Key.down):
                self._i.spin(key)
                self._result = self._previous_inputs[int(self._i)]
                sys.stdout.write(f'\r> {self._result}')
                sys.stdout.flush()

            elif key == keyboard.Key.enter:
                listener.stop()

            # If backspace was pressed: delete last symbol, clear output and print result
            elif key == keyboard.Key.backspace and self._result:
                self._result = self._result[:-1]
                sys.stdout.write(f'\r> {self._result}')
                sys.stdout.flush()

            # If a symbol key was pressed: add it to result
            elif not isinstance(key, keyboard.Key):
                self._result += str(key).strip("'")

        print("> ", end='', flush=True)

        with keyboard.Listener(on_press=_on_press) as listener:
            listener.join()

        return self._result
