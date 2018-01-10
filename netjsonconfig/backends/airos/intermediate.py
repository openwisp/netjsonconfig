from six import string_types
from six.moves import reduce


def flatten(elements):
    """
    Flatten a list
    elements :: List
    return List
    """
    if elements is not list:
        return elements
    else:
        return reduce(lambda x, y: x + flatten(y), elements, [])


def shrink(configuration):
    """
    configuration :: Dict
    return Dict
    """
    temp = {}
    for key, value in configuration.items():
        if isinstance(value, string_types) or isinstance(value, int):
            temp[key] = value
        else:
            # reduce to atom list
            # as value could be dict or list
            # enclose it in a flattened list
            for child in intermediate_to_list(flatten([value])):
                for child_key, child_value in child.items():
                    nested_key = '{key}.{subkey}'.format(key=key, subkey=child_key)
                    temp[nested_key] = child_value
    return temp


def intermediate_to_list(configuration):
    """
    Explore the configuration tree and flatten where
    possible with the following policy
    - list -> prepend the list index to every item key
    - dictionary -> prepend the father key to every key

    configuration :: List[Enum[Dict,List]]
    return List[Dict]

    >>> intermediate_to_list([
        {
            'spam': {
                'eggs': 'spam and eggs'
            }
        }
    ])
    >>>
    [{
        'spam.eggs' : 'spam and eggs'
    ]}

    >>> intermediate_to_list([
        {
            'spam': {
                'eggs': 'spam and eggs'
            }
        },
        [
            {
                'henry': 'the first'
            },
            {
                'jacob' : 'the second'
            }
        ]
    ])
    >>>
    [
        {
            'spam.eggs' : 'spam and eggs'
        },
        {
            '1.henry' : 'the first'
        },
        {
            '2.jacob' : 'the second'
        }
    ]
    """

    result = []

    for element in configuration:
        if isinstance(element, list):
            for index, el in enumerate(element):
                temp = {}
                for key, value in el.items():
                    temp['{i}.{key}'.format(i=index + 1, key=key)] = value
                result = result + intermediate_to_list([temp])

        elif isinstance(element, dict):
            temp = {}
            temp.update(shrink(element))
            result.append(temp)

        else:
            raise Exception('malformed intermediate representation')

    return result
