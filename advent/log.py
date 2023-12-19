import logging
import sys


def gray(s: str) -> str:
    return f"\033[90m{s}\033[0m"


def green(s: str) -> str:
    return f"\033[92m\033[1m{s}\033[0m"


def yellow(s: str) -> str:
    return f"\033[93m\033[1m{s}\033[0m"


def red(s: str) -> str:
    return f"\033[91m\033[1m{s}\033[0m"


# Very slightly adapted from https://stackoverflow.com/a/56944256/15625637
class ColoredLogFormatter(logging.Formatter):
    BLUE = "\x1b[34;21m"
    GRAY = "\x1b[38;21m"
    YELLOW = "\x1b[33;21m"
    RED = "\x1b[31;21m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"
    FMT = "[%(asctime)s][%(levelname)s] %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: BLUE + FMT + RESET,
        logging.INFO: GRAY + FMT + RESET,
        logging.WARNING: YELLOW + FMT + RESET,
        logging.ERROR: RED + FMT + RESET,
        logging.CRITICAL: BOLD_RED + FMT + RESET,
    }

    def format(self, record: logging.LogRecord) -> str:
        formatter = logging.Formatter(self.FMT)
        if sys.stderr.isatty():
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
