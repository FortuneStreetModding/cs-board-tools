"""The Bundle dataclass and its constructor live here.
"""
from dataclasses import dataclass, field
from cs_board_tools.schema.frb import BoardFile
from cs_board_tools.schema.descriptor import (
    AuthorInfo,
    CustomMusic,
    MapDescriptor,
    Name
)


@dataclass
class Bundle:
    """
    A Bundle is an object that holds the data that is,
    on the disk, held across the Fortune Avenue .frb file,
    the Map Descriptor .yaml file, and the other accompanying files.
    """
    authors: list[AuthorInfo]
    background: str = field(default="")
    descriptor: MapDescriptor = field(default_factory=MapDescriptor)
    frb_filenames: list[str] = field(default_factory=list)
    frbs: list[BoardFile] = field(default_factory=list)
    icon: str = field(default="")
    music: CustomMusic = field(default_factory=CustomMusic)
    name: Name = field(default_factory=Name)
    screenshots: list[str] = field(default_factory=list)

    def __init__(self):
        self.descriptor = MapDescriptor()
        self.music = CustomMusic()
        self.name = Name()
