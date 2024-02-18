"""Queries relating to which SquareTypes are present on a board live here.
"""
from cs_board_tools.schema.frb import BoardFile, SquareType


def are_square_types_present(frb: BoardFile, t: list[SquareType]) -> bool:
    """
    Accepts a list of SquareTypes, searches a given BoardFile object for
    Squares of that SquareType, and returns a boolean search result.

    :param frb: A BoardFile object that you would like to search.
    :type frb: BoardFile

    :param t: A list of SquareTypes to search the board for.
    :type t: list[SquareType]

    :return: The result of the search. If True, the SquareType was present.
    :rtype: bool
    """
    types = []
    for i, square in enumerate(frb.squares):
        types.append(square.square_type)
    result = all(item in types for item in t)
    return result


def is_square_type_present(frb: BoardFile, t: SquareType) -> bool:
    """
    Accepts a single SquareType, searches a given BoardFile object for
    Squares of that SquareType, and returns a boolean search result.

    :param frb: A BoardFile object that you would like to search.
    :type frb: BoardFile

    :param t: A SquareType that you would like to search the board for.
    :type t: SquareType

    :return: The result of the search. If True, the SquareType was present.
    :rtype: bool
    """
    result = False
    for i, square in enumerate(frb.squares):
        if square.square_type == t:
            result = True
    return result
