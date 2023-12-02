import argparse
import logging
import pathlib
from typing import Type

import aocd

from advent.base import BaseSolver, Result, Solution
from advent.log import ColoredLogFormatter, green
