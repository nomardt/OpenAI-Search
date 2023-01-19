#!/usr/bin/env python3
import sys

from loguru import logger as log

from models import ArgsNamespace, AI


def main() -> None:
    config = ArgsNamespace()

    # Inline mode
    if config.prompt:
        AI(config.api_key).request()

    # Interactive mode
    else:
        print("You are in interactive mode.")

        while True:
            config = ArgsNamespace(source=input('# '), interactive_mode=True)

            if config.prompt in ('exit', 'quit'):
                raise SystemExit
                
            elif not config.prompt and config.api_key:
                AI(config)
                
            elif not config.prompt:
                print("[x] You should write any prompt.")
                
            else:
                AI(config).request()


if __name__ == '__main__':
    try:
        main()
        
    except (KeyboardInterrupt, SystemExit):
        sys.exit('Program stopped.')
