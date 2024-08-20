# -*- coding: utf-8 -*-
"""Generic classes to support queries."""

from logging import getLogger

LOGGER = getLogger(__name__)


class Color:  # pylint: disable=R0903,R0902
    """Choose color to print messages."""

    def __init__(self) -> None:
        """Class constructor."""
        self.no_color = '\033[0m'
        self.blue = '\033[94m'
        self.violet = '\033[95m'
        self.green = '\033[92m'
        self.red = '\033[91m'
        self.yellow = '\033[93m'
        self.beige = '\033[36m'
        self.black = '\033[30m'
        self.white = '\033[37m'
        self.pink = '\033[31m'
        self.cyan = '\033[96m'
        self.grey = '\033[90m'
        self.bold = '\033[1m'
        self.underline = '\033[4m'
        self.strikethrough = '\033[9m'
