"""The queries.frb module contains functions that assist in querying
Fortune Avenue-compatible .frb files.
"""

from .squaretype import (
    are_square_types_present,
    is_square_type_present
)

__all__ = [
    are_square_types_present.__name__,
    is_square_type_present.__name__
]
