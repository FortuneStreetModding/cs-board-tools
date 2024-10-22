# Usage
This library can be used in multiple ways. You can load `.frb` board files, `.yaml` descriptor files, and `.zip` bundle files respectively. You can also load bundles from a directory of files, and you can run validation tests on any or all of these files, as well.

## Loading Boards

You can use this library to load CSMM-compatible board bundles, as well as Fortune Avenue-compatible `.frb` files, and CSMM-comatible`.yaml` descriptor files. This guide will walk you through all of them, so feel free to skip to the section most relevant to you.

### How to Load a Board
The method will differ slightly depending on the files available to you.

#### .zip board bundle file
::::{tab-set}

:::{tab-item} Python 3.10+
```py
from cs_board_tools.io import read_zip


def test_reading_zip_file():
    filename="WiiU.zip"
    bundles = read_zip(filename)
    board_bundle = bundles[0]
```
:::
::::
The `read_zip` function returns a list of Bundles. In the example above, that list would contain only one Bundle (for the Wii U board), but you could, in theory, zip up a number of boards together and get results for all of them at the same time.

#### a list of files in a directory
::::{tab-set}

:::{tab-item} Python 3.10+
```py
from cs_board_tools.io import read_files


def reading_list_of_files():
    files=["WiiU.yaml", "WiiU.png", "WiiU.webp", "WiiU.frb"]
    bundles = read_files(files)
    board_bundle = bundles[0]
```
:::
::::
The `read_files` function also returns a list of Bundles.

#### .yaml file only
::::{tab-set}

:::{tab-item} Python 3.10+
```py
from cs_board_tools.io import read_yaml


def reading_yaml():
    filename="WiiU.yaml"
    descriptor = read_yaml(f"./tests/artifacts/{filename}")
```
:::
::::
When loading a `.yaml` descriptor file, the object returned is a MapDescriptor object, rather than a full bundle. As such, the `read_yaml` function returns just that.

#### .frb file only
::::{tab-set}

:::{tab-item} Python 3.10+
```py
from cs_board_tools.io import read_frb


def reading_frb():
    filename="WiiU.frb"
    frb = read_frb(f"./tests/artifacts/{filename}")
```
:::
::::
The `read_frb` function returns a BoardFile object, representing only the data that is stored in the `.frb` file directly.


## Validating Boards
Validating boards is incredibly simple!

### How to Validate a Board
To validate a board, you must first load it. Please see the Loading Boards section for more information. Once you have your list of Bundles, you can pass them in for validation like so:
::::{tab-set}

:::{tab-item} Python 3.10+
```py
from cs_board_tools.io import read_zip
from cs_board_tools.validation import validate_board_bundle

filename = "WiiU.zip"
bundles = read_zip(filename)          # load the bundle
result = validate_board_bundle(bundles) # validate it
```
:::
::::
Now, you can get all of the validation details from that object.

::::{tab-set}

:::{tab-item} Python 3.10+
```py
# print any error messages
print(result.error_messages)

# print only the first error message
print(result.error_messages[0])

# there are also lists for warnings and informational messages, too.
print(result.informational_messages)
print(result.warning_messages)

#print the number of tests with errors or warnings
print(result.issue_count)

# print the number of successful tests
print(result.success_count)

# print the status of the Door and Dice check
print(result.boards[].door.status)
```
:::
::::
The next section contains charts showing in detail the attributes available in this `result` **ValidationResultBundle** object, as well as the attributes available in the objects nested within. These objects give you access to all of the result data from the validation operation.

### Object Attributes

#### ValidationResultBundle (top-level object)

|  attribute             |  type                  |  description                                             |
|------------------------|------------------------|----------------------------------------------------------|
| error_count            |          int           | Number of errors.                                        |
| warning_count          |          int           | Number of warnings.                                      |
| issue_count            |          int           | (errors + warnings)                                      |
| success_count          |          int           | Number of successful tasks.                              |
| total_count            |          int           | Total tasks. (successful and not)                        |
| error_messages         |       list[str]        | All error messages in list form.                         |
| informational_messages |       list[str]        | All informational messages in list form.                 |
| warning_messages       |       list[str]        | All warning messages in list form.                       |
| boards                 | list[ValidationResult] | List of objects representing the results for each board. |


#### ValidationResult (board-level object)

|  attribute             |  type                  |  description                                                  |
|------------------------|------------------------|---------------------------------------------------------------|
| board_name             |          str           | The name of the board that the validation results pertain to. |
| paths                  |          int           | The maximum number of paths for any square on the board.      |
| error_count            |          int           | Number of errors.                                             |
| warning_count          |          int           | Number of warnings.                                           |
| issue_count            |          int           | (errors + warnings)                                           |
| success_count          |          int           | Number of successful tasks.                                   |
| total_count            |          int           | Total tasks. (successful and not)                             |
| board_configuration    |      CheckResult       | The results of the Board Configuration checks.                |
| consistency            |      CheckResult       | The results of the frb/yaml consistency check.                |
| icon                   |      CheckResult       | The results of the Board Icon check.
| max_paths              |      CheckResult       | The results of the max paths check.                           |
| music_download         |      CheckResult       | The results of the music download check.                      |
| naming                 |      CheckResult       | The results of the naming convention check.                   |
| screenshots            |      CheckResult       | The results of the max paths check.                           |
| venture                |      CheckResult       | The results of the venture card check.                        |
| yaml                   |      CheckResult       | The results of the yaml validation check.                     |
| error_messages         |       list[str]        | All error messages in list form.                              |
| informational_messages |       list[str]        | All informational messages in list form.                      |
| warning_messages       |       list[str]        | All warning messages in list form.                            |

#### CheckResult (individual check-level)

|  attribute             | type      |  description                                                                                        |
|------------------------|-----------|-----------------------------------------------------------------------------------------------------|
| data                   | any       | Can store anything you would like. Currently only used by the Max Paths check to return that value. |
| status                 | str       | `OK`, `WARNING`, `ERROR`, or `SKIPPED`                                                              |
| error_messages         | list[str] | A list of `error` messages.                                                                         |
| informational_messages | list[str] | A list of `informational` messages.                                                                 |
| warning_messages       | list[str] | A list of `warning` messages.                                                                       |


## CLI
`cs-board-tools` can be used from the terminal to display information about Fortune Avenue-compatible `.frb` files, CSMM-compatible `.yaml` descriptor files, or Board Bundles either via `.zip` archive files, or by reading in files from a directory. It has two main commands: `display` and `validate`, and they work the same regardless of the type of input file you are passing in.

### Displaying
::::{tab-set}

:::{tab-item} directory
```bash
cs-board-tools display -d .
```
:::
:::{tab-item} frb
```bash
cs-board-tools display -f SomeAwesomeBoard.frb
```
:::
:::{tab-item} yaml
```bash
cs-board-tools display -f SomeAwesomeBoardDescriptor.yaml
```
:::
:::{tab-item} zip
```bash
cs-board-tools display -f SomeAwesomeBundle.zip
```
:::
::::

### Validating
::::{tab-set}

:::{tab-item} directory
```bash
cs-board-tools validate -d .
```
:::
:::{tab-item} frb
```bash
cs-board-tools validate -f SomeAwesomeBoard.frb
```
:::
:::{tab-item} yaml
```bash
cs-board-tools validate -f SomeAwesomeBoardDescriptor.yaml
```
:::
:::{tab-item} zip
```bash
cs-board-tools validate -f SomeAwesomeBundle.zip
```
:::
::::

The information returned will differ depending on what type of file was passed in. For example, a screenshot test cannot be performed against a solo .frb file as the information needed to run that test lives in the `.yaml` descriptor file. Only Bundles are able to display the full range of information, and perform all validation tests, as they contain the .frb, the .yaml, and the other related files too.

#### Optional Flags
The Validation function supports a number of optional flags to change the behavior of the tests. These flags are detailed in the table below for easy reference.

| short flag | long flag                         |  description                                                          |
|------------|-----------------------------------|-----------------------------------------------------------------------|
|   `-g`     | `--gdrive-api-key`                | Allows specifying a Google Drive API key for the Music Download test. |
|   `-sbc`   | `--skip-board-configuration-test` | Skips the Board Configuration tests.                                  |
|   `-sct`   | `--skip-consistency-test`         | Skips the Consistency tests.                                          |
|   `-sdt`   | `--skip-music-download-test`      | Skips the Music Download tests.                                       |
|   `-sit`   | `--skip-icon-test`                | Skips the Board Icon tests.                                           |
|   `-snt`   | `--skip-naming-convention-test`   | Skips the Naming Convention tests.                                    |
|   `-spt`   | `--skip-max-paths-test`           | Skips the Max Paths tests.                                            |
|   `-sst`   | `--skip-screenshot-test`          | Skips the Screenshot tests.                                           |
|   `-svt`   | `--skip-venture-card-test`        | Skips the Venture Card tests.                                         |
|   `-sw`    | `--skip-warnings`                 | Silences warnings from output.                                        |
