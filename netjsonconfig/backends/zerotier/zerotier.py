from ..base.backend import BaseVpnBackend
from . import converters
from .parser import ZeroTierParser, config_suffix, vpn_pattern
from .renderer import ZeroTierRenderer
from .schema import schema


class ZeroTier(BaseVpnBackend):
    schema = schema
    converters = [converters.ZeroTier]
    renderer = ZeroTierRenderer
    parser = ZeroTierParser
    # BaseVpnBackend attributes
    vpn_pattern = vpn_pattern
    config_suffix = config_suffix

    @classmethod
    def auto_client(cls, server=None, **kwargs):
        server = server or {}
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
