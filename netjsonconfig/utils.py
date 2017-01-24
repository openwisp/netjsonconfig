import re
from collections import OrderedDict
from copy import deepcopy

import six


def merge_config(template, config):
    """
    Merges ``config`` on top of ``template``.

    Conflicting keys are handled in the following way:

    * simple values (eg: ``str``, ``int``, ``float``, ecc) in ``config`` will
      overwrite the ones in ``template``
    * values of type ``list`` in both ``config`` and ``template`` will be
      merged using to the ``merge_list`` function
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
            result[key] = merge_list(result[key], value)
        else:
            result[key] = value
    return result


def merge_list(list1, list2, identifiers=['name', 'config_value', 'id']):
    """
    Merges ``list2`` on top of ``list1``.

    If both lists contain dictionaries which have keys specified
    in ``identifiers`` which have equal values, those dicts will
    be merged (dicts in ``list2`` will override dicts in ``list1``).
    The remaining elements will be summed in order to create a list
    which contains elements of both lists.

    :param list1: list from template
    :param list2: list from config
    :returns: merged ``list``
    """
    dict_map = {'list1': OrderedDict(), 'list2': OrderedDict()}
    counter = 1
    for list_ in [list1, list2]:
        container = dict_map['list{0}'.format(counter)]
        for el in list_:
            # merge by internal python id by default
            key = id(el)
            # if el is a dict, merge by keys specified in ``identifiers``
            if isinstance(el, dict):
                for id_key in identifiers:
                    if id_key in el:
                        key = el[id_key]
                        break
            container[key] = deepcopy(el)
        counter += 1
    merged = merge_config(dict_map['list1'], dict_map['list2'])
    return list(merged.values())


def sorted_dict(dictionary):
    return OrderedDict(sorted(dictionary.items()))


var_pattern = re.compile(r'\{\{\s*([a-zA-Z0-9_]*)\s*\}\}')


def evaluate_vars(data, context={}):
    """
    Evaluates variables in ``data``

    :param data: data structure containing variables, may be
                 ``str``, ``dict`` or ``list``
    :param context: ``dict`` containing variables
    :returns: modified data structure
    """
    if isinstance(data, (dict, list)):
        if isinstance(data, dict):
            loop_items = data.items()
        elif isinstance(data, list):
            loop_items = enumerate(data)
        for key, value in loop_items:
            data[key] = evaluate_vars(value, context)
    elif isinstance(data, six.string_types):
        vars_found = var_pattern.findall(data)
        for var in vars_found:
            var = var.strip()
            # if found multiple variables, create a new regexp pattern for each
            # variable, otherwise different variables would get the same value
            # (see https://github.com/openwisp/netjsonconfig/issues/55)
            if len(vars_found) > 1:
                pattern = r'\{\{(\s*%s\s*)\}\}' % var
            # in case of single variables, use the precompiled
            # regexp pattern to save computation
            else:
                pattern = var_pattern
            if var in context:
                data = re.sub(pattern, context[var], data)
    return data


class _TabsMixin(object):  # pragma: nocover
    """
    mixin that adds _tabs method to test classes
    """
    def _tabs(self, string):
        """
        replace 4 spaces with 1 tab
        """
        return string.replace('    ', '\t')
