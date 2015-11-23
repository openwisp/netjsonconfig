from collections import OrderedDict
from copy import deepcopy


def merge_config(template, config):
    """
    merge two dicts `template` and `config`
    values of `config` are merged in values present in `template`
    lists present in `config` will be added to lists in `template`
    returns merged dict
    """
    result = template.copy()
    for key, value in config.items():
        if isinstance(value, dict):
            node = result.get(key, {})
            result[key] = merge_config(node, value)
        elif isinstance(value, list) and isinstance(result.get(key), list):
            result[key] = deepcopy(result[key]) + deepcopy(value)
        else:
            result[key] = value
    return result


def sorted_dict(dictionary):
    return OrderedDict(sorted(dictionary.items()))


class _TabsMixin(object):  # pragma: nocover
    """
    mixin that adds _tabs method to test classes
    """
    def _tabs(self, string):
        """
        replace 4 spaces with 1 tab
        """
        return string.replace('    ', '\t')
