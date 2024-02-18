# cs-board-tools

## Summary
This repository contains tools that are designed to allow Python developers to easily load and validate Custom Street board bundles.

## Table of Contents
* [Summary](#summary)
* [Table of Contents](#table-of-contents)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage as a Library](#usage-as-a-library)
  * [Loading a Board Bundle](#loading-a-board-bundle)
  * [Validating a Board Bundle](#validating-a-board-bundle)
* [Usage from the CLI](#usage-from-the-cli)
  * [Display from Directory](#display-from-directory)
  * [Validate from File](#validate-from-file)
* [Further Reading](#further-reading)

## Prerequisites
`cs-board-tools` requires Python 3.10 or higher.

## Installation
`cs-board-tools` can be installed via pip:
```py
pip install cs-board-tools
```
## Usage as a Library
### Loading a Board Bundle
In its simplest form, loading a board bundle is as easy as passing a filename into a Python function.
```py
from cs_board_tools.io import read_zip


def load_zip_bundle():
    filename="WiiU.zip"
    bundles = read_zip(filename)
    board_bundle = bundles[0]
```
### Validating a Board Bundle
Then, with that board_bundle object from the previous step, all you have to do is pass it into the `validate_board_bundle` function to validate it. What you will get in return is a **ValidationResultBundle** object, containing all of the results of the tests.

```py
results = validate_board_bundle(board_bundle)

percent = results.success_count / results.total_count
print(
    f"{results.success_count} out of {results.total_count} "
    f"({percent}%) tests were successful."
)
```

## Usage from the CLI
`cs-board-tools` can be used from the terminal to display information about Fortune Avenue-compatible `.frb` files, Map Descriptor `.yaml` files, or Board Bundles either via `.zip` archive files, or by reading in files from a directory. It has two main commands: `display` and `validate`, and they work the same regardless of the type of input file you are passing in.

### Display from Directory
```bash
cs-board-tools display -d .
```

### Validate from File
```bash
cs-board-tools validate -f SomeAwesomeBundle.zip
```

These work vice-versa as well: you can validate bundles from directory, just as you can display bundles from file.

## Further Reading
`cs-board-tools` has a rich set of documentation. (Add the link to it once it's generated and placed someplace.)
