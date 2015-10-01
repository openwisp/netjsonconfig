from collections import OrderedDict


def merge_dict(source, destination):
    """
    merge two dicts `source` and `destination`
    `destination` overwrites `source`
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge_dict(value, node)
        else:
            destination[key] = value

    return destination


def sorted_dict(dictionary):
    return OrderedDict(sorted(dictionary.items()))
