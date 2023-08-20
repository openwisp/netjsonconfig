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
        config_path='/etc/ow_zerotier_extra',
        copy_config_path='0',
        ifname='',
        disabled=False,
    ):
        nwid = nwid or ['']
        copy_config_path = '1' if ifname else copy_config_path
        return {
            'name': name,
            'secret': identity_secret,
            'config_path': config_path,
            'nwid_ifname': [
                {
                    'id': nwid,
                    'ifname': ifname,
                }
            ],
            'disabled': disabled,
        }
