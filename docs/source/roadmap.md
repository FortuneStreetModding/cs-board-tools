# Roadmap
Please take this page with a grain of salt. Forward-looking statements are always uncertain. But this page will reflect a best effort at prioritizing things that folks will actually want to use.

| Projected Date | Feature                        | Additional Notes                                             |
|----------------|--------------------------------|--------------------------------------------------------------|
|   2024-03-31   | Queries libraries              | Pre-written functions to handle common queries.              |
|   2024-06-30   | Write support                  | Allow saving changes to bundles.                             |
|   2024-06-30   | Support for generating objects | Allow generating new bundles from Python and CLI.            |
|   2024-07-31   | BRSAR support                  | Allow querying and modifying items in .brsar files.          |
|   2024-12-31   | Support for an input language  | Allow an input document to describe all the desired changes. |

## Changelog
|  Release Version  | Date Released |  Feature or Bugfix                                                                                |
|-------------------|---------------|---------------------------------------------------------------------------------------------------|
|       1.0.0       |   2024-02-18  | Initial release.                                                                                  |
|    pre-release    |   2024-02-02  | Added naming convention checks that ensure filename case is consistent.                           |
|    pre-release    |   2024-02-02  | Added support for reading and storing all filenames in bundle for easier querying.                |
|    pre-release    |   2024-01-20  | Migrated to new Python library backend (ruamel), as it seems to produce more compatible results.  |
|    pre-release    |   2023-12-14  | Implemented unit testing to help detect any regressions before shipping.                          |
|    pre-release    |   2023-12-11  | Added support for validating solo .frb and .yaml files.                                           |
|    pre-release    |   2023-12-11  | Added CLI support.                                                                                |

## How do I suggest an item for the roadmap?
The best way to do so is to raise an [Issue](https://github.com/fortunestreetmodding/cs-board-tools/issues) in the project's Github repository. This will make it visible so others can comment on it and 👍 your post.
