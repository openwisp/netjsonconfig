from ...zerotier.converters import ZeroTier as BaseZeroTier
from ..schema import schema
from .base import OpenWrtConverter


class ZeroTier(OpenWrtConverter, BaseZeroTier):
    _uci_types = ['zerotier']
    _schema = schema['properties']['zerotier']['items']

    def __intermediate_vpn(self, vpn):
        files = self.netjson.get('files', [])
        self.netjson['files'] = self.__get_zt_ifname_files(vpn, files)
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
        vpn['name'] = vpn.pop('.name')
        # 'disabled' defaults to False in OpenWRT
        vpn['disabled'] = vpn.pop('enabled', '0') == '0'
        del vpn['.type']
        return super().__netjson_vpn(vpn)

    def __get_zt_ifname_files(self, vpn, files):
        updated_files = []
        zt_interface_map = {
            'path': f"{vpn.get('config_path')}/devicemap",
            'mode': '0644',
            'contents': '',
        }
        for file in files:
            if file.get('path') == zt_interface_map.get('path'):
                zt_interface_map['contents'] += file.get('contents') + '\n'
            else:
                updated_files.append(file)

        if zt_interface_map.get('contents'):
            updated_files.append(zt_interface_map)
        return updated_files
