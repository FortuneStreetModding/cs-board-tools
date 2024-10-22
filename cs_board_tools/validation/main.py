"""Holds the entrypoints for running validation checks, which
then use the validation check functions from all the surrounding
files.
"""


from cs_board_tools.errors import (
    get_count,
    get_text,
    IssueType,
    process_log_messages,
    reset_errors_and_warnings,
)
from cs_board_tools.schema.validation import (
    ValidationResult,
    ValidationResultBundle
)
from cs_board_tools.schema.bundle import Bundle
from cs_board_tools.schema.frb import BoardFile
from cs_board_tools.schema.descriptor import MapDescriptor

from .consistency import check_consistency
from .board import check_board_configuration
from .filesystem import check_for_screenshots, check_icon
from .music import check_music_download
from .naming import check_naming_convention
from .paths import check_max_paths
from .venture import check_venture_cards


board_name_ignore_list = [
    "Yoshi's Island", "Mario Circuit", "Peach's Castle", "Mario Stadium",
    "Delfino Plaza", "Super Mario Bros.", "Bowser's Castle", "Starship Mario",
    "Good Egg Galaxy", "Castle Trodain", "Ghost Ship", "Colossus",
    "Mt Magmageddon", "Slimenia", "Robbin' Hood Ruins", "Alefgard",
    "Alltrades Abbey", "The Observatory", "Colossus (Wii Easy)",
    "Good Egg Galaxy (Wii Easy)", "Bowser's Castle (Wii Easy)", "Event Spiral",
    "Shop Texture Test Board"
]


def validate_bundle(
    bundles: list[Bundle],
    gdrive_api_key=None,
    skip_consistency_test=False,
    skip_board_configuration_test=False,
    skip_icon_test=False,
    skip_max_paths_test=False,
    skip_music_download_test=False,
    skip_naming_convention_test=False,
    skip_screenshots_test=False,
    skip_venture_cards_test=False,
    skip_warnings=False
) -> ValidationResultBundle:
    """
    The entry-point for validating board bundles.

    :param bundles: A list of Bundle objects representing your board bundle(s).
    :type bundles: list[Bundle]

    :param gdrive_api_key: Optional. Needed in order to run
        the Music Download test if one of your download
        mirrors is Google Drive. Not used otherwise.
    :type gdrive_api_key: string, optional

    :param skip_consistency_test: If set to True, the Consistency Check
        will be skipped. Defaults to False.
    :type skip_consistency_test: bool, optional

    :param skip_board_configuration_test: If set to True, the Board Configuration
        Checks will be skipped. Defaults to False.
    :type skip_board_configuration_test: bool, optional

    :param skip_mapicon_test: If set to True, the Map Icon Check will
        be skipped. Defaults to False.
    :type skip_max_paths_test: bool, optional

    :param skip_max_paths_test: If set to True, the Max Paths Check will
        be skipped. Defaults to False.
    :type skip_max_paths_test: bool, optional

    :param skip_music_download_test: If set to True, the Music Download
        Check will be skipped. Defaults to False.
    :type skip_music_download_test: bool, optional

    :param skip_naming_convention_test: If set to True, the Naming
        Convention Check will be skipped. Defaults to False.
    :type skip_naming_convention_test: bool, optional

    :param skip_screenshots_test: If set to True, the FRB/Screenshot Check
        will be skipped. Defaults to False.
    :type skip_screenshots_test: bool, optional

    :param skip_venture_cards_test: If set to True, the Venture Card Checks
        will be skipped. Defaults to False.
    :type skip_venture_cards_test: bool, optional

    :param skip_warnings: If set to True, the Venture Card Checks
        that return Warning messages will be skipped. Defaults to False.
    :type skip_warnings: bool, optional

    :return: A bundle containing the overall results, as well as a list
        containing objects that represent each of the individual results.
    :rtype: ValidationResultBundle
    """

    result_bundle = ValidationResultBundle()

    r = []
    for b in bundles:
        reset_errors_and_warnings()
        board_result = ValidationResult()
        board_result.board_name = b.name.en

        if not b.name.en or b.name.en in board_name_ignore_list:
            board_result.board_configuration = check_board_configuration(skip=True)
            board_result.consistency = check_consistency(bundle=b, skip=True)
            board_result.max_paths = check_max_paths(frb="", skip=True)
            board_result.icon = check_icon(bundle=b, skip=True)
            board_result.music_download = check_music_download(skip=True)
            board_result.naming = check_naming_convention(bundle=b, skip=True)
            board_result.screenshots = check_for_screenshots(bundle=b, skip=True)
            board_result.venture = check_venture_cards(bundle=b, skip=True, skip_warnings=skip_warnings)
        else:
            board_result.naming = check_naming_convention(
                bundle=b,
                skip=skip_naming_convention_test,
                skip_warnings=skip_warnings
            )
            board_result.consistency = check_consistency(
                bundle=b,
                skip=skip_consistency_test,
                skip_warnings=skip_warnings
            )

            if len(b.frbs) == 0:
                board_result.board_configuration = check_board_configuration(frb="", skip=True)
                board_result.max_paths = check_max_paths(frb="", skip=True)
                board_result.paths = 0
            else:
                board_result.board_configuration = check_board_configuration(
                    frbs=b.frbs,
                    descriptor=b.descriptor,
                    skip=skip_board_configuration_test,
                    skip_warnings=skip_warnings
                )
                board_result.max_paths = check_max_paths(
                    frb=b.frbs[0],
                    skip=skip_max_paths_test,
                    skip_warnings=skip_warnings
                )
                board_result.paths = int(board_result.max_paths.data)

            board_result.icon = check_icon(
                bundle=b,
                skip=skip_icon_test,
                skip_warnings=skip_warnings
            )

            board_result.music_download = check_music_download(
                descriptor=b.descriptor,
                gdrive_api_key=gdrive_api_key,
                skip=skip_music_download_test,
                skip_warnings=skip_warnings
            )

            board_result.screenshots = check_for_screenshots(
                bundle=b,
                skip=skip_screenshots_test,
                skip_warnings=skip_warnings
            )

            board_result.venture = check_venture_cards(
                bundle=b,
                skip=skip_venture_cards_test,
                skip_warnings=skip_warnings
            )

        # go ahead and process yaml validation results as
        # those get generated elsewhere, on load
        board_result.yaml = b.descriptor.yaml_validation_results
        process_log_messages(errors=board_result.yaml.error_messages)

        errors = get_count(IssueType.ERRORS)
        successes = get_count(IssueType.SUCCESS)
        warnings = get_count(IssueType.WARNINGS)
        issues = errors + warnings
        total = issues + successes

        board_result.error_count = errors
        board_result.success_count = successes
        board_result.warning_count = warnings
        board_result.issue_count = issues
        board_result.total_count = total
        board_result.error_messages = get_text(IssueType.ERRORS)
        board_result.warning_messages = get_text(IssueType.WARNINGS)
        board_result.informational_messages = get_text(IssueType.SUCCESS)

        r.append(board_result)

    result_bundle.boards = r

    error_count = 0
    warning_count = 0
    issue_count = 0
    success_count = 0
    total_count = 0
    error_messages = []
    informational_messages = []
    warning_messages = []

    for m in result_bundle.boards:
        error_count += m.error_count
        warning_count += m.warning_count
        issue_count += m.issue_count
        success_count += m.success_count
        total_count += m.total_count
        informational_messages.extend(m.informational_messages)
        error_messages.extend(m.error_messages)
        warning_messages.extend(m.warning_messages)

    result_bundle.error_count = error_count
    result_bundle.issue_count = issue_count
    result_bundle.success_count = success_count
    result_bundle.total_count = total_count
    result_bundle.warning_count = warning_count

    result_bundle.error_messages = error_messages.copy()
    result_bundle.informational_messages = informational_messages.copy()
    result_bundle.warning_messages = warning_messages.copy()

    reset_errors_and_warnings()
    return result_bundle


def validate_board_file(
    frbs: list[BoardFile],
    skip_board_configuration_tests=False,
    skip_max_paths_test=False,
) -> ValidationResultBundle:
    """
    The entry-point for validating Fortune Avenue-compatible .frb files.

    :param frbs: A list of BoardFile objects representing your .frb(s).
    :type frbs: list[BoardFile]

    :param skip_board_configuration_tests: If set to True, the Board
        Configuration checks will be skipped. Defaults to False.
    :type skip_board_configuration_tests: bool, optional

    :param skip_max_paths_test: If set to True, the Max Paths Check will
        be skipped. Defaults to False.
    :type skip_max_paths_test: bool, optional

    :return: A bundle containing the overall results, as well as a list
        containing objects that represent each of the individual results.
    :rtype: ValidationResultBundle
    """
    result_bundle = ValidationResultBundle()

    r = []
    for f in frbs:
        reset_errors_and_warnings()
        board_result = ValidationResult()
        board_result.board_name = "Unknown .frb"

        board_result.board_configuration = check_board_configuration(
            frb=f,
            skip=skip_board_configuration_tests
        )
        board_result.max_paths = check_max_paths(
            frb=f,
            skip=skip_max_paths_test
        )
        board_result.paths = int(board_result.max_paths.data)

        errors = get_count(IssueType.ERRORS)
        successes = get_count(IssueType.SUCCESS)
        warnings = get_count(IssueType.WARNINGS)
        issues = errors + warnings
        total = issues + successes

        board_result.error_count = errors
        board_result.success_count = successes
        board_result.warning_count = warnings
        board_result.issue_count = issues
        board_result.total_count = total
        board_result.error_messages = get_text(IssueType.ERRORS)
        board_result.warning_messages = get_text(IssueType.WARNINGS)
        board_result.informational_messages = get_text(IssueType.SUCCESS)

        r.append(board_result)

    result_bundle.boards = r

    error_count = 0
    warning_count = 0
    issue_count = 0
    success_count = 0
    total_count = 0
    error_messages = []
    informational_messages = []
    warning_messages = []

    for m in result_bundle.boards:
        error_count += m.error_count
        warning_count += m.warning_count
        issue_count += m.issue_count
        success_count += m.success_count
        total_count += m.total_count
        informational_messages.extend(m.informational_messages)
        error_messages.extend(m.error_messages)
        warning_messages.extend(m.warning_messages)

    result_bundle.error_count = error_count
    result_bundle.issue_count = issue_count
    result_bundle.success_count = success_count
    result_bundle.total_count = total_count
    result_bundle.warning_count = warning_count

    result_bundle.error_messages = error_messages.copy()
    result_bundle.informational_messages = informational_messages.copy()
    result_bundle.warning_messages = warning_messages.copy()

    reset_errors_and_warnings()
    return result_bundle


def validate_descriptor(
    descriptors: list[MapDescriptor],
    gdrive_api_key=None,
    skip_music_download_test=False
) -> ValidationResultBundle:
    """
    The entry-point for validating MapDescriptor .yaml files.

    :param descriptors: A list of MapDescriptor objects representing
        your .yaml files.
    :type descriptors: list[MapDescriptor]

    :param gdrive_api_key: Optional. Needed in order to run
        the Music Download test if one of your download
        mirrors is Google Drive. Not used otherwise.
    :type gdrive_api_key: string, optional

    :param skip_music_download_test: If set to True, the Music Download
        Check will be skipped. Defaults to False.
    :type skip_music_download_test: bool, optional

    :return: A bundle containing the overall results, as well as a list
        containing objects that represent each of the individual results.
    :rtype: ValidationResultBundle
    """
    result_bundle = ValidationResultBundle()

    r = []
    for d in descriptors:
        reset_errors_and_warnings()
        board_result = ValidationResult()
        board_result.board_name = d.name.en

        board_result.music_download = check_music_download(
            descriptor=d,
            skip=skip_music_download_test,
            gdrive_api_key=gdrive_api_key
        )

        # go ahead and process yaml validation results as
        # those get generated elsewhere, on load
        board_result.yaml = d.yaml_validation_results
        process_log_messages(errors=board_result.yaml.error_messages)

        errors = get_count(IssueType.ERRORS)
        successes = get_count(IssueType.SUCCESS)
        warnings = get_count(IssueType.WARNINGS)
        issues = errors + warnings
        total = issues + successes

        board_result.error_count = errors
        board_result.success_count = successes
        board_result.warning_count = warnings
        board_result.issue_count = issues
        board_result.total_count = total
        board_result.error_messages = get_text(IssueType.ERRORS)
        board_result.warning_messages = get_text(IssueType.WARNINGS)
        board_result.informational_messages = get_text(IssueType.SUCCESS)

        r.append(board_result)

    result_bundle.boards = r

    error_count = 0
    warning_count = 0
    issue_count = 0
    success_count = 0
    total_count = 0
    error_messages = []
    informational_messages = []
    warning_messages = []

    for m in result_bundle.boards:
        error_count += m.error_count
        warning_count += m.warning_count
        issue_count += m.issue_count
        success_count += m.success_count
        total_count += m.total_count
        informational_messages.extend(m.informational_messages)
        error_messages.extend(m.error_messages)
        warning_messages.extend(m.warning_messages)

    result_bundle.error_count = error_count
    result_bundle.issue_count = issue_count
    result_bundle.success_count = success_count
    result_bundle.total_count = total_count
    result_bundle.warning_count = warning_count

    result_bundle.error_messages = error_messages.copy()
    result_bundle.informational_messages = informational_messages.copy()
    result_bundle.warning_messages = warning_messages.copy()

    reset_errors_and_warnings()
    return result_bundle
