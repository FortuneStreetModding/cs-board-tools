"""The Errors module handles counts and message lists for errors,
warnings, and even informational reasons.
"""

from enum import Enum

all_errors = []
all_fixes = []
all_warnings = []
all_informational = []
error_count = 0
fixed_count = 0
success_count = 0
warning_count = 0


class IssueType(Enum):
    """This enum is used with the get_count and get_messages functions
    to tell the function which count or list of messages to get.
    """
    ERRORS = 1
    FIXED = 2
    SUCCESS = 3
    WARNINGS = 4


def process_log_messages(
    errors: list[str] = [],
    messages: list[str] = [],
    warnings: list[str] = [],
    job_was_successful: bool = False
):
    """
    This function is not just used to process log messages. It also
    tallies things like which jobs were sucessful and which were
    errored. The other commands in this file can be used to

    :param errors: A list of errors, as collected by the calling
        process.
    :type errors: list[str]

    :param messages: A list of informational messages, as collected
        by the calling process.
    :type messages: list[str]

    :param warnings: A list of warning messages, as collected by
        the calling process.
    :type warnings: list[str]

    :param job_was_successful: The existance of the messages passed
        into the other parameters normally help classify the state
        of the job that sent them. For example, if errors are present,
        it means the job has reached an error state. However, if
        you set job_was_successful to True, the job will be counted
        as a success in metrics even if errors are present. As you
        might expect, this defaults to False.
    :type job_was_successful: bool
    """

    global all_errors
    global all_informational
    global all_warnings
    global error_count
    global success_count
    global warning_count

    if len(errors) > 0:
        error_count += len(errors)
        all_errors += errors

    if len(messages) > 0:
        all_informational += messages

    if len(warnings) > 0:
        warning_count += len(warnings)
        all_warnings += warnings

    if job_was_successful:
        success_count += 1
    else:
        if len(errors) == 0 and len(warnings) == 0:
            success_count += 1


def get_count(t: IssueType) -> int:
    """
    Returns the number of checks of the type specified by parameter t.

    :param t: t is of type IssueType, and it represents the type of
        count to get. Possible options are IssueType.ERRORS,
        IssueType.FIXED, IssueType.WARNINGS, and IssueType.SUCCESS.
    :type t: cs_board_tools.errors.IssueType

    :return: A bundle containing the overall results, as well as a
        list containing objects that represent each of the individual
        results.
    :rtype: int
    """
    match (t):
        case IssueType.ERRORS:
            return error_count
        case IssueType.FIXED:
            return fixed_count
        case IssueType.WARNINGS:
            return warning_count
        case IssueType.SUCCESS:
            return success_count


def get_text(t: IssueType) -> list[str]:
    """
    Works similarly to get_count, but instead returns the messages of
    the type specified by parameter t.

    :param t: t is of type IssueType, and it represents the type of
        count to get. Possible options are IssueType.ERRORS,
        IssueType.FIXED, IssueType.WARNINGS, and IssueType.SUCCESS.
    :type t: cs_board_tools.errors.IssueType

    :return: A bundle containing the overall results, as well as a
        list containing objects that represent each of the individual
        results.
    :rtype: int
    """
    match (t):
        case IssueType.ERRORS:
            return all_errors.copy()
        case IssueType.FIXED:
            return all_fixes.copy()
        case IssueType.WARNINGS:
            return all_warnings.copy()
        case IssueType.SUCCESS:
            return all_informational.copy()


def reset_errors_and_warnings():
    """
    When called, it clears all counts and message lists.
    """
    global all_errors
    global all_fixes
    global all_informational
    global all_warnings
    global error_count
    global fixed_count
    global success_count
    global warning_count
    all_errors.clear()
    all_fixes.clear()
    all_informational.clear()
    all_warnings.clear()
    error_count = 0
    fixed_count = 0
    success_count = 0
    warning_count = 0
