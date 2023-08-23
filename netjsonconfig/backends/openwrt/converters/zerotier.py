from ...zerotier.converters import ZeroTier as BaseZeroTier
from ..schema import schema
from .base import OpenWrtConverter


class ZeroTier(OpenWrtConverter, BaseZeroTier):
    _uci_types = ['zerotier']
    _schema = schema['properties']['zerotier']['items']

    def __intermediate_vpn(self, vpn):
        nwid_ifnames = vpn.get('nwid_ifname', [])
        files = self.netjson.get('files', [])
        self.netjson['files'] = self.__get_zt_ifname_files(vpn, files)
        vpn.update(
            {
                '.name': self._get_uci_name(vpn.pop('name')),
                '.type': 'zerotier',
                'config_path': vpn.get('config_path', '/etc/openwisp/zerotier'),
                'copy_config_path': vpn.get('copy_config_path', '1'),
                'join': [nwid_ifname.get('id', '') for nwid_ifname in nwid_ifnames],
                'enabled': not vpn.pop('disabled', False),
            }
        )
        del vpn['nwid_ifname']
        return super().__intermediate_vpn(vpn, remove=[''])

    def __netjson_vpn(self, vpn):
        nwids = vpn.pop('join')
        vpn['name'] = vpn.pop('.name')
        vpn['nwid_ifname'] = [
            {"id": nwid, "ifname": f"owzt{nwid[-6:]}"} for nwid in nwids
        ]
        # 'disabled' defaults to False in OpenWRT
        vpn['disabled'] = vpn.pop('enabled', '0') == '0'
        del vpn['.type']
        return super().__netjson_vpn(vpn)

    def __get_zt_ifname_files(self, vpn, files):
        config_path = vpn.get('config_path', '/etc/openwisp/zerotier')
        nwid_ifnames = vpn.get('nwid_ifname', [])
        zt_file_contents = '# network_id=interface_name\n'

        for nwid_ifname in nwid_ifnames:
            nwid = nwid_ifname.get('id', '')
            ifname = nwid_ifname.get('ifname', f'owzt{nwid[-6:]}')
            zt_file_contents += f"{nwid}={ifname}\n"

        zt_interface_map = {
            'path': f"{config_path}/devicemap",
            'mode': '0644',
            'contents': zt_file_contents,
        }

        if not files:
            return [zt_interface_map]
        updated_files = []
        for file in files:
            if file.get('path') == zt_interface_map.get('path'):
                zt_interface_map['contents'] += '\n' + file['contents']
            else:
                updated_files.append(file)
        if zt_interface_map.get('contents'):
            updated_files.append(zt_interface_map)
        return updated_files
