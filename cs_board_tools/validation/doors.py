"""The Doors and Dice check ensures that if the Max Dice Roll is 9,
One-Way Alley Doors do not exist in the .frb file, and vice versa.
"""
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


def check_doors(frb: BoardFile, skip: bool) -> CheckResult:
    """
    Checks to ensure that boards that have Max Dice Roll set to 9
    do not have doors, and that boards with doors do not have a Max
    Dice Roll of 9.

    This is a condition that is known to cause the
    game to crash.

    :param frb: A BoardFile object representing an .frb file.
    :type frb: BoardFile

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
    # If the Max Dice Roll is not set to 9,
    # none of our checks at the moment are
    # relevant. So just return an OK and move on.
    if frb.board_info.max_dice_roll != 9:
        return build_results_object(
            messages=informational_messages,
            success=True
        )
    # If Max Dice Roll is set to 9...
    # ...ensure there are no One Way Alley Doors.
    # The combination of these things is unstable
    # in-game and likely to crash the game.
    for s in frb._board_data.squares:
        if s.square_type in doors:
            error_messages.append(doors_and_dice_error)
            break

    results = build_results_object(
        errors=error_messages,
        messages=informational_messages,
        warnings=warning_messages
    )

    error_messages.clear()
    informational_messages.clear()
    warning_messages.clear()

    return results
