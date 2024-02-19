"""Utilities involving the filesystem that other tasks have needed
repeatedly -- namely, functions that assist with proper handling of
temporary files.
"""
import os


def get_files_recursively(directory):
    """
    This function takes a directory, and adds all of its files to an array,
    then traverses through any subdirectories and adds those files too. Once
    complete, it returns that array.

    :param directory: A directory to search.
    :type directory: Path
    """
    files = [os.path.join(directory, d) for d in os.listdir(directory)]
    for obj in files:
        if os.path.isdir(obj):
            files.extend(get_files_recursively(os.path.join(directory, obj)))
    return files


def remove_temp_directories(directories):
    """
    This function empties and removes all the directories passed
    to it.

    It is only used by the zip part of this module to clean up
    its mess as it has to extract the zip, then load it in as a
    Python object, then delete the files from disk.

    :param directories: A list of directories to remove.
    :type directories: list[Path]
    """
    import os
    for d in directories:
        if os.path.exists(d):
            filelist = [os.path.join(d, f) for f in os.listdir(d)]
            for f in filelist:
                if os.path.isdir(f):
                    os.rmdir(f)
                if os.path.isfile(f):
                    os.remove(f)
            os.rmdir(d)


def remove_temp_files(files):
    """
    This function removes all the files passed to it.

    It is only used by the zip part of this module to clean up
    its mess as it has to extract the zip, then load it in as a
    Python object, then delete the files from disk.

    :param files: A list of files to remove.
    :type files: list[Path]
    """
    for f in files:
        if os.path.exists(f):
            os.remove(f)


def cleanup(temp_dir, directories, files, should_delete):
    """
    This function serves as an aggregate entrypoint for the
    other two. Most functions, that need this functionality
    from other files will call this function rather than the
    calling remove_temp_directories and remove_temp_files
    directly. It also has the added bit of handling whether or
    not to delete the temporary directory (which is determined
    by whether or not we created the directory. This module
    otherwise will leave the directory but remove all the files
    it knows it extracted from the .zip archive.)

    :param temp_dir: The temporary directory.
    :type temp_dir: Path

    :param directories: A list of directories to remove.
    :type directories: list[Path]

    :param files: A list of files to remove.
    :type files: list[Path]

    :param should_delete: A bool determining whether or not to
        remove the directory passed through the temp_dir
        parameter.
    :type should_delete: bool
    """
    # delete the files we extracted from the zip
    remove_temp_files(files)
    remove_temp_directories(directories)

    # temporary directory management; don't
    # delete it if we didn't create it
    if should_delete:
        remove_temp_directories([temp_dir])
