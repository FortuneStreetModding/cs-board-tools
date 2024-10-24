# Getting Started
Getting started with `cs-board-tools` is easy. Simply make sure Python 3.10 or newer is installed, then install `cs-board-tools` with pip, and you're ready to go!

## Prerequisites
`cs-board-tools` requires Python 3.10 or higher.

### Installation
`cs-board-tools` can be installed via pip in the terminal, or it can be specified in your project's `pyproject.toml` or `requirements.txt` file.
::::{tab-set}

:::{tab-item} via pip
```bash
pip install git+https://github.com/FortuneStreetModding/cs-board-tools
```
:::
:::{tab-item} via pyproject.toml
```toml
dependencies = [
  'cs-board-tools @ git+https://github.com/FortuneStreetModding/cs-board-tools.git'
]
```
:::
:::{tab-item} via requirements.txt
```bash
cs-board-tools @ git+https://github.com/FortuneStreetModding/cs-board-tools@main
```
:::
::::

## Loading a Bundle
In its simplest form, loading a bundle is as easy as passing a filename into a Python function.
```py
from cs_board_tools.io import read_zip


def load_zip_bundle():
    filename="WiiU.zip"
    bundles = read_zip(filename)
    board_bundle = bundles[0]
```
## Validating a Bundle
Then, with that `board_bundle` object from the previous step, all you have to do is pass it into the `validate_board_bundle` function to validate it. What you will get in return is a **ValidationResultBundle** object, containing all of the results of the tests.

```py
results = validate_board_bundle(board_bundle)

percent = results.success_count / results.total_count
print(
    f"{results.success_count} out of {results.total_count} "
    f"({percent}%) tests were successful."
)
```

## Usage from the Terminal
`cs-board-tools` can be used from the terminal to display information about Fortune Avenue-compatible `.frb` files, CSMM-compatible `.yaml` descriptor files, or board bundles either via `.zip` archive files, or by reading in files from a directory. It has two main commands: `display` and `validate`, and they work the same regardless of the type of input file you are passing in.

### Display Bundle from Directory
```bash
cs-board-tools display -d .
```

### Validate Bundle from File
```bash
cs-board-tools validate -f SomeAwesomeBundle.zip
```

These work the other way around as well: you can validate bundles from directory, just as you can display bundles from file.

## Further Reading

For more information about using `cs-board-tools`, including further details about the data returned in the **ValidationResultBundle** object, please see the [Usage](#usage) section.

For a more traditional API-style documentation, please see the [API Reference](#api) section.
