import re

from .converters import *
from .renderers import Resolv, Hostapd
from ..base.backend import BaseBackend
from .schema import schema


class Raspbian(BaseBackend):
    """
    Raspbian Backend
    """
    schema = schema
    env_path = 'netjsonconfig.backends.raspbian'
    converters = [
        DNS_Servers,
        DNS_Search
    ]
    renderer = Resolv
