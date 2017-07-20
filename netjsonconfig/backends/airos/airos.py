from ..base.backend import BaseBackend
from .converters import (Aaa, Bridge, Discovery, Dyndns, Ebtables, Gui, Httpd,
                         Igmpproxy, Iptables, Netconf, Netmode, Ntpclient,
                         Pwdog, Radio, Resolv, Route, Snmp, Sshd, Syslog,
                         System, Telnetd, Update, Users, Vlan, Wireless,
                         Wpasupplicant)
from .intermediate import flatten, intermediate_to_list
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
