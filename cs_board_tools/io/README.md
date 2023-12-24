# cs-board-tools | Loading

## Summary
Use this module to load boards. You can load the following:

* solo frbs
* solo yaml board descriptors
* lists of files
* zip files

You can also load multiple boards in a single zip file, or the files for multiple boards in that same list. What gets returned is a list of Bundles, whether you provide the files for one or fifty board bundles.

## Table of Contents
* [Summary](#summary)
* [Table of Contents](#table-of-contents)
* [How to Use](#how-to-use)
  * [Loading a list of files](#loading-a-list-of-files)
  * [Loading .zip files](#loading-zip-files)
  * [Loading solo Fortune Avenue .frb files](#loading-solo-fortune-avenue-frb-files)
  * [Loading solo Map Descriptor .yaml files](#loading-solo-map-descriptor-yaml-files)

## How to Use
### Loading a list of files
```py
from cs_board_tools.io import read_files


def read_files():
    files = ["WiiU.yaml", "WiiU.png", "WiiU.webp", "WiiU.frb"]
    bundles = read_files(files)              # returns a list of board bundles
    board_bundle = bundles[0]                # get the bundle

    print(board_bundle.name.en)              # "Wii U"
    print(board_bundle.authors[0].name)      # "nikkums"
    print(len(board_bundle.frbs[0].squares)) # 55
```

### Loading zip files
```py
from cs_board_tools.io import read_zip


def test_reading_zip_file():
    filename="WiiU.zip"
    bundles = read_zip("filename")           # returns a list of board bundles
    board_bundle = bundles[0]                # get the bundle

    print(board_bundle.name.en)              # "Wii U"
    print(board_bundle.authors[0].name)      # "nikkums"
    print(len(board_bundle.frbs[0].squares)) # 55

```

### Loading solo Fortune Avenue .frb files
```py
from cs_board_tools.io import read_frb


def test_reading_frb():
    filename="WiiU.frb"
    frb_object = read_frb(filename)

    print(len(frb_object.squares)) # 55
```

### Loading solo Map Descriptor .yaml files
```py
from cs_board_tools.io import read_yaml


def test_reading_yaml():
    filename="WiiU.yaml"
    descriptor = read_yaml(filename)

    print(descriptor.name.en) # "Wii U"
    print(descriptor.authors[0].name) # "nikkums"
```
