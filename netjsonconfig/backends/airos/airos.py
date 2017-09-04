from collections import OrderedDict
from io import BytesIO
import six

from ..base.backend import BaseBackend
from .converters import (Aaa, Bridge, Dhcpc, Discovery, Dyndns, Ebtables, Gui,
                         Httpd, Igmpproxy, Iptables, Netconf, Netmode,
                         Ntpclient, Pwdog, Radio, Resolv, Route, Snmp, Sshd,
                         Syslog, System, Telnetd, Tshaper, Unms, Update, Users,
                         Vlan, Wireless, Wpasupplicant)
from .intermediate import flatten, intermediate_to_list
from .renderers import AirOsRenderer
from .schema import schema


def to_ordered_list(value):
    flattened = flatten(intermediate_to_list(value))
    return [OrderedDict(sorted(x.items())) for x in flattened if x != {}]


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
            Dhcpc,
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
            Tshaper,
            Unms,
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
            self.intermediate_data[k] = to_ordered_list(v)

    def generate(self):
        """
        Returns a ``BytesIO`` instance representing the configuration file

        :returns: in-memory configuration file, instance of ``BytesIO``
        """
        fl = BytesIO()
        fl.write(six.b(self.render()))
        fl.seek(0)
        return fl

    def write(self, name, path='./'):
        byte_object = self.generate()
        file_name = '{0}.cfg'.format(name)
        if not path.endswith('/'):
            path += '/'
        with open('{0}{1}'.format(path, file_name), 'wb') as out:
            out.write(byte_object.getvalue())
