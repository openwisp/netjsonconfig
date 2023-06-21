from ...zerotier.converters import ZeroTier as BaseZeroTier
from ..schema import schema
from .base import OpenWrtConverter


class ZeroTier(OpenWrtConverter, BaseZeroTier):
    _uci_types = ['zerotier']
    _schema = schema['properties']['zerotier']['items']

    def __intermediate_vpn(self, vpn):
        vpn.update(
            {
                '.name': self._get_uci_name(vpn.pop('name')),
                '.type': 'zerotier',
                'join': vpn.pop('id'),
                'enabled': not vpn.pop('disabled', False),
            }
        )
        return super().__intermediate_vpn(vpn, remove=[''])

    def __netjson_vpn(self, vpn):
        vpn['id'] = vpn.pop('join')
        vpn['name'] = vpn.pop('.name').replace('_', '-')
        # 'enabled' defaults to False in OpenWRT
        vpn['disabled'] = vpn.pop('enabled', '0') == '0'
        del vpn['.type']
        return super().__netjson_vpn(vpn)
