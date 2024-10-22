"""Validation checks related to board configuration, in the .yaml and/or
the .frb file, live here.
"""
from cs_board_tools.schema.descriptor import MapDescriptor
from cs_board_tools.schema.frb import BoardFile, SquareType
from cs_board_tools.schema.validation import CheckResult
from cs_board_tools.validation.results import build_results_object


doors_and_dice_error = (
    "The board contains One Way Alley Door squares "
    "while its Max Dice Roll is set to 9."
)

doors = [
    SquareType.OneWayAlleyDoorA,
    SquareType.OneWayAlleyDoorB,
    SquareType.OneWayAlleyDoorC,
    SquareType.OneWayAlleyDoorD
]

# Mini-checks
# These tests simply return strings when errors occur, then return them to
# be part of the larger "Board Configuration" check.

def check_doors_and_dice(frbs: list[BoardFile]) -> str:
    """
    Checks to ensure that boards that have Max Dice Roll set to 9
    do not have doors. This is a condition that is known to cause the
    game to crash.

    :param frbs: A list of BoardFile objects representing one or more
        .frb files.
    :type frbs: list[BoardFile]

    :return: A string containing the error message if the check
        fails, or an empty string if it passes.
    :rtype: str
    """
    result = ""

    # If Max Dice Roll is set to 9...
    # ...ensure there are no One Way Alley Doors.
    # The combination of these things is unstable
    # in-game and likely to crash the game.
    if frbs[0].board_info.max_dice_roll == 9:
        for f in frbs:
            for s in f._board_data.squares:
                if s.square_type in doors:
                    result = doors_and_dice_error

    return result


def check_square_coordinates(frbs: list[BoardFile]) -> str:
    """
    Checks to see if the board contains any squares with X or Y
    coordinates outside the recommended playing field. Boards
    that stretch too far out can make the game's minimap cover
    too much of the screen. The recommended maximum coordinates
    for a square are +/- 544 Y, 672 X.

    :param frbs: A list of BoardFile objects representing one or more
        .frb files.
    :type frbs: list[BoardFile]

    :return: A string containing the error message if the check
        fails, or an empty string if it passes.
    :rtype: str
    """
    result = ""
    squares_exceeded_dict = {}
    most_squares_exceeded = 0
    filenum = 1

    for f in frbs:
        squares_exceeded = 0

        for s in f._board_data.squares:
            if abs(s.positionX) > 672:
                squares_exceeded + 1
            elif abs(s.positionY) > 544:
                squares_exceeded + 1

        squares_exceeded_dict[filenum] = squares_exceeded

        if squares_exceeded > most_squares_exceeded:
            most_squares_exceeded = squares_exceeded

        filenum + 1

    if most_squares_exceeded > 0:
        squares_exceeded_message = ""
        for k, v in squares_exceeded_dict:
            squares_exceeded_message += f"{k}: {v}, "

        result = (
            "This board contains squares that exceed the "
            "recommended maximum coordinates of +/- 544 Y, "
            "672 X. The results of the the check are as "
            "follows, illustrating the number of offending"
            f"squares in each .frb file: {squares_exceeded_message}"
        )

    return result


def check_switch_ids(frbs: list[BoardFile]) -> str:
    """
    Checks the Destination ID of any Switch squares in any of the
    frbs equal the number of total frbs there are in this bundle.

    :param frbs: A list of BoardFile objects representing one or more
        .frb files.
    :type frbs: list[BoardFile]

    :return: A string containing the error message if the check
        fails, or an empty string if it passes.
    :rtype: str
    """
    offending_switch_dict = {}
    at_least_one_bad_switch = False
    result = ""

    for f in frbs:
        offending_switches_in_file = 0
        for s in f.squares:
            if s.square_type == SquareType.SwitchSquare:
                if s.district_destination_id != len(frbs):
                    offending_switches_in_file + 1
        if offending_switches_in_file > 0:
            offending_switch_dict[f"{f}"] = offending_switches_in_file
            at_least_one_bad_switch = True

    if at_least_one_bad_switch:
        switch_message = ""
        for k,v in offending_switch_dict:
            switch_message += f"{k}: {v}, "
        result = (
            "At least one of the Switch squares in at least one of "
            "your .frb files has a Destination Square ID that is set "
            "incorrectly. This value should match the total number of "
            ".frb files in your bundle. The check's results are as "
            f"follows: {switch_message}"
        )
    return result


def check_two_way_doors(frbs: list[BoardFile]) -> str:
    """
    Checks that there are no Two-Way Doors if Max Dice Roll is set to
    8 or 9. (A Two-Way door is a One-Way Door whose Destination ID is
    set to the ID of another door.)

    :param frbs: A list of BoardFile objects representing one or more
        .frb files.
    :type frbs: list[BoardFile]

    :return: A string containing the error message if the check
        fails, or an empty string if it passes.
    :rtype: str
    """
    door_ids = []
    frb = frbs[0]
    result = ""
    waypoint_connection_ids = []

    # populate door_ids list
    for idx, s in enumerate(frb.squares):
        if s.square_type in doors:
            door_ids.append(idx)

    # populate waypoint_connection_ids list
    for d in door_ids:
        for w in frb.squares[d].waypoints:
            waypoint_connection_ids.append(w.entryId)
            for i in w.destinations:
                waypoint_connection_ids.append(i)

    # check to see if any of the waypoint connection ids are doors
    # if yes = a two-way door is present
    for w in waypoint_connection_ids:
        if w in door_ids:
            if frb.board_info.max_dice_roll > 7:
                return (
                    "This board uses Two-Way Doors, and Max Dice Roll is "
                    "> 7. This is a scenario that can cause crashes, so "
                    "please switch to using One-Way Alley Ends (rather "
                    "than linking Doors directly), or reduce Max Dice Roll "
                    "to be less than or equal to 7."
                )

    return result


def check_yaml_authors(descriptor: MapDescriptor) -> str:
    """
    Checks to ensure that a board's .yaml descriptor file has
    defined at least one Author.

    :param descriptor: A MapDescriptor object representing a .yaml file.
    :type descriptor: MapDescriptor

    :return: A string containing the error message if the check
        fails, or an empty string if it passes.
    :rtype: str
    """

    if not descriptor.authors:
        return "The .yaml board descriptor does not define any authors."


def check_yaml_changelog(descriptor: MapDescriptor) -> str:
    """
    Checks to ensure that a board's .yaml descriptor file defines a
    changelog.

    :param descriptor: A MapDescriptor object representing a .yaml file.
    :type descriptor: MapDescriptor

    :return: A string containing the error message if the check
        fails, or an empty string if it passes.
    :rtype: str
    """
    if not descriptor.changelog:
        return "The .yaml board descriptor does not define a changelog."


def check_yaml_max_dice_roll(descriptor: MapDescriptor) -> str:
    """
    Checks to ensure that the board's Max Dice Roll is set to 9
    or lower.

    :param descriptor: A MapDescriptor object representing a .yaml file.
    :type descriptor: MapDescriptor

    :return: A string containing the error message if the check
        fails, or an empty string if it passes.
    :rtype: str
    """
    if int(descriptor.max_dice_roll) > 9:
        return "Max Dice Roll must be set to 9 or lower."


def check_board_configuration(descriptor: MapDescriptor = None, frbs: list[BoardFile] = None, skip: bool = False, skip_warnings: bool = False) -> CheckResult:
    """
    An entry-point for checks related to the current board configuration
    as defined in the .frb board file and/or .yaml descriptor file. Both
    descriptor and frb are optional parameters, but at least one of them
    needs to be present. Additional checks are performed if both are
    present.

    :param descriptor: A MapDescriptor object representing a
        .yaml file.
    :type descriptor: MapDescriptor, optional

    :param frb: A BoardFile object representing an .frb file.
    :type frbs: list[BoardFile], optional

    :param skip: If set to True, the check will be skipped, but a
        valid resultobject with no messages and SKIPPED as its
        status will still be returned. Defaults to False.
    :type skip: bool, optional

    :param skip_warnings: If set, skips tests resulting in
        "Warning" messages.
    :type skip_warnings: bool, optional

    :return: A CheckResult object containing the check status as
        well as any messages and additional data.
    :rtype: CheckResult
    """

    error_messages = []
    informational_messages = []
    warning_messages = []

    if skip:
        return build_results_object(skip=True)


    # Mini-checks for individual or groups of issues go here.

    # descriptor and frb checks
    # if descriptor and frbs:


    # descriptor checks
    if descriptor:
        author_result = check_yaml_authors(descriptor)
        if author_result:
            error_messages.append(author_result)

        changelog_result = check_yaml_changelog(descriptor)
        if changelog_result:
            error_messages.append(changelog_result)

        max_dice_roll_result = check_yaml_max_dice_roll(descriptor)
        if max_dice_roll_result:
            error_messages.append(max_dice_roll_result)

    # frb checks
    if frbs:
        doors_and_dice_result = check_doors_and_dice(frbs)
        if doors_and_dice_result:
            error_messages.append(doors_and_dice_result)

        square_coordinates_result = check_square_coordinates(frbs)
        if square_coordinates_result:
            error_messages.append(square_coordinates_result)

        switch_id_result = check_switch_ids(frbs)
        if switch_id_result:
            error_messages.append(switch_id_result)

        two_way_door_result = check_two_way_doors(frbs)
        if two_way_door_result:
            error_messages.append(two_way_door_result)

    # Result tabulation, reset, and return

    results = build_results_object(
        errors=error_messages,
        messages=informational_messages,
        warnings=warning_messages
    )

    error_messages.clear()
    informational_messages.clear()
    warning_messages.clear()

    return results
