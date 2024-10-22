def remove_null_entries_from_dict(dictionary: dict) -> dict:
    """
    Takes in a dictionary, and removes any null entries from it. This helps
    with normalization.

    :param dictionary: A Python dictionary object.
    :type dictionary: dict

    :return: Returns the dict with any null values removed.
    :rtype: dict
    """
    return dict(
        (k, v) for (k, v) in dictionary.items() if v is not None
    )
