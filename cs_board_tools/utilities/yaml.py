"""These functions handle loading yaml and yaml schema.
"""
import yaml
import json
import jsonschema
import requests
from cs_board_tools.schema.validation import CheckResult
from cs_board_tools.errors import process_log_messages

error_messages = []
informational_messages = []
warning_messages = []


def check_first_line(firstLine):
    """This function checks the very first line of the .yaml
        file to ensure it is "---"

    :param firstLine: The first line of the .yaml file.
    :type firstLine: str
    """
    global error_messages
    if not firstLine == "---":
        error_messages.append("YAML file first line must be ---")


def load_yaml(yaml_filename, yaml_schema):
    """This function handles loading the .yaml file from disk.

    :param yaml_filename: The filename of the .yaml file.
    :type yaml_filename: str

    :param yaml_schema: The schema of the Map Descriptor format.
    :type yaml_schema: str
    """
    results = CheckResult()
    global error_messages
    global informational_messages
    global warning_messages
    yamlContent = ""
    with open(yaml_filename, "r", encoding="utf8") as stream:
        # check the first line before anything else, so we
        # won't have to open the file twice. Then seek back
        # to the top.
        check_first_line(stream.readline().strip())
        stream.seek(0x0)

        try:
            yamlContent = yaml.safe_load(stream)
            board_dict = json.dumps(yamlContent)
            yamlContent = yaml.safe_load(board_dict)
            jsonschema.validate(yamlContent, yaml_schema)
        except yaml.YAMLError as exc:
            error_messages.append(str(exc))
        except jsonschema.ValidationError as err:
            error_messages.append(str(err))

    results.error_messages = error_messages.copy()
    results.informational_messages = informational_messages.copy()
    results.warning_messages = warning_messages.copy()

    if error_messages:
        results.status = "ERROR"
    elif warning_messages:
        results.status = "WARNING"
    else:
        results.status = "OK"

    process_log_messages(
        errors=error_messages.copy(),
        messages=informational_messages.copy(),
        warnings=warning_messages.copy()
    )

    error_messages.clear()
    informational_messages.clear()
    warning_messages.clear()

    return [yamlContent, results]


def load_yaml_schema():
    """This function handles loading the Map Descriptor yaml schema from
    the fortunestreetmodding.github.io repo.

    :return: Returns the schema JSON as a string.
    :rtype: str
    """
    url = "http://fortunestreetmodding.github.io/schema/mapdescriptor.json"
    res = requests.get(url)
    if not res.ok:
        return
    return res.json()
