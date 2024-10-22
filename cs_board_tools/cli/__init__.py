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
from cs_board_tools.utilities import get_files_recursively
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
def display(directory: str, file: str, gdrive_api_key=None):
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
@click.option('-sbc', '--skip-board-configuration-test', is_flag=True, flag_value=True, default=False)
@click.option('-sct', '--skip-consistency-test', is_flag=True, flag_value=True, default=False)
@click.option('-smt', '--skip-icon-test', is_flag=True, flag_value=True, default=False)
@click.option('-spt', '--skip-max-paths-test', is_flag=True, flag_value=True, default=False)
@click.option('-sdt', '--skip-music-download-test', is_flag=True, flag_value=True, default=False)
@click.option('-snt', '--skip-naming-convention-test', is_flag=True, flag_value=True, default=False)
@click.option('-sst', '--skip-screenshots-test', is_flag=True, flag_value=True, default=False)
@click.option('-svt', '--skip-venture-cards-test', is_flag=True, flag_value=True, default=False)
@click.option('-sw', '--skip-warnings', is_flag=True, flag_value=True, default=False)
@click.option('-g', '--gdrive-api-key', is_flag=False, flag_value=None, default=None)
@click.option('-d', '--directory', type=str, help=directory_flag_help_message)
@click.option('-f', '--file', type=str, help=file_flag_help_message)
def validate(directory: str,
             file: str,
             gdrive_api_key: str = None,
             skip_board_configuration_test: bool = False,
             skip_consistency_test: bool = False,
             skip_icon_test: bool = False,
             skip_max_paths_test: bool = False,
             skip_music_download_test: bool = False,
             skip_naming_convention_test: bool = False,
             skip_screenshots_test: bool = False,
             skip_venture_cards_test: bool = False,
             skip_warnings: bool = False):
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

    :param gdrive-api-key: An API key for Google Drive. If you
    would prefer, you can set the $GDRIVE_API_KEY environment
    variable instead. (e.g. `export GDRIVE_API_KEY=value`)
    :type gdrive-api-key: str, optional

    :param skip_board_configuration_test: If set, skips the Board
    Configuration tests.
    :type skip_board_configuration_test: bool, optional

    :param skip-consistency-test: If set, skips the Board Consistency
    tests.
    :type skip-consistency-test: bool, optional

    :param skip-icon-test: If set, skips the Icon tests.
    :type skip-icon-test: bool, optional

    :param skip-max-paths-test: If set, skips the Max Paths tests.
    :type skip-max-paths-test: bool, optional

    :param skip_naming_convention_test: If set, skips the Naming
    Convention tests.
    :type skip_naming_convention_test: bool, optional

    :param skip_screenshots_test: If set, skips the Screenshot tests.
    :type skip_screenshots_test: bool, optional

    :param skip-venture-cards-test: If set, skips the Venture
    Card tests.
    :type skip-venture-cards-test: bool, optional

    :param skip-warnings: If set, skips tests resulting in
    "Warning" messages.
    :type skip-warnings: bool, optional
    """
    print("\n        -{========================>")
    print(f"        -{{  cs-board-tools {__version__}  }}-")
    print("        -{    board validation    }-")
    print("         <========================}-\n")

    bundles = []

    if gdrive_api_key is None:
        gdrive_api_key = os.environ.get("GDRIVE_API_KEY")

    if directory:
        files = get_files_recursively(directory)
        bundles = read_files(files)
        result = validate_bundle(
            bundles=bundles,
            gdrive_api_key=gdrive_api_key,
            skip_board_configuration_test=skip_board_configuration_test,
            skip_consistency_test=skip_consistency_test,
            skip_icon_test=skip_icon_test,
            skip_max_paths_test=skip_max_paths_test,
            skip_music_download_test=skip_music_download_test,
            skip_naming_convention_test=skip_naming_convention_test,
            skip_screenshots_test=skip_screenshots_test,
            skip_venture_cards_test=skip_venture_cards_test,
            skip_warnings=skip_warnings
        )
        print_bundles_validation_result(results=result)
    elif file:
        if file.endswith(".frb"):  # if it's a solo .frb file
            frb = read_frb(file)
            result = validate_board_file([frb])
            print_frbs_validation_result(results=result)
        elif file.endswith(".yaml"):  # if it's a solo .yaml file
            descriptor = read_yaml(file)
            result = validate_descriptor([descriptor], gdrive_api_key)
            print_descriptors_validation_result(results=result)
        # if it's anything else, it's a bundle. Handle accordingly:
        else:
            bundles = read_zip(file)
            if len(bundles) == 0:
                print("Please provide a valid input archive.")
                sys.exit(1)

            result = validate_bundle(
                bundles=bundles,
                gdrive_api_key=gdrive_api_key,
                skip_board_configuration_test=skip_board_configuration_test,
                skip_consistency_test=skip_consistency_test,
                skip_icon_test=skip_icon_test,
                skip_max_paths_test=skip_max_paths_test,
                skip_music_download_test=skip_music_download_test,
                skip_naming_convention_test=skip_naming_convention_test,
                skip_screenshots_test=skip_screenshots_test,
                skip_venture_cards_test=skip_venture_cards_test,
                skip_warnings=skip_warnings
            )
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
