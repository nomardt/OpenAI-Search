#!/usr/bin/env python3
import sys
from argparse import Namespace

from loguru import logger as log

from logger import configure_logging
from models import ArgsNamespace, AI


def interactive_loop_session(config: Namespace) -> None:
    log.info("Interactive mode enabled.")

    while True:
        user_input = input('Enter your prompt:\n> ')
        log.prompt(user_input)

        config = ArgsNamespace(source=user_input, interactive_mode=True)
        log.debug(f"Got {config = } for interactive mode")

        if config is None:
            continue

        elif config.prompt in ('exit', 'quit'):
            raise SystemExit

        elif not config.prompt and config.api_key:
            AI(config)

        elif not config.prompt:
            log.critical("[x] You should write any prompt.")

        else:
            AI(config).request()


@log.catch()
def main() -> None:
    config = ArgsNamespace()

    if config:

        if config.prompt:
            log.prompt(config.prompt)
            AI(config).request()

        else:
            interactive_loop_session(config)


if __name__ == '__main__':
    configure_logging('-d' in sys.argv or '--debug' in sys.argv)

    try:
        main()
        
    except (KeyboardInterrupt, SystemExit):
        log.error("Process finished.")

    except Exception as err:
        log.opt(exception=True).error(err)
