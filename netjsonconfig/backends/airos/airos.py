from six import string_types
from six.moves import reduce

from ..base.backend import BaseBackend
from .converters import (Aaa, Bridge, Discovery, Dyndns, Ebtables, Gui, Httpd,
                         Igmpproxy, Iptables, Netconf, Netmode, Ntpclient,
                         Pwdog, Radio, Resolv, Route, Snmp, Sshd, Syslog,
                         System, Telnetd, Update, Users, Vlan, Wireless,
                         Wpasupplicant)
from .renderers import AirOsRenderer
from .schema import schema


class AirOs(BaseBackend):
    """
    AirOS backend
    """
    # backend schema validator
    schema = schema
    # converters from configuration
    # dictionary to intermediate representation
    converters = [
            Aaa,
            Bridge,
            Discovery,
            Dyndns,
            Ebtables,
            Gui,
            Httpd,
            Igmpproxy,
            Iptables,
            Netconf,
            Netmode,
            Ntpclient,
            Pwdog,
            Radio,
            Resolv,
            Route,
            Snmp,
            Sshd,
            Syslog,
            System,
            Telnetd,
            Update,
            Users,
            Vlan,
            Wireless,
            Wpasupplicant,
    ]
    # the environment where airos
    # templates lives
    env_path = 'netjsonconfig.backends.airos'
    renderer = AirOsRenderer

    def to_intermediate(self):
        super(AirOs, self).to_intermediate()
        for k, v in self.intermediate_data.items():
            self.intermediate_data[k] = [x for x in flatten(intermediate_to_list(v)) if x != {}]


def flatten(elements):
    """
    Flatten a list
    """
    if elements is not list:
        return elements
    else:
        return reduce(lambda x, y: x + flatten(y), elements, [])


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
            result = result + intermediate_to_list(list(enumerate(element)))

        elif isinstance(element, tuple):
            (index, config) = element
            # update the keys to prefix the index
            temp = {}
            for key, value in config.items():
                # write the new key
                temp['{i}.{key}'.format(i=index + 1, key=key)] = value
            config = temp
            # now the keys are updated with the index
            # reduce to atoms the new config
            # by recursively calling yourself
            # on a list containing the new atom
            result = result + intermediate_to_list([config])

        elif isinstance(element, dict):
            temp = {}
            for key, value in element.items():
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

            # now it is atomic, append it to
            result.append(temp)

        else:
            raise Exception('malformed intermediate representation')

    return result
