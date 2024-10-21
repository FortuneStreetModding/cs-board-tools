"""Naming convention checks live here.
"""
from cs_board_tools.validation.results import build_results_object
from cs_board_tools.schema.bundle import Bundle

capitalization_mismatch_error = (
    "The file referenced in the descriptor, {filename}, exists, but "
    "the capitalization of the filenames is mismatched. The name of the "
    "file on disk is {filename_on_disk}."
)

file_not_exist_error = (
    "The file referenced in the descriptor, {filename}, does not exist."
)

whitespace_error = (
    "There is a whitespace character in the filename: {filename}."
)


def filename_capitalization_matches(
        filename_on_disk:
        str, filename_reference: str
    ) -> bool:
    """
    Checks to see if the filename found on disk matches the
    capitalization found in the descriptor.

    :param filename_on_disk: The filename that actually exists, in string form.
    :type filename_on_disk: str

    :param filename_reference: The filename _reference_. Most likely, this will
        be the filename as seen in the descriptor.
    :type filename_reference: str

    :return: True if the files' capitalization matches, False if it doesn't.
    :rtype: bool
    """
    return (filename_on_disk == filename_reference)


def filename_contains_spaces(filename: str) -> bool:
    """
    Checks to see if the filename contains spaces.

    :param filename: A string filename.
    :type filename: str

    :return: True if the file contains spaces, False if it doesn't.
    :rtype: bool
    """
    return (" " in filename)


def file_exists(yaml_filename: str, filenames_of_same_type: list[str]) -> bool:
    """
    Checks to see if file referenced in the descriptor
    actually exists on disk.

    :param yaml_filename: The filename as listed in the descriptor.
    :type yaml_filename: str

    :param filenames_of_same_type: The list of files of that type that
        were actually found on disk.
    :type filenames_of_same_type: list[str]

    :return: True if the file exists, False if it doesn't.
    :rtype: bool
    """
    upper_filenames = []

    # rsplit is being used here to remove the filename's extension
    for f in filenames_of_same_type:
        upper_filenames.append(f.rsplit('.', 1)[0].upper())

    return (yaml_filename.upper() in upper_filenames)
    # True = filename is in the file list, whether case matches or not
    # False = the file just isn't there at all.


def check_naming_convention(bundle: Bundle, skip: bool = False, skip_warnings: bool = False):
    """
    Checks to see if files are named appropriately.

    :param bundle: The Board Bundle.
    :type bundle: cs_board_tools.schema.bundle.Bundle

    :param skip: If set to True, the check will be skipped, but a
    valid result object with no messages and SKIPPED as its
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

    all_filenames = []

    all_filenames.extend(bundle.filenames.brstm)
    all_filenames.extend(bundle.filenames.cmpres)
    all_filenames.extend(bundle.filenames.frb)
    all_filenames.extend(bundle.filenames.other)
    all_filenames.extend(bundle.filenames.png)
    all_filenames.extend(bundle.filenames.webp)
    all_filenames.extend(bundle.filenames.yaml)

    for frb in bundle.descriptor.frbs:
        if not file_exists(frb, all_filenames):
            error_messages.append(
                file_not_exist_error.format(filename=frb)
            )

        for file in bundle.filenames.frb:
            frb_without_extension = file.rsplit('.', 1)[0]
            extension = file.rsplit('.', 1)[1]

            # case-insensitive matching
            if frb.lower() != frb_without_extension.lower():
                continue

            # case-sensitive matching
            if frb != frb_without_extension:
                error_messages.append(
                    capitalization_mismatch_error.format(
                        filename=f"{frb}.{extension}",
                        filename_on_disk=f"{file}"
                    )
                )

    for file in all_filenames:
        f = file
        if "/" in file:
            f = file.rsplit("/", 1)[1]
        if filename_contains_spaces(f):
            error_messages.append(
                whitespace_error.format(filename=f)
            )

    results = build_results_object(
        errors=error_messages,
        messages=informational_messages,
        warnings=warning_messages
    )

    error_messages.clear()
    informational_messages.clear()
    warning_messages.clear()

    return results
