from .converters import Interfaces, Wireless, DnsServers, DnsSearch, Ntp
from .renderers import Raspbian
from ..base.backend import BaseBackend
from .schema import schema


class Raspbian(BaseBackend):
    """
    Raspbian Backend
    """
    schema = schema
    env_path = 'netjsonconfig.backends.raspbian'
    converters = [
        Interfaces,
        Wireless,
        DnsServers,
        DnsSearch,
        Ntp
    ]
    renderer = Raspbian
