from collections import OrderedDict
from copy import deepcopy


def merge_config(template, config):
    """
    Merges ``config`` on top of ``template``.

    Conflicting keys are handled in the following way:

    * simple values (eg: ``str``, ``int``, ``float``, ecc) in ``config`` will
      overwrite the ones in ``template``
    * values of type ``list`` in both ``config`` and ``template`` will be summed
      in order to create a list which contains elements of both
    * values of type ``dict`` will be merged recursively

    :param template: template ``dict``
    :param config: config ``dict``
    :returns: merged ``dict``
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
