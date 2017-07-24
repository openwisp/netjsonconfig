from unittest import TestCase

from netjsonconfig import AirOs
from netjsonconfig.backends.airos.airos import to_ordered_list
from netjsonconfig.backends.airos.converters import (Aaa, Bridge, Discovery,
                                                     Dyndns, Ebtables, Gui,
                                                     Httpd, Igmpproxy,
                                                     Iptables, Netconf,
                                                     Netmode, Ntpclient, Pwdog,
                                                     Radio, Resolv, Route,
                                                     Snmp, Sshd, Syslog,
                                                     System, Telnetd, Update,
                                                     Users, Vlan, Wireless,
                                                     Wpasupplicant)


class ConverterTest(TestCase):
    """
    Test case specific for intermediate configuration checks

    The intermediate configuration is a dict-like object with
    section names as keys and a list of configuration values
    as values
    """
    maxDiff = 1000

    def assertEqualConfig(self, a, b):
        """
        Test that the content of two list is the equal
        element wise

        This provides smaller, more specific, reports as it will trigger
        failure for differently ordered elements or the element
        content

        If an element fails the assertion will be the only one printed
        """
        for (a, b) in zip(a, to_ordered_list(b)):
            self.assertEqual(a, b)


class AaaAirOs(AirOs):
    """
    Mock backend with converter for radius authentication
    """
    converters = [
        Aaa,
    ]


class BridgeAirOs(AirOs):
    """
    Mock backend with converter for bridge interface
    """
    converters = [
        Bridge,
    ]


class DiscoveryAirOs(AirOs):
    """
    Mock backend with converter for network hardware discovery
    """
    converters = [
        Discovery,
    ]


class DyndnsAirOs(AirOs):
    """
    Mock backend with converter for dynamic dns capabilities
    """
    converters = [
        Dyndns,
    ]


class EbtablesAirOs(AirOs):
    """
    Mock backend with converter for ebtables
    """
    converters = [
        Ebtables,
    ]


class GuiAirOs(AirOs):
    """
    Mock backend with converter for web interface settings
    """
    converters = [
        Gui,
    ]


class HttpdAirOs(AirOs):
    """
    Mock backend with converter for web server
    """
    converters = [
        Httpd,
    ]


class IgmpproxyAirOs(AirOs):
    """
    Mock backend with converter for igmpproxy
    """
    converters = [
        Igmpproxy,
    ]


class IptablesAirOs(AirOs):
    """
    Mock backend with converter for iptables
    """
    converters = [
        Iptables,
    ]


class NetconfAirOs(AirOs):
    """
    Mock backend with converter for network configuration
    """
    converters = [
        Netconf,
    ]


class NetmodeAirOs(AirOs):
    """
    Mock backend with converter for network mode
    """
    converters = [
        Netmode,
    ]


class NtpclientAirOs(AirOs):
    """
    Mock backend with converter for ntp settings
    """
    converters = [
        Ntpclient,
    ]


class PwdogAirOs(AirOs):
    """
    Mock backend with converter for ping watchdog settings
    """
    converters = [
        Pwdog,
    ]


class RadioAirOs(AirOs):
    """
    Mock backend with converter for radio settings
    """
    converters = [
        Radio,
    ]


class ResolvAirOs(AirOs):
    """
    Mock backend with converter for network resolver
    """
    converters = [
        Resolv,
    ]


class RouteAirOs(AirOs):
    """
    Mock backend with converter for static routes
    """
    converters = [
        Route,
    ]


class SnmpAirOs(AirOs):
    """
    Mock backend with converter for simple network management protocol
    """
    converters = [
        Snmp,
    ]


class SshdAirOs(AirOs):
    """
    Mock backend with converter for ssh daemon settings
    """
    converters = [
        Sshd,
    ]


class SyslogAirOs(AirOs):
    """
    Mock backend with converter for remote logging
    """
    converters = [
        Syslog,
    ]


class SystemAirOs(AirOs):
    """
    Mock backend with converter for system settings
    """
    converters = [
        System,
    ]


class TelnetdAirOs(AirOs):
    """
    Mock backend with converter for telnet daemon settings
    """
    converters = [
        Telnetd,
    ]


class UpdateAirOs(AirOs):
    """
    Mock backend with converter for update
    """
    converters = [
        Update,
    ]


class UsersAirOs(AirOs):
    """
    Mock backend with converter for users settings
    """
    converters = [
        Users,
    ]


class VlanAirOs(AirOs):
    """
    Mock backend with converter for vlan settings
    """
    converters = [
        Vlan,
    ]


class WirelessAirOs(AirOs):
    """
    Mock backend with converter for wireless settings
    """
    converters = [
        Wireless,
    ]


class WpasupplicantAirOs(AirOs):
    """
    Mock backend with converter for wpasupplicant settings
    """
    converters = [
        Wpasupplicant,
    ]
