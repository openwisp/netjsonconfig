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
        nwid=None,
        identity_secret='{{zt_identity_secret}}',
        config_path='',
        copy_config_path='0',
        zt_ifname='',
        disabled=False,
    ):
        nwid = nwid or ['']
        return {
            'id': nwid,
            'name': name,
            'secret': identity_secret,
            'config_path': config_path,
            'copy_config_path': copy_config_path,
            'zt_ifname': zt_ifname,
            'disabled': disabled,
        }
