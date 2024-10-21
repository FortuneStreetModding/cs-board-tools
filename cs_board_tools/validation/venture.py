"""Venture Card tests ensure there are exactly 64 cards enabled,
and also that when certain cards are enabled, their prerequisites
are met.
"""
from cs_board_tools.schema.frb import SquareType
from cs_board_tools.validation.results import build_results_object
from cs_board_tools.queries.frb.squaretype import are_square_types_present
from cs_board_tools.schema.bundle import Bundle

count_error = (
    "Boards are required to have exactly 64 cards, but {numCards} "
    "are enabled."
)

count_warning = (
    "No venture cards have been specified. This will work, but a default "
    "assortment of Venture Cards will be activated."
)

venture_45_error = (
    "Venture Card 45 is active, but the board does not contain "
    "both an Arcade square and a Take-A-Break square."
)

venture_87_warning = (
    "Max Dice Roll is set to {max_dice_roll}, but Venture Card 87 is "
    "enabled. Venture Card 87 makes the player roll either a 7 or an "
    "8, which can work, but can also cause issues since this value being "
    "higher than the Max Dice Roll makes it very hard to test pathing for."
)

venture_115_warning = (
    "Max Dice Roll is set to {max_dice_roll}, but Venture Card 115 is "
    "enabled. Venture Card 115 makes the player roll an 7, which can "
    "work, but can also cause issues since this value being higher "
    "than the Max Dice Roll makes it very hard to test pathing for."
)

venture_125_error = (
    "Venture Card 125 is active, but the board does not contain "
    "both an Arcade square and a Boon square."
)


def check_card_45(bundle: Bundle, numbers: list[int]) -> str:
    result = ""
    if 45 in numbers:
        present = are_square_types_present(
            bundle.frbs[0], [
                SquareType.ArcadeSquare,
                SquareType.TakeABreakSquare
            ]
        )
        if not present:
            result = venture_45_error
    return result


def check_card_87(bundle: Bundle, numbers: list[int]) -> str:
    result = ""
    if 87 in numbers:
        max_dice_roll = bundle.descriptor.max_dice_roll
        if max_dice_roll < 8:
            result = venture_87_warning.format(max_dice_roll=str(max_dice_roll))
    return result


def check_card_115(bundle: Bundle, numbers: list[int]) -> str:
    result = ""
    if 115 in numbers:
        max_dice_roll = bundle.descriptor.max_dice_roll
        if max_dice_roll < 7:
            result = venture_115_warning.format(max_dice_roll=str(max_dice_roll))
    return result


def check_card_125(bundle: Bundle, numbers: list[int]) -> str:
    result = ""
    if 125 in numbers:
        present = are_square_types_present(
            bundle.frbs[0], [
                SquareType.ArcadeSquare,
                SquareType.BoonSquare
            ]
        )
        if not present:
            result = venture_125_error
    return result


def check_venture_cards(bundle: Bundle, skip: bool = False, skip_warnings: bool = False):
    """
    Checks to ensure that if certain Venture Cards are enabled,
    that their accompanying Square types are present on the board.

    After all, being warped to an Arcade Square requires there to
    _be_ an Arcade Square.

    :param bundle: A Bundle object representing a board.
    :type bundle: Bundle

    :param skip: If set to True, the check will be skipped, but a
    valid resultobject with no messages and SKIPPED as its
    status will still be returned.
    :type skip: bool

    :param skip_warnings: If set to True, the checks that return
    Warnings will be skipped, but a valid resultobject with
    no messages and SKIPPED as its status will still be
    returned.
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

    card_info = bundle.descriptor.venture_cards
    if not skip_warnings:
        if card_info.count == 0:
            warning_messages.append(count_warning)

        result_87 = check_card_87(bundle=bundle, numbers=card_info.numbers)
        if result_87:
            warning_messages.append(result_87)

        result_115 = check_card_115(bundle=bundle, numbers=card_info.numbers)
        if result_115:
            warning_messages.append(result_115)

    # Check Card Count
    if card_info.count != 64 and card_info.count != 0:
        error_messages.append(count_error.format(numCards=str(card_info.count)))

    # Check Venture Cards
    result_45 = check_card_45(bundle=bundle, numbers=card_info.numbers)
    if result_45:
        error_messages.append(result_45)

    result_125 = check_card_125(bundle=bundle, numbers=card_info.numbers)
    if result_125:
        error_messages.append(result_125)

    results = build_results_object(
        errors=error_messages,
        messages=informational_messages,
        warnings=warning_messages,
    )

    error_messages.clear()
    informational_messages.clear()
    warning_messages.clear()

    return results
