"""The code that handles extracting .zip files live here.
"""
import os
from zipfile import ZipFile


def extract_zip_file(file, path):
    """This function handles extracting the zip file,
    if one is passed in by the user.

    :param file: The filename of the .zip archive.
    :type file: str
    :param path: The path it should be extracted to.
        Typically, this is the chosen temporary directory.
    :type path: str
    :return: Returns a list of the files that were extracted,
        with the relative path attached.
    :rtype: list[str]
    """
    # read in the zip file and extract it
    with ZipFile(file, "r") as zip:
        filenames = []
        subdir = False
        for entry in zip.infolist():
            filenames.append(entry.filename)
            if "/" in entry.filename:
                subdir = True
        if not path:
            path = "./upload"

        # if we're dealing with filenames that contain slashes,
        # it's likely that they are already in a subdirectory.
        # so we should roll with that path.
        if subdir:
            path = path
        # otherwise, put it in its own subdirectory based
        # on the board name.
        else:
            path = f"{path}/{os.path.basename(file)[:-4]}"

        zip.extractall(path)
    zip.close()
    return [f"{path}/{f}" for f in filenames]
