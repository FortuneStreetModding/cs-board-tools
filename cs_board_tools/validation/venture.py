"""Venture Card tests ensure there are exactly 64 cards enabled,
and also that when certain cards are enabled, their prerequisites
are met.
"""
from cs_board_tools.schema.frb import SquareType
from cs_board_tools.validation.results import build_results_object
from cs_board_tools.queries.frb.squaretype import are_square_types_present
from cs_board_tools.schema.bundle import Bundle

venture_45_error = (
    "Venture Card 45 is active, but the board does not contain "
    "both an Arcade square and a Take-A-Break square."
)
venture_125_error = (
    "Venture Card 125 is active, but the board does not contain "
    "both an Arcade square and a Boon square."
)
count_error = (
    "Boards are required to have exactly 64 cards, but {numCards} "
    "are enabled."
)


def check_venture_cards(bundle: Bundle, skip: bool):
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
    # Check Card Count
    if card_info.count != 64:
        error_messages.append(
            count_error.format(numCards=str(card_info.count))
        )

    # Check Venture 45
    if "45" in card_info.numbers:
        present = are_square_types_present(
            bundle.frbs[0], [
                SquareType.ArcadeSquare,
                SquareType.TakeABreakSquare
            ]
        )
        if not present:
            error_messages.append(venture_45_error)

    # Check Venture 125
    if "125" in card_info.numbers:
        present = are_square_types_present(
            bundle.frbs[0], [
                SquareType.ArcadeSquare,
                SquareType.BoonSquare
            ]
        )
        if not present:
            error_messages.append(venture_125_error)

    results = build_results_object(
        errors=error_messages,
        messages=informational_messages,
        warnings=warning_messages,
    )

    error_messages.clear()
    informational_messages.clear()
    warning_messages.clear()

    return results
