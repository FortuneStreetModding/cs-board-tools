"""Entry-point functions for loading Map Descriptor .yaml files and
the schema for those files live here.
"""
from pathlib import Path
import requests

from cs_board_tools.schema.descriptor import (
    build_map_descriptor_object,
    MapDescriptor
)


def read_yaml(file_path: Path) -> MapDescriptor:
    """
    Reads a Map Descriptor .yaml file into a Python object.

    :param file_path: A Path object representing the .yaml file's filename,
        and -- if it's in a different directory than your current shell --
        its relative path as well.
    :type file_path: Path

    :return: Returns a MapDescriptor file representing the data from the
        .yaml file.
    :rtype: MapDescriptor
    """
    return build_map_descriptor_object(file_path)


def read_yaml_schema() -> str:
    """
    Returns the schema for Map Descriptor .yaml files.

    :return: Returns schema. You can find this schema file in the
        fortunestreetmodding.github.io repository.
    :rtype: str
    """
    url = "http://fortunestreetmodding.github.io/schema/mapdescriptor.json"
    res = requests.get(url)
    if not res.ok:
        return
    return res.json()
