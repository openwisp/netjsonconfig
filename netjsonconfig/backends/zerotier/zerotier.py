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
    def auto_client(cls, nwid=None, name=None, **kwargs):
        server = kwargs['server'] or {}
        return {
            'zerotier': [
                {
                    'id': [nwid],
                    'name': name or f'network_{nwid}',
                    'disabled': server.get('disabled', False),
                }
            ]
        }
