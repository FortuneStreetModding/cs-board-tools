# cs-board-tools: Validation

## Summary
This module handles validation checks.

## Table of Contents
* [Summary](#summary)
* [Table of Contents](#table-of-contents)
* [How to Use](#how-to-use)
* [Object Reference](#object-reference)
  * [ValidationResultBundle](#validationresultbundle)
    * [Attributes](#attributes)
  * [ValidationResult](#validationresult)
    * [Attributes](#attributes-1)
  * [CheckResult](#checkresult)


## How to Use
To validate a board, all you need are a few lines of Python. Two to import the functions, and two to call them. One function is to load the bundles, and the other is to validate them.
```py
from cs_board_tools.io import read_zip
from cs_board_tools.validation import validate_board_bundle

bundles = read_zip("WiiU.zip")    # load the bundles
result = validate_bundle(bundles) # validate them
```

Note that it's plural -- the `read_zip` and `validate_bundle` functions return a `list[Bundle]` no matter how many items passed in. Why is that? It's because you can actually zip any number of bundles together, so the application has no way to know in advance what you're feeding it. So if your `.zip` file contains only one bundle, as this example illustrates, you'll simply receive lists with a length of 1. Doing it this way means that `bundles[0]` can be reliably accessed, and you don't have to do an if-else dance just to see whether it's a list or not.

Please note that other functions besides `read_zip()` and `validate_bundle()` exist in those namespaces as well. There are functions for loading and validating solo `.frb` and `.yaml` files, and validating from directory as well. They largely work the same. As such, I won't go over them here.

| function            | description             |
|---------------------|-------------------------|
| `read_board_file()` | Reads an .frb.          |
| `read_descriptor()` | Reads a .yaml.          |
| `read_files()`      | Reads from a directory. |
| `read_zip()`        | Reads a .zip.           |

| function                | description             |
|-------------------------|-------------------------|
| `validate_board_file()` | Reads an .frb.          |
| `validate_bundle()`     | Reads from a directory. |
| `validate_descriptor()` | Reads a .yaml.          |

For more information, please see the cs-board-tools documentation, which I will link when it is posted.

### Object Attributes
Below are the objects returned by the validation functions.
* `ValidationResultBundle` is the top-level object, which holds general validation data as well as summed results, such as error counts and messages.
* `ValidationResult` is stored in `ValidationResultBundle.boards`, which is a list. This object represents the results of one board's validation checks. This way, if your input contained multiple bundles, you could validate them all simultaneously. This `ValidationResult` object contains a number of attributes of `CheckResult` type, which is the next and lowest-level of the results.
* `CheckResult` represents the results of a specific check, for a specific board. These objects are contained across a wide range of attributes on the `ValidationResult` object.

The attributes for these objects are listed below in full.

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
| consistency            |      CheckResult       | The results of the frb/yaml consistency check.                |
| door                   |      CheckResult       | The results of the doors and dice check.                      |
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
| status                 | str       | `OK`, `WARNING`, `ERROR`, or `SKIPPED`                                                              |
| error_messages         | list[str] | A list of `error` messages.                                                                         |
| informational_messages | list[str] | A list of `informational` messages.                                                                 |
| warning_messages       | list[str] | A list of `warning` messages.                                                                       |
| data                   | any       | Can store anything you would like. Currently only used by the Max Paths check to return that value. |

## Further Reading
For further information, please see the Documentation...which will be linked when it's up.
