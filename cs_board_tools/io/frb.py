"""Entry-point functions for reading and writing Fortune Avenue-compatible
.frb files live here.
"""
from pathlib import Path

from cs_board_tools.schema.frb import (
    BoardFile,
    read_frb as read,
    write_frb as write
)


def read_frb(file_path: Path) -> BoardFile:
    """
    Reads Fortune Avenue .frb board files into Python objects.

    :param file_path: The file name and path to the .frb file to load.
    :type file_path: Path

    :return: An object representing that .frb file, called a BoardFile.
    :rtype: BoardFile
    """
    return read(file_path)


def write_frb(board_file: BoardFile, file_path: Path):
    """
    Saves a BoardFile object back to a Fortune Avenue-compatible .frb file.

    :param board_file: The BoardFile object to save.
    :type board_file: BoardFile

    :param file_path: The file name and path to save the .frb file to.
    :type file_path: Path
    """
    write(board_file, file_path)
