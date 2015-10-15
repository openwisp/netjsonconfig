from collections import OrderedDict


def merge_config(template, config):
    """
    merge two dicts `template` and `config`
    values of `config` are merged in values present in `template`
    lists present in `config` will be added to lists in `template`
    """
    for key, value in config.items():
        if isinstance(value, dict):
            # get node or create one
            node = template.setdefault(key, {})
            merge_config(node, value)
        elif isinstance(value, list) and isinstance(template.get(key), list):
            template[key] += value
        else:
            template[key] = value

    return template


def sorted_dict(dictionary):
    return OrderedDict(sorted(dictionary.items()))
