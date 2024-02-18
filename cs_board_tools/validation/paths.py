"""These tests check Paths counts to ensure things will work
and be compatible once the board has been added into the game.
"""
from cs_board_tools.schema.frb import BoardFile, Square
from cs_board_tools.schema.validation import CheckResult
from cs_board_tools.validation.results import build_results_object

max_paths_warning = (
    "The Max Paths value of {max_paths} is higher than {limit}."
)


def get_destinations(
    squares: list[Square],
    prev_square_id: int,
    square_id: int
) -> list[int]:
    """
    Looks at a Square's waypoints and returns a list of possible
    destinations for a given Entry ID.

    :param squares: A list of Square objects to test.
    :type squares: list[Square]

    :param prev_square_id: The ID of the Previous Square, the
        one you previously walked over in-game. The one you have
        your back to.
    :type prev_square_id: int

    :param square_id: The ID of the Square for which to get the
        paths count.
    :type square_id: int

    :return: Returns a list of Square IDs as Destinations.
    :rtype: list[int]
    """
    destinations = []

    if not (square_id < len(squares) or square_id == 255):
        return
    if not (prev_square_id < len(squares) or prev_square_id == 255):
        return

    square = squares[square_id]
    for w in square.waypoints:
        for d in w.destinations:
            if w.entryId == prev_square_id or prev_square_id == 255:
                if d != 255:
                    destinations.append(d)
    return list(set(destinations))


def get_paths_count(
    squares: list[Square],
    prev_square_id: int,
    square_id: int,
    dice: int,
    limit: int
):
    """
    This function calculates the number of paths on a square.

    :param squares: A list of Square objects to test.
    :type squares: list[Square]

    :param prev_square_id: The ID of the Previous Square, the
        one you previously walked over in-game. The one you have
        your back to.
    :type prev_square_id: int

    :param square_id: The ID of the Square for which to get the
        paths count.
    :type square_id: int

    :param dice: The Maximum Dice Roll value of the board, which
        is used as the search depth in the calculation.
    :type dice: int

    :param limit: An upper limit of Max Paths to prevent computer
        slowdown.
    :type limit: int

    :return: Returns the number of paths from that square.
    :rtype: int
    """
    count = 0
    if dice == 0:
        count += 1
        return count

    destinations = get_destinations(
        squares=squares,
        prev_square_id=prev_square_id,
        square_id=square_id,
    )
    for d in destinations:
        if d < len(squares):
            count += get_paths_count(
                squares=squares,
                prev_square_id=square_id,
                square_id=d,
                dice=(dice - 1),
                limit=limit,
            )
    return count


def get_paths_count_without_prev_square(
    squares: list[Square],
    square_id: int,
    dice: int,
    limit: int
) -> int:
    """
    As the title suggests, this function calculates the number of
    paths on a square, when a previous Square ID is not provided.

    :param squares: A list of Square objects to test.
    :type squares: list[Square]

    :param square_id: The ID of the Square for which to get the
        paths count.
    :type square_id: int

    :param dice: The Maximum Dice Roll value of the board, which
        is used as the search depth in the calculation.
    :type dice: int

    :param limit: An upper limit of Max Paths to prevent computer
        slowdown.
    :type limit: int

    :return: Returns the number of paths from that square.
    :rtype: int
    """
    paths_count = 0
    paths_count = get_paths_count(
        squares=squares,
        square_id=square_id,
        prev_square_id=255,
        dice=dice,
        limit=limit,
    )
    return paths_count


def calculate_max_paths(
    squares: list[Square],
    dice: int,
    limit: int
) -> [int, int]:
    """
    Calculates the Max Paths value for all squares.

    :param squares: A list of Square objects to test.
    :type squares: list[Square]

    :param dice: The Maximum Dice Roll value of the board, which
        is used as the search depth in the calculation.
    :type dice: int

    :param limit: An upper limit of Max Paths to prevent computer
        slowdown.
    :type limit: int

    :return: Returns a tuple with the square ID with the maximum
        max paths count, and the max paths count itself.
    :rtype: [int, int]
    """
    max_paths_count = 0
    square_id_with_max_paths_count = 255
    for i in range(len(squares)):
        paths_count = get_paths_count_without_prev_square(
            squares=squares, square_id=i, dice=dice, limit=limit
        )
        if paths_count > max_paths_count:
            max_paths_count = paths_count
            square_id_with_max_paths_count = i
        paths_count = 0

    return [square_id_with_max_paths_count, max_paths_count]


def check_max_paths(frb: BoardFile, skip: bool) -> CheckResult:
    """
    Checks the Max Paths values for all squares on a board, and warns
    if the values are too high.

    This warns, rather than erroring, because although a high max paths
    value is likely to indicate that a game played on this board will
    crash, it doe not necessarily indicate that. There are boards with
    values as high as 220 that work totally fine. Yet another with a
    value of 135 might crash.

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

    search_depth = int(len(frb._board_data.squares) / 3)

    if search_depth < 16:
        search_depth = 16

    paths = calculate_max_paths(
        squares=frb._board_data.squares, dice=search_depth, limit=1000
    )

    if paths[1] > 100:
        warning_messages.append(
            max_paths_warning.format(max_paths=paths[1], limit=100)
        )

    results = build_results_object(
        errors=error_messages,
        messages=informational_messages,
        warnings=warning_messages,
        data=paths[1]
    )

    error_messages.clear()
    informational_messages.clear()
    warning_messages.clear()

    return results
