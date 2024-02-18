"""The CLI module handles interfacing a user's CLI with the rest of the
functions in this library.
"""
import click
import os
import sys

from ..__about__ import __version__
from .bundle import (
    print_bundles,
    print_bundles_validation_result
)
from .frb import (
    print_frbs,
    print_frbs_validation_result
)
from .descriptor import (
    print_descriptors,
    print_descriptors_validation_result
)

from cs_board_tools.io import (
    read_files,
    read_frb,
    read_yaml,
    read_zip
)
from cs_board_tools.validation import (
    validate_bundle,
    validate_board_file,
    validate_descriptor
)

directory_flag_help_message = (
    "The directory to scan, if the board bundle's files are not zipped."
)

file_flag_help_message = (
    "The archive file to open. Should end in .frb, .yaml., or .zip, "
)

display_short_help_message = (
    "Display data from a CSMM-compatible file."
)

validate_short_help_message = (
    "Display validation data about a CSMM-compatible file."
)


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version=__version__, prog_name='cs-board-tools')
@click.pass_context
def cs_board_tools(ctx: click.Context):
    pass


@click.command(short_help=display_short_help_message)
@click.option('-d', '--directory', type=str, help=directory_flag_help_message)
@click.option('-f', '--file', type=str, help=file_flag_help_message)
def display(directory: str, file: str):
    """
    Used to display information from a Fortune Avenue-compatible
    .frb file, a Custom Street Map Manager-compatible .zip file,
    or a Map Descriptor .yaml file. Nicely formats and prints the
    data to your terminal.

    Examples:
    * cs-board-tools display -d /path/to/board_directory/
    * cs-board-tools display -f BoardName.zip

    :param directory: (-d or --directory) A directory name. "."
    works if your working directory is already the directory you
    want to check.

    :type directory: str, optional

    :param file: (-f or --file) A file name. "file.zip" works if
    file.zip is in your current working directory.

    :type file: str, optional
    """
    print("\n        -{========================>")
    print(f"        -{{  cs-board-tools {__version__}  }}-")
    print("        -{     board display      }-")
    print("         <========================}-\n")

    bundles = []

    if directory:
        files = [os.path.join(directory, d) for d in os.listdir(directory)]
        bundles = read_files(files)
        print_bundles(bundles)
    elif file:
        if file.endswith(".frb"):  # if it's a solo .frb file
            frb = read_frb(file)
            print_frbs([frb])
            # print_frbs
        elif file.endswith(".yaml"):  # if it's a solo .yaml file
            descriptor = read_yaml(file)
            print_descriptors([descriptor])
            # print_yamls
        # if it's anything else, it's a bundle. Handle accordingly:
        else:
            bundles = read_zip(file)
            print_bundles(bundles)
    else:
        print(
            "No file or directory was entered. \n"
            "Please specify a directory with -d or --directory "
            "or a file with -f or --file. \n"
            "You can also show help with -h or --help."
        )


@click.command(short_help=validate_short_help_message)
@click.option('-d', '--directory', type=str, help=directory_flag_help_message)
@click.option('-f', '--file', type=str, help=file_flag_help_message)
def validate(directory: str, file: str):
    """
    Used to display validation data from a Fortune Avenue-compatible
    .frb file, a Custom Street Map Manager (CSMM)-compatible .zip file,
    or a Map Descriptor .yaml file. Nicely formats and prints the
    data to your terminal.

    Examples:
    * cs-board-tools validate -d /path/to/board_directory/
    * cs-board-tools validate -f BoardName.zip

    :param directory: (-d or --directory) A directory name. "."
    works if your working directory is already the directory you
    want to check.

    :type directory: str, optional

    :param file: (-f or --file) A file name. "file.zip" works if
    file.zip is in your current working directory.

    :type file: str, optional
    """
    print("\n        -{========================>")
    print(f"        -{{  cs-board-tools {__version__}  }}-")
    print("        -{    board validation    }-")
    print("         <========================}-\n")

    bundles = []

    if directory:
        files = [os.path.join(directory, d) for d in os.listdir(directory)]
        bundles = read_files(files)
        result = validate_bundle(bundles=bundles)
        print_bundles_validation_result(results=result)
    elif file:
        if file.endswith(".frb"):  # if it's a solo .frb file
            frb = read_frb(file)
            result = validate_board_file([frb])
            print_frbs_validation_result(results=result)
        elif file.endswith(".yaml"):  # if it's a solo .yaml file
            descriptor = read_yaml(file)
            result = validate_descriptor([descriptor])
            print_descriptors_validation_result(results=result)
        # if it's anything else, it's a bundle. Handle accordingly:
        else:
            bundles = read_zip(file)
            if len(bundles) == 0:
                print("Please provide a valid input archive.")
                sys.exit(1)

            result = validate_bundle(bundles=bundles)
            print_bundles_validation_result(results=result)
    else:
        print(
            "No file or directory was entered. \n"
            "Please specify a directory with -d or --directory "
            "or a file with -f or --file. \n"
            "You can also show help with -h or --help."
        )

cs_board_tools.add_command(display)
cs_board_tools.add_command(validate)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        cs_board_tools.main(['--help'])
    else:
        cs_board_tools()
