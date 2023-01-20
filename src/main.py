#!/usr/bin/env python3
import sys
from argparse import Namespace

from loguru import logger as log

from models import ArgsNamespace, AI


@log.catch()
def main() -> None:
    config = ArgsNamespace()

    # Inline mode
    if config.prompt:
        AI(config).request()

    # Interactive mode
    else:
        log.debug("Interactive mode enabled.")

        while True:
            config = ArgsNamespace(source=input('# '), interactive_mode=True)
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


if __name__ == '__main__':
    log.remove()
    log.add(
        sys.stdout,
        level='DEBUG',
        colorize=True,
        diagnose=True, # TODO
        enqueue=True,
    )

    try:
        main()
        
    except (KeyboardInterrupt, SystemExit) as err:
        log.error(f"Exited with code: {err}")

    except Exception as err:
        log.opt(exception=True).error(err)
