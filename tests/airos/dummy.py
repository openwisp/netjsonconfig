from netjsonconfig import AirOS

from netjsoncongig.backends.airos.converters import Aaa, Bridge, Discovery, Dyndns, Ebtables, Gui, \
        Httpd, Igmpproxy, Iptables, Netconf, Netmode, Ntpclient, \
        Pwdog, Radio, Resolv, Route, Snmp, Sshd, Syslog, System, \
        Telnetd, Update, Users, Vlan, Wireless, Wpasupplicant

from unittest import TestCase


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
        for (a, b) in zip(a, b):
            self.assertEqual(a, b)


class AaaAirOS(AirOS):
    """
    Mock backend with converter for radius authentication
    """
    converters = [
            Aaa,
    ]


class BridgeAirOS(AirOS):
    """
    Mock backend with converter for bridge interface
    """
    converters = [
            Bridge,
    ]


class DiscoveryAirOS(AirOS):
    """
    Mock backend with converter for network hardware discovery
    """
    converters = [
            Discovery,
    ]


class DyndnsAirOS(AirOS):
    """
    Mock backend with converter for dynamic dns capabilities
    """
    converters = [
            Dyndns,
    ]


class EbtablesAirOS(AirOS):
    """
    Mock backend with converter for ebtables
    """
    converters = [
            Ebtables,
    ]


class GuiAirOS(AirOS):
    """
    Mock backend with converter for web interface settings
    """
    converters = [
            Gui,
    ]


class HttpdAirOS(AirOS):
    """
    Mock backend with converter for web server
    """
    converters = [
            Httpd,
    ]


class Igmpproxy(AirOS):
    """
    Mock backend with converter for igmpproxy
    """
    converters = [
            Igmpproxy,
    ]


class IptablesAirOS(AirOS):
    """
    Mock backend with converter for iptables
    """
    converters = [
            Iptables,
    ]


class NetconfAirOS(AirOS):
    """
    Mock backend with converter for network configuration
    """
    converters = [
            Netconf,
    ]


class NetmodeAirOS(AirOS):
    """
    Mock backend with converter for network mode
    """
    converters = [
            Netmode,
    ]


class NtpclientAirOS(AirOS):
    """
    Mock backend with converter for ntp settings
    """
    converters = [
            Ntpclient,
    ]


class PwdogAirOS(AirOS):
    """
    Mock backend with converter for ping watchdog settings
    """
    converters = [
            Pwdog,
    ]


class RadioAirOS(AirOS):
    """
    Mock backend with converter for radio settings
    """
    converters = [
            Radio,
    ]


class ResolvAirOS(AirOS):
    """
    Mock backend with converter for network resolver
    """
    converters = [
            Resolv,
    ]


class RouteAirOS(AirOS):
    """
    Mock backend with converter for static routes
    """
    converters = [
            Route,
    ]


class SnmpAirOS(AirOS):
    """
    Mock backend with converter for simple network management protocol
    """
    converters = [
            Snmp,
    ]



class SshdAirOS(AirOS):
    """
    Mock backend with converter for ssh daemon settings
    """
    converters = [
            Sshd,
    ]


class SyslogAirOS(AirOS):
    """
    Mock backend with converter for remote logging
    """
    converters = [
            Syslog,
    ]


class SystemAirOS(AirOS):
    """
    Mock backend with converter for system settings
    """
    converters = [
            System,
    ]


class TelnetdAirOS(AirOS):
    """
    Mock backend with converter for telnet daemon settings
    """
    converters = [
            Telnetd,
    ]


class UpdateAirOS(AirOS):
    """
    Mock backend with converter for update
    """
    converters = [
            Update,
    ]


class UsersAirOS(AirOS):
    """
    Mock backend with converter for users settings
    """
    converters = [
            Users,
    ]


class VlanAirOS(AirOS):
    """
    Mock backend with converter for vlan settings
    """
    converters = [
            Vlan,
    ]


class WirelessAirOS(AirOS):
    """
    Mock backend with converter for wireless settings
    """
    converters = [
            Wireless,
    ]


class WpasupplicantAirOS(AirOS):
    """
    Mock backend with converter for wpasupplicant settings
    """
    converters = [
            Wpasupplicant,
    ]
