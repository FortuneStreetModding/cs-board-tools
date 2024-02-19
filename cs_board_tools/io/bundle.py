"""Entry-point functions for loading Bundles -- either .zip file
archives or full directories of files directly -- live here.
"""
import os
from pathlib import Path

from cs_board_tools.io.frb import read_frb
from cs_board_tools.io.yaml import read_yaml
from cs_board_tools.schema.bundle import Bundle
from cs_board_tools.utilities import extract_zip_file, cleanup



def cleanup_filenames(filenames: list[str]) -> list[str]:
    """
    Takes in a list of filenames and cleans them up. This means removing
    any directory/path information, trailing slashes, or other common
    characters in an attempt to normalize these values as much as possible.

    :param filenames: A list of filenames. These values can be relative or
        absolute, or a combination of both.
    :type filenames: list[str]

    :return: A normalized list of filenames. (filename.extension)
    :rtype: list[str]
    """
    better_filenames = []
    for f in filenames:
        cleaned_up_f = f
        if cleaned_up_f[0:2] == "./":
            cleaned_up_f = cleaned_up_f[2:]
        if cleaned_up_f[-1] == "/":
            cleaned_up_f = cleaned_up_f[:-1]
        if "/" in cleaned_up_f:
            cleaned_up_f = cleaned_up_f.rsplit("/", 1)[1]
        better_filenames.append(cleaned_up_f)
    return better_filenames


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

    brstm_filenames = []
    cmpres_filenames = []
    frb_filenames = []
    png_filenames = []
    webp_filenames = []
    yaml_filenames = []
    zip_filenames = []

    directories = []
    unused_filenames = []

    # get all the files we care about:
    for x in files:
        if x.endswith(".brstm"):
            brstm_filenames.append(x)
        elif x.endswith(".cmpres"):
            cmpres_filenames.append(x)
        elif x.endswith(".frb"):
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
        bundle_path = y.rsplit("/", 1)[0]

        bundle.authors = bundle.descriptor.authors
        bundle.background = bundle.descriptor.background

        screenshot_paths = [f for f in webp_filenames if f"{bundle_path}/" in f]

        bundle.filenames.brstm = cleanup_filenames([f for f in brstm_filenames if f"{bundle_path}/" in f])
        bundle.filenames.cmpres = cleanup_filenames([f for f in cmpres_filenames if f"{bundle_path}/" in f])
        bundle.filenames.frb = cleanup_filenames([f for f in frb_filenames if f"{bundle_path}/" in f])
        bundle.filenames.png = cleanup_filenames([f for f in png_filenames if f"{bundle_path}/" in f])
        bundle.filenames.webp = cleanup_filenames(screenshot_paths)
        bundle.filenames.yaml = cleanup_filenames([f for f in yaml_filenames if f"{bundle_path}/" in f])

        bundle.icon = bundle.descriptor.icon
        bundle.music = bundle.descriptor.music
        bundle.name = bundle.descriptor.name

        board_files = []
        for f in bundle.filenames.frb:
            board_files.append(read_frb(f"{bundle_path}/{f}"))

        bundle.frbs = board_files
        bundle.screenshots = screenshot_paths

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

    directories = []

    for x in files:  # I love this joke
        if x.endswith("/"):
            directories.append(x)

    files_minus_directories = [f for f in files if f not in directories]

    bundles = read_files(files)

    cleanup(
        temp_dir=temp_dir_path,
        directories=directories,
        files=files_minus_directories,
        should_delete=we_created_temp_dir
    )

    return bundles
