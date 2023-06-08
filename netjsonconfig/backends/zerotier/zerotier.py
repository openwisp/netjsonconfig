from ..base.backend import BaseVpnBackend
from . import converters
from .parser import config_suffix, vpn_pattern
from .renderer import ZeroTierRenderer
from .schema import schema


class ZeroTier(BaseVpnBackend):
    schema = schema
    converters = [converters.ZeroTier]
    renderer = ZeroTierRenderer
    # BaseVpnBackend attributes
    vpn_pattern = vpn_pattern
    config_suffix = config_suffix

    @classmethod
    def auto_client(cls, server={}, **kwargs):
        network_id = server.get('id', server.get('nwid', ''))
        return {
            'zerotier': [
                {
                    'id': network_id,
                    'name': server.get('name', ''),
                    'disabled': server.get('disabled', False),
                }
            ]
        }
