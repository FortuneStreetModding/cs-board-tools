"""Entry-point functions for loading Bundles -- either .zip file
archives or full directories of files directly -- live here.
"""
import os
from pathlib import Path

from cs_board_tools.io.frb import read_frb
from cs_board_tools.io.yaml import read_yaml
from cs_board_tools.schema.bundle import Bundle
from cs_board_tools.utilities import extract_zip_file, cleanup


def read_files(files: list[Path]) -> list[Bundle]:
    """
    Reads one or more Map Bundles from a single directory. (A list of files)

    :param files: A list of Path objects representing each file. Should
        at least include filename if they are in the same directory as
        your current shell but should include path as well if they are
        elsewhere.
    :type files: list[Path]

    :return: Returns a list of Bundles, representing however many bundles
        you passed the files in for. If only one, you will get a list of
        bundles of length 1.
    :rtype: list[Bundle]
    """
    if not files:
        return ["no files found!"]

    frb_filenames = []
    webp_filenames = []
    png_filenames = []
    yaml_filenames = []
    zip_filenames = []
    directories = []
    unused_filenames = []

    # get all the files we care about:

    for x in files:
        if x.endswith(".frb"):
            frb_filenames.append(x)
        elif x.endswith(".png"):
            png_filenames.append(x)
        elif x.endswith(".webp"):
            webp_filenames.append(x)
        elif x.endswith(".yaml"):
            yaml_filenames.append(x)
        elif x.endswith(".zip"):
            zip_filenames.append(x)
        elif x.endswith("/"):
            directories.append(x)
        else:
            unused_filenames.append(x)

    # # now we can actually start processing them
    bundles = []
    for y in yaml_filenames:
        bundle = Bundle()
        bundle.descriptor = read_yaml(y)

        bundle.authors = bundle.descriptor.authors
        bundle.background = bundle.descriptor.background
        bundle.description = bundle.descriptor.description
        bundle.icon = bundle.descriptor.icon
        bundle.music = bundle.descriptor.music
        bundle.name = bundle.descriptor.name

        board_files = []
        frb_filenames = []
        screenshots = []

        for f in bundle.descriptor.frbs:

            for file in files:
                if f in file and "frb" in file:
                    frb_filenames.append(f"{file}")
            # reading screenshots
            for w in webp_filenames:
                if f in w:
                    screenshots.append(w)

        # reading board files
        for filename in frb_filenames:
            board_files.append(read_frb(filename))

        bundle.frbs = board_files
        bundle.frb_filenames = frb_filenames
        bundle.screenshots = screenshots

        bundles.append(bundle)

    return bundles


def read_zip(file_path: Path, temp_dir_path: str = "./temp") -> list[Bundle]:
    """
    Reads one or more Map Bundles from a .zip file.

    :param file_path: A Path object representing the .zip file. Should
        at least include filename, but should include path as well if
        the .zip file is in a different directory than your current shell.
        ProTip: This .zip file can contain multiple bundles; this is why the
        function returns list[Bundle].
    :type file_path: Path

    :return: Returns a list of Bundles, representing however many bundles
        you passed the files in for. If only one, you will get a list of
        Bundles of length 1.
    :rtype: list[Bundle]
    """
    we_created_temp_dir = False
    if not os.path.exists(temp_dir_path):
        we_created_temp_dir = True
        os.mkdir(temp_dir_path)

    files = extract_zip_file(file_path, temp_dir_path)

    # if files is singular, see if it ends in .zip
    # if it does, extract it
    if not files:
        return ["no files found!"]

    frb_filenames = []
    webp_filenames = []
    png_filenames = []
    yaml_filenames = []
    zip_filenames = []
    directories = []
    unused_filenames = []

    # get all the files we care about:

    for x in files:
        if x.endswith(".frb"):
            frb_filenames.append(x)
        elif x.endswith(".png"):
            png_filenames.append(x)
        elif x.endswith(".webp"):
            webp_filenames.append(x)
        elif x.endswith(".yaml"):
            yaml_filenames.append(x)
        elif x.endswith(".zip"):
            zip_filenames.append(x)
        elif x.endswith("/"):
            directories.append(x)
        else:
            unused_filenames.append(x)

    files_minus_directories = [f for f in files if f not in directories]

    bundles = read_files(files)

    cleanup(
        temp_dir=temp_dir_path,
        directories=directories,
        files=files_minus_directories,
        should_delete=we_created_temp_dir
    )

    return bundles
