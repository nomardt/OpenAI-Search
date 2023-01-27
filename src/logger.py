import sys

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

    log.add(
        sink=sys.stdout,
        level='INFO',
        format='<green>{time:HH:mm:ss}</green> {message}',
        colorize=True,
        serialize=False,
        backtrace=False,
        diagnose=False,
        enqueue=True,
        catch=True,
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
            enqueue=True,
            catch=True,
        )

    log.debug("Logging set up in debug mode.")
