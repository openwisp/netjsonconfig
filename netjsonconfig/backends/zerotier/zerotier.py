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
    def auto_client(
        cls,
        name='ow_zt',
        networks=None,
        identity_secret='{{secret}}',
        config_path='/etc/openwisp/zerotier',
        disabled=False,
    ):
        networks = networks or []
        return {
            'name': name,
            'networks': networks,
            'secret': identity_secret,
            'config_path': config_path,
            'disabled': disabled,
        }
