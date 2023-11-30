from typing import Iterator


def lines(s: str) -> Iterator[str]:
    for line in s.splitlines():
        yield line


def ints(line: str) -> Iterator[int]:
    for i in line.split():
        yield int(i)


def tokens(line: str, sep: str = " ") -> Iterator[str]:
    for s in line.split(sep):
        yield s


def all_ints(s: str) -> Iterator[int]:
    for line in lines(s):
        yield from ints(line)


def all_tokens(s: str) -> Iterator[str]:
    for line in lines(s):
        yield from tokens(line)
