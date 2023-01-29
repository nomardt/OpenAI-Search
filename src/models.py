import argparse
from typing import Sequence

import openai
import dotenv
from loguru import logger as log


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

        else:
            namespace.prompt = ' '.join(namespace.prompt).lstrip()
            namespace.temp = namespace.temp[0]

            if not (0. <= namespace.temp <= 1.):
                namespace.temp = 0.2
                log.warning(
                    "The temperature only accepts floating point numbers from 0 to 1. Value 0.2 specified instead."
                )

            return namespace
