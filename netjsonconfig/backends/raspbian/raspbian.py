import re

from .converters import *
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
        Radio,
        Wireless,
        DnsServers,
        DnsSearch,
    ]
    renderer = Raspbian
