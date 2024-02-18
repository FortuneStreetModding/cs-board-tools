# cs-board-tools | CLI

## Summary
This module holds code to support invoking both loading (display) and validating boards via the CLI. The following different types of inputs can be used:

* solo frbs
* solo yaml board descriptors
* zip file archives
* directories

You can also load multiple boards in a single zip file, or the files for multiple boards in that same list. These functions just return all the data you ask for, whether you provide the files for one or fifty board bundles.

## Table of Contents
* [Summary](#summary)
* [Table of Contents](#table-of-contents)
* [How to Use](#how-to-use)
  * [Displaying Boards](#displaying-boards)
  * [Validating](#validating)

## How to Use
### Displaying Boards
#### From a directory
In this example, the `-d` flag tells `cs-board-tools` to search a directory, and `.` is the path, which represents the current directory. This command will work if your current working directory is inside a board Bundle's folder.
```bash
cs-board-tools display -d .
```
#### From a .zip file archive
The `-f` flag tells cs-board-tools to load from a file, and `WiiU.zip` is that file. This works with `.frb` and `.yaml` files too, though the amount of data displayed will be reduced depending on the data that is present in either file. Loading Board Bundles from directory or `.zip` file will always show the largest amount of data.
```bash
cs-board-tools display -f WiiU.zip
```
### Validating
The same ideas extend to Validating -- the `-d` flag loads from directory, and the `-f` flag loads from file.
```bash
cs-board-tools validate -d .
```

```bash
cs-board-tools validate -f WiiU.zip
```
