"""The validation module contains code pertaining to specific
checks performed against Fortune Avenue-compatible .frb files,
Map Descriptor .yaml files, and Map Bundle objects to ensure their
compatiblility with Custom Street Map Manager (CSMM).
"""

from .consistency import check_consistency
from .doors import check_doors
from ..errors import (
    get_count,
    get_text,
    IssueType,
    reset_errors_and_warnings,
)

from .filesystem import check_for_screenshots
from .main import (
    validate_board_file,
    validate_bundle,
    validate_descriptor
)
from .music import check_music_download
from .naming import check_naming_convention
from .paths import check_max_paths
from .venture import check_venture_cards

__all__ = [
    check_consistency.__name__,
    check_doors.__name__,
    check_for_screenshots.__name__,
    check_music_download.__name__,
    check_naming_convention.__name__,
    check_max_paths.__name__,
    check_venture_cards.__name__,
    get_count.__name__,
    get_text.__name__,
    IssueType.__name__,
    reset_errors_and_warnings.__name__,
    validate_board_file.__name__,
    validate_bundle.__name__,
    validate_descriptor.__name__
]
