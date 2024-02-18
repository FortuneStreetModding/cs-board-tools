"""The functions that live here aren't tests, but rather the
ones that build and return the CheckResults object.
"""
from cs_board_tools.schema.validation import CheckResult
from cs_board_tools.errors import process_log_messages
from typing import Any


def build_results_object(
    errors: list[str] = [],
    messages: list[str] = [],
    warnings: list[str] = [],
    data: Any = None,
    success: bool = False,
    skip: bool = False
) -> CheckResult:
    """
    This function builds a Results object and returns it
    fully populated with the details of the most recent check.

    :param errors: A list of error messages.
    :type errors: list[str]

    :param messages: A list of informational messages.
    :type messages: list[str]

    :param warnings: A list of warning messages.
    :type warnings: list[str]

    :param data: This parameter could hold any meaningful data.
        It will be returned embedded in the CheckResult object.
    :type data: Any

    :param success: If set to True, "OK" will be set as the check status.
    :type success: bool

    :param skip: If set to True, "SKIPPED" will be set as the check status.
    :type skip: bool

    :return: A CheckResult object containing the check status as
        well as any messages and additional data.
    :rtype: CheckResult
    """
    results = CheckResult()
    results.error_messages = errors.copy()
    results.informational_messages = messages.copy()
    results.warning_messages = warnings.copy()

    if skip:
        results.status = "SKIPPED"
    elif success:
        results.status = "OK"
    elif errors:
        results.status = "ERROR"
    elif warnings:
        results.status = "WARNING"
    else:
        results.status = "OK"

    results.data = data

    process_log_messages(
        errors=errors.copy(),
        messages=messages.copy(),
        warnings=warnings.copy(),
        job_was_successful=results.status
    )

    return results
