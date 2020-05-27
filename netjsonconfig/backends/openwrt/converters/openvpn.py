from ...openvpn.converters import OpenVpn as BaseOpenVpn
from .base import OpenWrtConverter


class OpenVpn(OpenWrtConverter, BaseOpenVpn):
    _uci_types = ['openvpn']

    def __intermediate_vpn(self, vpn):
        vpn.update(
            {
                '.name': self._get_uci_name(vpn.pop('name')),
                '.type': 'openvpn',
                'enabled': not vpn.pop('disabled', False),
            }
        )
        return super().__intermediate_vpn(vpn, remove=[''])

    def __netjson_vpn(self, vpn):
        if vpn.get('server_bridge') == '1':
            vpn['server_bridge'] = ''
        # 'enabled' defaults to False in OpenWRT
        vpn['disabled'] = vpn.pop('enabled', '0') == '0'
        vpn['name'] = vpn.pop('.name')
        del vpn['.type']
        return super().__netjson_vpn(vpn)
