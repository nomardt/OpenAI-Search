import sys
from datetime import datetime
from functools import partialmethod

from loguru import logger as log


def configure_logging(debug: bool = False):
    """
    1. DEBUG LOGGER:
     - level: DEBUG
     - to `sys.stdout` and to file 'debug.log' if `--debug` passed
     - default format
    2. INFO
     - level: INFO
     - to sys.stdout
     - format: only text and colorized with prefix
     - without traceback when error
    3. AI-QUERIES:
     - level: spec handler (sub-INFO)
     - to sys.stdout (and to file 'story.log' if --save-to-file passed)
     - format: only text and colorized with prefix
    """
    log.remove()

    log.level('PROMPT', no=25, color='<bold>', icon='>')
    log.__class__.prompt = partialmethod(log.__class__.log, 'PROMPT')

    log.level('RESPONSE', no=25)
    log.__class__.response = partialmethod(log.__class__.log, 'RESPONSE')

    log.add(
        sink=f'logs/history/ais_history_{datetime.now().isoformat(timespec="seconds").replace(":", "-")}.log',
        format='> <bold>{message}</bold>',
        filter=lambda record: record['level'].name == 'PROMPT',
        colorize=True,
        serialize=False,
        backtrace=False,
        diagnose=False,
        enqueue=True,
        catch=False,
        delay=True,
    )

    log.add(
        sink=f'logs/history/ais_history_{datetime.now().isoformat(timespec="seconds").replace(":", "-")}.log',
        format='{message}',
        filter=lambda record: record['level'].name == 'RESPONSE',
        colorize=True,
        serialize=False,
        backtrace=False,
        diagnose=False,
        enqueue=True,
        catch=False,
        delay=True,
    )

    if debug:
        log.add(
            sink='logs/debug.log',
            level='DEBUG',
            colorize=False,
            serialize=False,
            diagnose=True,
            backtrace=True,
            enqueue=True,
            catch=True,
            rotation='10 MB',
            retention=3,
            compression='zip',
            delay=True,
        )

        log.add(
            sink=sys.stdout,
            level='DEBUG',
            colorize=True,
            serialize=False,
            backtrace=True,
            diagnose=True,
            enqueue=False,
            catch=True,
        )
    else:
        log.add(
            sink=sys.stdout,
            level='INFO',
            format='<green>[{time:HH:mm:ss}]</green> {message}',
            filter=lambda record: record['level'].name not in ('PROMPT', 'RESPONSE'),
            colorize=True,
            serialize=False,
            backtrace=False,
            diagnose=False,
            enqueue=False,
            catch=True,
        )

        log.add(
            sink=sys.stdout,
            format="<italic>{message}</italic>",
            filter=lambda record: record['level'].name == 'RESPONSE',
            colorize=True,
            serialize=False,
            backtrace=False,
            diagnose=False,
            enqueue=False,
            catch=False,
        )

    log.debug("Logging set up in debug mode.")


if __name__ == '__main__':
    configure_logging()
