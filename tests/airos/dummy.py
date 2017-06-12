from netjsonconfig import AirOS

from netjsonconfig.backends.airos.converters import *


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


class NetconfAirOS(AirOS):
    """
    Mock backend with converter for network configuration
    """
    converters = [
            Netconf,
    ]


class Netmode(AirOS):
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
