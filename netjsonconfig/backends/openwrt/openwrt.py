from ..base.backend import BaseBackend
from ..vxlan.vxlan_wireguard import VxlanWireguard
from ..wireguard.wireguard import Wireguard
from . import converters
from .parser import OpenWrtParser, config_path, packages_pattern
from .renderer import OpenWrtRenderer
from .schema import schema


class OpenWrt(BaseBackend):
    """
    OpenWRT / LEDE Configuration Backend
    """

    schema = schema
    converters = [
        converters.General,
        converters.Ntp,
        converters.Led,
        converters.Interfaces,
        converters.Routes,
        converters.Rules,
        converters.Switch,
        converters.Radios,
        converters.Wireless,
        converters.OpenVpn,
        converters.WireguardPeers,
        converters.Default,
    ]
    parser = OpenWrtParser
    renderer = OpenWrtRenderer
    list_identifiers = ['name', 'config_value', 'id']

    def _generate_contents(self, tar):
        """
        Adds configuration files to tarfile instance.

        :param tar: tarfile instance
        :returns: None
        """
        uci = self.render(files=False)
        # create a list with all the packages (and remove empty entries)
        packages = packages_pattern.split(uci)
        if '' in packages:
            packages.remove('')
        # create an UCI file for each configuration package used
        for package in packages:
            lines = package.split('\n')
            package_name = lines[0]
            text_contents = '\n'.join(lines[2:])
            self._add_file(
                tar=tar,
                name='{0}{1}'.format(config_path, package_name),
                contents=text_contents,
            )

    @classmethod
    def wireguard_auto_client(cls, **kwargs):
        data = Wireguard.auto_client(**kwargs)
        config = {
            'interfaces': [
                {
                    'name': data['interface_name'],
                    'type': 'wireguard',
                    'private_key': data['client']['private_key'],
                    'port': data['client']['port'],
                    # Default values for Wireguard Interface
                    'mtu': 1420,
                    'nohostroute': False,
                    'fwmark': '',
                    'ip6prefix': [],
                    'addresses': [],
                    'network': '',
                }
            ],
            'wireguard_peers': [
                {
                    'interface': data['interface_name'],
                    'public_key': data['server']['public_key'],
                    'allowed_ips': data['server']['allowed_ips'],
                    'endpoint_host': data['server']['endpoint_host'],
                    'endpoint_port': data['server']['endpoint_port'],
                    # Default values for Wireguard Peers
                    'preshared_key': '',
                    'persistent_keepalive': 60,
                    'route_allowed_ips': True,
                }
            ],
        }
        if data['client']['ip_address']:
            config['interfaces'][0]['addresses'] = [
                {
                    'proto': 'static',
                    'family': 'ipv4',
                    'address': data['client']['ip_address'],
                    'mask': 32,
                },
            ]
        return config

    @classmethod
    def vxlan_wireguard_auto_client(cls, **kwargs):
        config = cls.wireguard_auto_client(**kwargs)
        vxlan_config = VxlanWireguard.auto_client(**kwargs)
        vxlan_interface = {
            'name': 'vxlan',
            'type': 'vxlan',
            'vtep': vxlan_config['server_ip_address'],
            'port': 4789,
            'vni': vxlan_config['vni'],
            'tunlink': config['interfaces'][0]['name'],
            # Default values for VXLAN interface
            'rxcsum': True,
            'txcsum': True,
            'mtu': 1280,
            'ttl': 64,
            'mac': '',
            'disabled': False,
            'network': '',
        }
        config['interfaces'].append(vxlan_interface)
        return config
