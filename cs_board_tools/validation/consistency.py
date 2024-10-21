"""Consistency checks involve making sure that values that live in both
the Fortune Avenue-compatible .frb board file and the Map Descriptor
.yaml file match.
"""
from cs_board_tools.schema.bundle import Bundle
from cs_board_tools.schema.frb import LoopingMode
from cs_board_tools.schema.validation import CheckResult
from cs_board_tools.validation.results import build_results_object


file_not_found_error = (
    "The board file(s) specified in the (.yaml) board "
    "descriptor could not be found."
)
mismatch_error = (
    "The value of {attribute} is {yamlValue} in the "
    "yaml file but {frbValue} in the frb file."
)

error_messages = []
informational_messages = []
warning_messages = []


def compare_values(frbValue, yamlValue, attribute):
    """
    A function that compares two values, one from the
    Fortune Avenue-compatible .frb board file, and the
    other from the Map Descriptor .yaml file.

    The attribute parameter tells the function what
    we're comparing, so we can build the error message
    appropriately if it doesn't match.

    :param frbValue: The value from the .frb file.
    :type frbValue: string

    :param yamlValue: The value from the .yaml file.
    :type yamlValue: string

    :param attribute: The attribute, in string form, which we are comparing.
    :type attribute: string

    """
    if not frbValue or not yamlValue:
        return
    global error_messages
    if frbValue != yamlValue:
        error_messages.append(
            mismatch_error.format(
                attribute=attribute,
                frbValue=frbValue,
                yamlValue=yamlValue
            )
        )


def convert_galaxy_status(galaxyStatus) -> str:
    """
    This function converts the Galaxy Status, as it's stored in the
    Fortune Avenue-compatible .frb file, into a string that matches
    what we store in the Map Descriptor .yaml file.

    :param galaxyStatus:
    :type galaxyStatus: cs_board_tools.schema.frb.LoopingMode

    :return: A string representing the equivalent value to what was
        passed in, but in a format that can be compared to the Map
        Descriptor .yaml file.
    :rtype: str
    """
    loopingMode = "unknown"
    match (galaxyStatus):
        case LoopingMode.NONE:
            loopingMode = "none"
        case LoopingMode.BOTH:
            loopingMode = "both"
        case LoopingMode.VERTICAL:
            loopingMode = "vertical"
    return loopingMode


def check_consistency(bundle: Bundle, skip: bool, skip_warnings: bool = False) -> CheckResult:
    """
    Checks to ensure that values that are stored in both the
    Fortune Avenue-compatible .frb board file, and in the Map
    Descriptor .yaml file, are the same.

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

    global error_messages
    global informational_messages
    global warning_messages

    if len(bundle.frbs) == 0:
        error_messages.append(file_not_found_error)
    else:
        frb_info = bundle.frbs[0].board_info
        yaml_info = bundle.descriptor

        compare_values(
            frb_info.base_salary,
            yaml_info.base_salary,
            "baseSalary"
        )
        compare_values(
            frb_info.initial_cash,
            yaml_info.initial_cash,
            "initialCash"
        )
        compare_values(
            frb_info.max_dice_roll,
            yaml_info.max_dice_roll,
            "maxDiceRoll"
        )
        compare_values(
            frb_info.salary_increment,
            yaml_info.salary_increment,
            "salaryIncrement"
        )

        # convert_galaxy_status is needed to convert the
        # Galaxy Status int from the frb into something
        # we can compare to the string value in the yaml
        frb_loop_mode = convert_galaxy_status(frb_info.galaxy_status)
        yaml_loop_mode = "none"
        if bundle.descriptor.looping is not None:
            yaml_loop_mode = bundle.descriptor.looping.mode.lower()
        compare_values(frb_loop_mode, yaml_loop_mode, "looping mode")

    results = build_results_object(
        errors=error_messages,
        messages=informational_messages,
        warnings=warning_messages
    )

    error_messages.clear()
    informational_messages.clear()
    warning_messages.clear()

    return results
