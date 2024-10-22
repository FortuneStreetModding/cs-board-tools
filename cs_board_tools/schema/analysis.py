"""Classes that hold query results or other useful groupings of data go here.
"""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SquareAnalysis:
    """Represents the SquareTypes present on the board in question and how many
    of each type there are. This is a WIP class related to a future feature.
    """

    # general information
    board_name: str = field(default="")
