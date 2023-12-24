"""Naming convention checks live here.
"""
from cs_board_tools.validation.results import build_results_object

whitespace_error = (
    "There is a whitespace character in the filename: {filename}."
)


def check_naming_convention(filename, skip):
    """
    Checks to see if files are named appropriately.

    :param filename: A string filename.
    :type filename: str

    :param skip: If set to True, the check will be skipped, but a
        valid resultobject with no messages and SKIPPED as its
        status will still be returned.
    :type skip: bool

    :return: A CheckResult object containing the check status as
        well as any messages and additional data.
    :rtype: CheckResult
    """
    if skip:
        return build_results_object(skip=True)

    error_messages = []
    informational_messages = []
    warning_messages = []

    if " " in filename:
        error_messages.append(whitespace_error)

    results = build_results_object(
        errors=error_messages,
        messages=informational_messages,
        warnings=warning_messages
    )

    error_messages.clear()
    informational_messages.clear()
    warning_messages.clear()

    return results
