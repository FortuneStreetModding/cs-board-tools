"""These functions involve the filesystem -- functions like
check_for_screenshots() live here.
"""
from cs_board_tools.schema.bundle import Bundle
from cs_board_tools.schema.validation import CheckResult
from cs_board_tools.validation.results import build_results_object


frbs_without_webps_error = (
    "Board file {filename} does not have a corresponding .webp screenshot."
)


def check_for_screenshots(bundle: Bundle, skip: bool) -> CheckResult:
    """
    Checks to see if all present .frb files have
    associated .webp screenshot files.

    :param bundle: A Bundle object representing a board.
    :type bundle: Bundle

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

    frbs = bundle.filenames.frb
    webps = bundle.screenshots

    if webps is not None:
        if len(webps) != 0:
            frbs_with_screenshots = []
            frbs_no_suffix = [f.replace('.frb', '') for f in frbs]

            for f in frbs_no_suffix:
                for w in webps:
                    if f in w:
                        frbs_with_screenshots.append(f"{f}.frb")

            for f in frbs:
                if f not in frbs_with_screenshots:
                    error_messages.append(
                        frbs_without_webps_error.format(filename=f)
                    )
        else:
            error_messages.append("No screenshots were found.")
    else:
        error_messages.append("No screenshots were found.")

    results = build_results_object(
        errors=error_messages,
        messages=informational_messages,
        warnings=warning_messages
    )

    error_messages.clear()
    informational_messages.clear()
    warning_messages.clear()

    return results
