"""These functions handle displaying and validating Board Bundles -- either
.zip file archives or full directories of files directly -- from the terminal.
"""
import sys
from prettytable import PrettyTable

from ..schema.bundle import Bundle
from ..schema.validation import ValidationResultBundle


def print_bundles(bundles: list[Bundle]):
    """
    Prints a list of Bundles to the terminal. Uses PrettyTable to
    print nicely-formatted ASCII tables.

    :param bundles: The Bundles you would like to print.
    :type bundles: list[Bundle]
    """

    if len(bundles) == 0 or len(bundles[0].frbs) == 0:
        print("Please provide a valid input.")
        sys.exit(1)

    found = f"| Found: {len(bundles)} bundle(s). Processing for display. |"
    print("=" * int(len(found)))
    print(found)
    print("=" * int(len(found)))

    for b in bundles:
        version = 1
        if b.descriptor.changelog:
            version = b.descriptor.changelog[0].version
        title = (
            f"{b.name.en} (v.{version}) by "
            f"{', '.join([a.name for a in b.authors])}"
        )
        b_table = PrettyTable()
        b_table.title = title
        b_table.field_names = ["Attribute", "Value or Count"]
        b_table.add_row(["Squares", len(b.frbs[0].squares)])
        b_table.add_row(["States", len(b.frbs)])
        b_table.add_row(["Screenshots", len(b.screenshots)])
        b_table.add_row(["Venture Cards", b.descriptor.venture_cards.count])
        b_table.add_row([" ", " "])
        b_table.add_row(["Base Salary", b.descriptor.base_salary])
        b_table.add_row(["Initial Cash", b.descriptor.initial_cash])
        b_table.add_row(["Max Dice Roll", b.descriptor.max_dice_roll])
        b_table.add_row(["Salary Increment", b.descriptor.salary_increment])
        b_table.add_row(["Target Amount", b.descriptor.target_amount])
        b_table.add_row([" ", " "])
        b_table.add_row(["Background", b.background])
        b_table.add_row(["Icon", b.icon])
        b_table.add_row([" ", " "])
        webp_filenames = b.filenames.webp
        if not webp_filenames:
            webp_filenames = ["None"]
        if len(b.frbs) > 1:
            b_table.add_row(["Board Files", ", \n".join(b.filenames.frb)])

            b_table.add_row([" ", " "])
            b_table.add_row(["Screenshot Files", ", \n".join(webp_filenames)])
        else:
            b_table.add_row(["Board File", f"{b.filenames.frb[0]}"])
            b_table.add_row(["Screenshot File", f"{webp_filenames[0]}"])

        b_table.align["Attribute"] = "r"
        b_table.align["Value or Count"] = "l"
        print(b_table)


def print_bundles_validation_result(results: ValidationResultBundle):
    """
    Prints data from a ValidationResultBundle object to the terminal.

    :param results: The results you would like to print.
    :type results: ValidationResultBundle
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

    for r in results.boards:
        b_table = PrettyTable()
        b_table.title = f"Validation Results for {r.board_name.en}"
        b_table.field_names = ["Attribute", "Value or Count"]
        b_table.add_row(["Max Paths", r.paths])
        b_table.add_row(["---", "---"])
        b_table.add_row(["Consistency", r.consistency.status])
        b_table.add_row(["Doors and Dice", r.door.status])
        b_table.add_row(["Max Paths", r.max_paths.status])
        b_table.add_row(["Music Download", r.music_download.status])
        b_table.add_row(["Naming Convention", r.naming.status])
        b_table.add_row(["Screenshots", r.screenshots.status])
        b_table.add_row(["Venture Cards", r.venture.status])
        b_table.add_row(["YAML Validation", r.yaml.status])

        b_table.align["Attribute"] = "r"
        b_table.align["Value or Count"] = "l"

        errs = [f"({r.board_name.en}) {e}" for e in r.error_messages]
        info = [f"({r.board_name.en}) {i}" for i in r.informational_messages]
        warn = [f"({r.board_name.en}) {w}" for w in r.warning_messages]
        error_messages.extend(errs)
        informational_messages.extend(info)
        warning_messages.extend(warn)

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
