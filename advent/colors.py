from typing import Any


def red(s: Any) -> str:
    return f"\033[91m\033[1m{s}\033[0m"


def orange(s: Any) -> str:
    return f"\033[38;5;208m\033[1m{s}\033[0m"


def yellow(s: Any) -> str:
    return f"\033[93m\033[1m{s}\033[0m"


def green(s: Any) -> str:
    return f"\033[92m\033[1m{s}\033[0m"


def blue(s: Any) -> str:
    return f"\033[94m\033[1m{s}\033[0m"


def indigo(s: Any) -> str:
    return f"\033[38;5;21m\033[1m{s}\033[0m"


def violet(s: Any) -> str:
    return f"\033[95m\033[1m{s}\033[0m"


def gray(s: Any) -> str:
    return f"\033[90m{s}\033[0m"
