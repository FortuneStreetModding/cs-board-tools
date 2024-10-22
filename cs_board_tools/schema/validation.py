"""Class definitions relating to validation checks.
"""
from dataclasses import dataclass, field
from typing import Any


# Check-level
@dataclass
class CheckResult:
    """A dataclass representing results from a single validation
    check on a single board.

    This object is normally attached to a ValidationResult object,
    to live alongside other result sets from other checks, representing
    a single board. This object contains a status, which will be either
    ERROR, OK, WARNING, or SKIPPED; data, a field designed to allow any
    sort of data to be passed back; and three lists of strings to hold
    error, informational, and warning messages, respectively.
    """
    data: Any = field(default="")
    status: str = field(default="SKIPPED")
    error_messages: list[str] = field(default_factory=list)
    informational_messages: list[str] = field(default_factory=list)
    warning_messages: list[str] = field(default_factory=list)


# File-level
@dataclass
class ValidationResult:
    """A dataclass representing results from multiple validation checks
    on a single board.

    This object is sometimes attached to a ValidationResultBundle object,
    in the case that the task is returning information about checks for
    multiple boards. If we are checking only one board, though, we will
    return this result alone. This object contains the board name, the
    number of max paths, error, warning, success and other check counts,
    full CheckResult objects representing the results of each test
    performed, and three lists containing an aggregate of all the checks'
    errors, warnings, or informational messages.
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

    # results for specific checks
    board_configuration: CheckResult = field(default_factory=CheckResult)
    consistency: CheckResult = field(default_factory=CheckResult)
    icon: CheckResult = field(default_factory=CheckResult)
    max_paths: CheckResult = field(default_factory=CheckResult)
    music_download: CheckResult = field(default_factory=CheckResult)
    naming: CheckResult = field(default_factory=CheckResult)
    screenshots: CheckResult = field(default_factory=CheckResult)
    venture: CheckResult = field(default_factory=CheckResult)
    yaml: CheckResult = field(default_factory=CheckResult)

    # things that are lists
    error_messages: list[str] = field(default_factory=list)
    informational_messages: list[str] = field(default_factory=list)
    warning_messages: list[str] = field(default_factory=list)


# Bundle-level
@dataclass
class ValidationResultBundle:
    """A dataclass representing results from validation checks performed
    against multiple boards.

    This object contains error, warning, success, issue (error + warning),
    and total counts, alongside lists for errors, warnings, and informational
    messages across all boards tested. It also contains an attribute called
    boards, which is a list of ValidationResult objects, representing
    validation check results for each board.
    """
    error_count: int = 0
    warning_count: int = 0
    issue_count: int = 0
    success_count: int = 0
    total_count: int = 0
    error_messages: list[str] = field(default_factory=list)
    warning_messages: list[str] = field(default_factory=list)
    informational_messages: list[str] = field(default_factory=list)
    boards: list[ValidationResult] = field(default_factory=list)
