import re

from six import string_types

from .converters import *
from .renderers import AirOS
from ..base.backend import BaseBackend
from .schema import schema

class AirOS(BaseBackend):
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
            Wpasupplicant
    ]

    # the environment where airos
    # templates lives
    env_path = 'netjsonconfig.backends.airos'

    renderer = AirOS

    def to_intermediate(self):
        super(AirOS, self).to_intermediate()
        for k, v in self.intermediate_data.items():
            self.intermediate_data[k] = [ x for x in flatten(intermediate_to_list(v)) if x != {}]

def flatten(xs):
    """
    Flatten a list
    """
    if xs is not list:
        return xs
    else:
        return reduce(lambda x,y: x + flatten(y), xs, [])

def intermediate_to_list(configuration):
    """
    Explore the configuration tree and flatten where
    possible with the following policy
    - list -> prepend the list index to every item key
    - dictionary -> prepend the father key to every key

    configuration :: list
    return list

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
            for k, v in config.items():
                # write the new key
                temp['{i}.{key}'.format(i=index + 1, key=k)] = v

            config = temp
            # now the keys are updated with the index
            # reduce to atoms the new config
            # by recursively calling yourself
            # on a list containing the new atom
            result = result + intermediate_to_list([config])

        elif isinstance(element, dict):
            temp = {}
            for k, v in element.items():
                if isinstance(v, string_types) or isinstance(v, int):
                    pass
                else:
                    # reduce to atom list
                    # as v could be dict or list
                    # enclose it in a flattened list
                    for son in intermediate_to_list(flatten([v])):

                        for sk, sv in son.items():
                            nested_key = '{key}.{subkey}'.format(key=k, subkey=sk)
                            temp[nested_key] = sv

            # now it is atomic, append it to 
            result.append(temp)

        else:
            raise Exception('malformed intermediate representation')

    return result
