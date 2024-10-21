"""These functions involve the filesystem -- functions like
check_for_screenshots() live here.
"""
from cs_board_tools.schema.bundle import Bundle
from cs_board_tools.schema.validation import CheckResult
from cs_board_tools.validation.results import build_results_object

original_backgrounds = [
    "bg001","bg002","bg003","bg004","bg005","bg006","bg007","bg008",
    "bg009","bg101","bg102","bg103","bg104","bg105","bg106","bg107",
    "bg108","bg109","bg901"
]

frbs_without_webps_error = (
    "Board file {filename} does not have a corresponding .webp screenshot."
)

no_icon_error = (
    "This board uses a custom background, but no mapIcon is defined in the "
    ".yaml board descriptor."
)

no_icon_warning = (
    "The .yaml board descriptor file does not define a mapIcon. This is will work "
    "when using an original background, but board authors are encouraged to create a "
    "custom mapIcon before uploading to the repository."
)

incorrect_icon_error = (
    "The mapIcon referenced by the .yaml board descriptor file could not be found."
)

def check_icon(bundle: Bundle, skip: bool, skip_warnings: bool = False) -> CheckResult:
    """
    Checks to see if the icon referenced in the board descriptor
    actually exists.

    :param bundle: A Bundle object representing a board.
    :type bundle: Bundle

    :param skip: If set to True, the check will be skipped, but a
    valid resultobject with no messages and SKIPPED as its
    status will still be returned.
    :type skip: bool

    :param skip_warnings: If set, skips tests resulting in
    "Warning" messages.
    :type skip_warnings: bool, optional

    :return: A CheckResult object containing the check status as
    well as any messages and additional data.
    :rtype: CheckResult
    """
    if skip:
        return build_results_object(skip=True)

    error_messages = []
    informational_messages = []
    warning_messages = []

    icon = bundle.icon
    if bundle.background not in original_backgrounds:
        if not icon:
            error_messages.append(no_icon_error)
    else:
        if not icon and not skip_warnings:
            warning_messages.append(no_icon_warning)

    if icon and f"{icon}.png" not in bundle.filenames.png:
        error_messages.append(incorrect_icon_error)

    results = build_results_object(
        errors=error_messages,
        messages=informational_messages,
        warnings=warning_messages
    )

    error_messages.clear()
    informational_messages.clear()
    warning_messages.clear()

    return results



def check_for_screenshots(bundle: Bundle, skip: bool, skip_warnings: bool = False) -> CheckResult:
    """
    Checks to see if all present .frb files have
    associated .webp screenshot files.

    :param bundle: A Bundle object representing a board.
    :type bundle: Bundle

    :param skip: If set to True, the check will be skipped, but a
    valid resultobject with no messages and SKIPPED as its
    status will still be returned.
    :type skip: bool

    :param skip_warnings: If set, skips tests resulting in
    "Warning" messages.
    :type skip_warnings: bool, optional

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
