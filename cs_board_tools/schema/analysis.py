"""Classes that hold query results or other useful groupings of data go here.
"""
from dataclasses import dataclass, field
from typing import Any


# Check-level
@dataclass
class SquareAnalysis:
    """Represents the SquareTypes present on the board in question and how many
    of each type there are.
    """

    # general information
    board_name: str = field(default="")
    paths: int = 0

    # overall validation info
    error_count: int = 0
    warning_count: int = 0
    issue_count: int = 0
    success_count: int = 0
    total_count: int = 0

    status: str = field(default="")
    data: Any = field(default="")
    error_messages: list[str] = field(default_factory=list)
    informational_messages: list[str] = field(default_factory=list)
    warning_messages: list[str] = field(default_factory=list)
