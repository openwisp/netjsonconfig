from ...utils import get_copy
from ..base.converter import BaseConverter
from ipaddress import IPv4Interface


class Interfaces(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        interfaces = get_copy(self.netjson, self.netjson_key)
        for interface in interfaces:
            ifname = interface.get('name')
            iftype = interface.get('type')
            addresses = interface.get('addresses', None)
            new_interface = {
                'ifname': ifname,
                'iftype': iftype,
            }
            address_list = []
            if iftype == 'bridge':
                new_interface.update({
                    'bridge_members': interface.get('bridge_members'),
                })
            mtu = interface.get('mtu', None)
            if mtu is not None:
                new_interface.update({
                    'mtu': mtu
                })
            mac = interface.get('mac', None)
            if mac is not None:
                new_interface.update({
                    'mac': mac
                })
            if addresses is not None:
                for address in addresses:
                    new_address = {}
                    if iftype in ['ethernet', 'bridge', 'loopback']:
                        if address.get('proto') == 'static':
                            if address.get('family') == 'ipv4':
                                addressmask = str(address.get('address')) + '/' + str(address.get('mask'))
                                new_address.update({
                                    'proto': 'static',
                                    'family': 'ipv4',
                                    'ipv4address': address.get('address'),
                                    'ipv4netmask': IPv4Interface(addressmask).with_netmask.split('/')[1]
                                })
                                if address.get('gateway', None) is not None:
                                    new_address.update({
                                        'ipv4gateway': address.get('gateway'),
                                    })
                            if address.get('family') == 'ipv6':
                                new_address.update({
                                    'proto': 'static',
                                    'family': 'ipv6',
                                    'ipv6address': address.get('address'),
                                    'ipv6netmask': address.get('mask')
                                })
                                if address.get('gateway', None) is not None:
                                    new_address.update({
                                        'ipv6gateway': address.get('gateway'),
                                    })
                        elif address.get('proto') == 'dhcp':
                            if address.get('family') == 'ipv4':
                                new_address.update({
                                    'proto': 'dhcp',
                                    'family': 'ipv4',
                                })
                            elif address.get('family') == 'ipv6':
                                new_address.update({
                                    'proto': 'dhcp',
                                    'family': 'ipv6',
                                })
                        address_list.append(new_address)
                    new_interface.update({
                        'address': address_list
                    })
            result.append(new_interface)
        return (('interfaces', result),)


class Wireless(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        interfaces = get_copy(self.netjson, self.netjson_key)
        for interface in interfaces:
            if interface['type'] == 'wireless':
                new_interface = {
                    'ifname': interface.get('name'),
                    'iftype': interface.get('type'),
                    'ssid': interface['wireless'].get('ssid')
                }
                wireless = interface.get('wireless')
                # radio_num = interface['wireless'].get('radio')
                # radios = get_copy(self.netjson, 'radios')
                # print radios
                # if radios is not None:
                #     req_radio = [radio for radio in radios if radio['name'] == radio_num][0]
                #     hwmode = self._get_hwmode(req_radio)
                #     channel = req_radio['channel']
                #     protocol = req_radio['protocol'].replace(".", "")
                #     new_interface.update({
                #         'hwmode': hwmode,
                #         'channel': channel,
                #         'protocol': protocol
                #     })
                new_interface.update({'encryption': self._get_encryption(wireless)})
                result.append(new_interface)
        return (('wireless', result),)

    def _get_hwmode(self, radio):
        protocol = radio['protocol']
        if protocol in ['802.11a', '802.11b', '802.11g']:
            return protocol[1:]
        if radio['channel'] is 0:
            return radio.get('hwmode')
        elif radio['channel'] <= 13:
            return 'g'
        else:
            return 'a'

    def _get_encryption(self, wireless):
        encryption = wireless.get('encryption')
        disabled = encryption.get('disabled', False)
        new_encryption = {}
        if encryption.get('protocol') is not 'none' and encryption.get('disabled') is not True:
            protocol, method = encryption.get('protocol').split("_")
            if protocol in ['wpa', 'wpa2']:
                auth_algs = '1'
                wpa = '1' if protocol == 'wpa' else '2'
                wpa_key_mgmt = 'WPA-PSK' if method == 'personal' else 'WPA-EAP'
                wpa_passphrase = encryption.get('key')
                new_encryption.update({
                    'auth_algs': auth_algs,
                    'wpa': wpa,
                    'wpa_key_mgmt': wpa_key_mgmt,
                    'wpa_passphrase': wpa_passphrase
                    })
                if encryption.get('cipher', None) is not None or 'auto':
                    wpa_pairwise = str(encryption.get('cipher').replace('+', ' ')).upper()
                    new_encryption.update({'wpa_pairwise': wpa_pairwise})
        return new_encryption

class DnsServers(BaseConverter):
    netjson_key = 'dns_servers'

    def to_intermediate(self):
        result = []
        dns_servers = get_copy(self.netjson, self.netjson_key)
        for nameserver in dns_servers:
            result.append(nameserver)
        return (('dns_servers', result),)


class DnsSearch(BaseConverter):
    netjson_key = 'dns_search'

    def to_intermediate(self):
        result = []
        dns_search = get_copy(self.netjson, self.netjson_key)
        for domain in dns_search:
            result.append(domain)
        return (('dns_search', result),)
