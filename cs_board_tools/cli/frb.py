"""These are functions which handle displaying and validating
Fortune Avenue-compatible .frb files from the terminal.
"""
import sys
from prettytable import PrettyTable

from ..schema.frb import BoardFile
from ..schema.validation import ValidationResultBundle


def print_frbs(frbs: list[BoardFile]):
    """Prints a list of Fortune Avenue-compatible .frb files to the terminal.
    Uses PrettyTable to print nicely-formatted ASCII tables.

    Args:
        bundles (list[Bundle]): The Bundles you would like to print.
    """
    if len(frbs) == 0:
        print("Please provide a valid input.")
        sys.exit(1)

    found = f"| Found: {len(frbs)} boards. Processing for display. |"
    print("=" * int(len(found)))
    print(found)
    print("=" * int(len(found)))

    for f in frbs:
        title = "Unknown .frb"
        b_table = PrettyTable()
        b_table.title = title
        b_table.field_names = ["Attribute", "Value or Count"]
        b_table.add_row(["Squares", len(f.squares)])
        b_table.add_row(["States", len(frbs)])
        b_table.add_row([" ", " "])
        b_table.add_row(["Base Salary", f.board_info.base_salary])
        b_table.add_row(["Initial Cash", f.board_info.initial_cash])
        b_table.add_row(["Max Dice Roll", f.board_info.max_dice_roll])
        b_table.add_row(["Salary Increment", f.board_info.salary_increment])
        b_table.add_row(["Target Amount", f.board_info.target_amount])
        b_table.add_row([" ", " "])

        b_table.align["Attribute"] = "r"
        b_table.align["Value or Count"] = "l"
        print(b_table)


def print_frbs_validation_result(results: ValidationResultBundle):
    """Prints data from a ValidationResultBundle object to the terminal, when that
    object contains results from an frb-only validation test.

    Args:
        results (ValidationResultBundle): The results you would like to print.
    """

    found = (
        f"| Found: {len(results.boards)} board(s). "
        "Processing for display. |"
    )
    print("=" * int(len(found)))
    print(found)
    print("=" * int(len(found)))

    # put things that differ by language up here

    error_messages = []
    informational_messages = []
    warning_messages = []

    for r in results.boards:
        title = "Validation Results for Unknown .frb"
        b_table = PrettyTable()
        b_table.title = title
        b_table.field_names = ["Attribute", "Value or Count"]
        b_table.add_row(["Max Paths", r.paths])
        b_table.add_row(["---", "---"])
        b_table.add_row(["Doors and Dice", r.door.status])
        b_table.add_row(["Max Paths", r.max_paths.status])

        b_table.align["Attribute"] = "r"
        b_table.align["Value or Count"] = "l"

        error_messages.extend(r.error_messages.copy())
        informational_messages.extend(r.informational_messages.copy())
        warning_messages.extend(r.warning_messages.copy())

        print(b_table)
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
