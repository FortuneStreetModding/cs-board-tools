"""A set of libraries designed to help users interact with
Custom Street user content through Python. We hope you love it!
If you're aware of any bugs, or have ideas for future functionality,
feel free to let us know by raising an Issue in the Github repository,
or by creating a thread in the #ideas forum of the Custom Street Discord
server.

`cs-board-tools`, like all of our other projects, is fully open-source.
As such, if you are a software developer and would like to help out,
we'd love to have you!
"""

from .io import (
    read_files,
    read_frb,
    read_yaml,
    read_zip
)
from .validation import (
    validate_bundle,
    validate_board_file,
    validate_descriptor
)

__all__ = [
    read_files.__name__,
    read_frb.__name__,
    read_yaml.__name__,
    read_zip.__name__,
    validate_bundle.__name__,
    validate_board_file.__name__,
    validate_descriptor.__name__,
]
