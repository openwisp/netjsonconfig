from . import converters
from ..base.backend import BaseBackend
from .renderer import Commands, Hostapd, Hostname, Interfaces, Ntp, Resolv
from .schema import schema


class Raspbian(BaseBackend):
    """
    Raspbian Backend
    """
    schema = schema
    converters = [
        converters.General,
        converters.Interfaces,
        converters.Wireless,
        converters.DnsServers,
        converters.DnsSearch,
        converters.Ntp
    ]
    renderers = [
        Hostname,
        Hostapd,
        Interfaces,
        Resolv,
        Ntp,
        Commands
    ]
