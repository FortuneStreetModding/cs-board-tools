"""This module contains code which handles displaying and validating
MapDescriptor .yaml files from the terminal.
"""
import sys
from prettytable import PrettyTable

from ..schema.descriptor import MapDescriptor
from ..schema.validation import ValidationResultBundle


def print_descriptors(descriptors: list[MapDescriptor]):
    """Prints a list of MapDescriptors to the terminal. Uses PrettyTable to
    print nicely-formatted ASCII tables.

    Args:
        descriptors (list[MapDescriptor]): The MapDescriptor you
        would like to print.
    """
    if len(descriptors) == 0 or len(descriptors[0].frbs) == 0:
        print("Please provide a valid input.")
        sys.exit(1)

    found = (
        f"| Found: {len(descriptors)} descriptors(s)."
        " Processing for display. |"
    )
    print("=" * int(len(found)))
    print(found)
    print("=" * int(len(found)))

    for d in descriptors:
        version = 1
        if d.changelog:
            version = d.changelog[0].version
        title = (
            f"{d.name.en} (v.{version}) by "
            f"{', '.join([a.name for a in d.authors])}"
        )
        b_table = PrettyTable()
        b_table.title = title
        b_table.field_names = ["Attribute", "Value or Count"]
        b_table.add_row(["States", len(d.frbs)])
        b_table.add_row(["Venture Cards", d.venture_cards.count])
        b_table.add_row([" ", " "])
        b_table.add_row(["Base Salary", d.base_salary])
        b_table.add_row(["Initial Cash", d.initial_cash])
        b_table.add_row(["Max Dice Roll", d.max_dice_roll])
        b_table.add_row(["Salary Increment", d.salary_increment])
        b_table.add_row(["Target Amount", d.target_amount])
        b_table.add_row([" ", " "])
        b_table.add_row(["Background", d.background])
        b_table.add_row(["Icon", d.icon])

        b_table.align["Attribute"] = "r"
        b_table.align["Value or Count"] = "l"
        print(b_table)


def print_descriptors_validation_result(results: ValidationResultBundle):
    """Prints data from a ValidationResultBundle object to the terminal, when that
    object contains results from a descriptor-only validation test.

    Args:
        results (ValidationResultBundle): The results you would like to print.
    """
    found = (
        f"| Found: {len(results.boards)} boards(s). "
        "Processing for display. |"
    )
    print("=" * int(len(found)))
    print(found)
    print("=" * int(len(found)))

    # put things that differ by language up here

    error_messages = []
    informational_messages = []
    warning_messages = []

    gdrive_api_key_missing = False
    gdrive_message = ""
    for r in results.boards:
        b_table = PrettyTable()
        b_table.title = f"Validation Results for {r.board_name}"
        b_table.field_names = ["Attribute", "Value or Count"]
        b_table.add_row(["Music Download", r.music_download.status])
        b_table.add_row(["YAML Validation", r.yaml.status])

        b_table.align["Attribute"] = "r"
        b_table.align["Value or Count"] = "l"

        # If the Google Drive API key is missing, it's going
        # have an informational message in _each_ board. So
        # if you validate or display 49 boards, you'll get
        # 49 messages. For the purposes of the terminal output,
        # we'd like to only print this message once. So this
        # section focuses on making that happen.

        informational = []
        for message in r.informational_messages:
            if "Music Download test" in message:
                if not gdrive_api_key_missing:
                    gdrive_api_key_missing = True
                    gdrive_message = message
            else:
                informational.append(message)

        errs = [f"({r.board_name}) {e}" for e in r.error_messages]
        info = [f"({r.board_name}) {i}" for i in informational]
        warn = [f"({r.board_name}) {w}" for w in r.warning_messages]
        error_messages.extend(errs)
        informational_messages.extend(info)
        warning_messages.extend(warn)

        print(b_table)

    # Append the gdrive message, if the API key is missing
    if gdrive_api_key_missing:
        informational_messages.append(f"(General) {gdrive_message}")

    if results.issue_count == 0:
        print("No issues were found.")
    else:
        if results.error_count > 0:
            print(f"{results.error_count} error(s) were found:")
            print('\n'.join(error_messages))
        if results.warning_count > 0:
            print(f"\n{results.warning_count} warning(s) were found:")
            print('\n'.join(warning_messages))
    # informational messages should print whether the validation passed or not
    if len(results.informational_messages) > 0:
        print(
            f"\n{len(informational_messages)} "
            "informational message(s) were generated:"
        )
        print('\n'.join(informational_messages))
