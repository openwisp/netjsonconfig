from ..base.backend import BaseVpnBackend
from . import converters
from .parser import config_suffix, vpn_pattern
from .renderer import WireguardRenderer
from .schema import schema


class Wireguard(BaseVpnBackend):
    schema = schema
    converters = [converters.Wireguard]
    renderer = WireguardRenderer
    # BaseVpnBackend attributes
    vpn_pattern = vpn_pattern
    config_suffix = config_suffix
