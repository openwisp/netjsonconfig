from .converters import General, Interfaces, Wireless, DnsServers, DnsSearch, Ntp
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
        General,
        Interfaces,
        Wireless,
        DnsServers,
        DnsSearch,
        Ntp
    ]
    renderer = Raspbian
