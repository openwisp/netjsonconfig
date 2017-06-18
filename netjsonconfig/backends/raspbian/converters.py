from ...utils import get_copy
from ..base.converter import BaseConverter
from ipaddress import IPv4Interface


class Radio(BaseConverter):
    netjson_key = 'radios'

    def to_intermediate(self):
        result = []
        radios = get_copy(self.netjson, self.netjson_key)
        for radio in radios:
            temp = {
                'name': radio['name'],
                'protocol': radio['protocol'],
                'channel': radio['channel'],
                'hwmode': self._get_hwmode(radio)
            }
            result.append(temp)
        return (('wireless', result),)

    def _get_hwmode(self, radio):
        protocol = radio['protocol']
        if protocol in ['802.11a', '802.11b', '802.11g']:
            return protocol[4:]
        if radio['channel'] is 0:
            return radio.get('hwmode')
        elif radio['channel'] <= 13:
            return '11g'
        else:
            return '11a'


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
                temp = {
                    'radio': interface['wireless'].get('radio'),
                    'mode': interface['wireless'].get('mode'),
                    'ssid': interface['wireless'].get('ssid'),
                }
                bssid = interface['wireless'].get('bssid', None)
                if bssid is not None:
                    temp.update({'bssid': bssid})
                hidden = interface['wireless'].get('hidden', None)
                if hidden is not None:
                    temp.update({'hidden': hidden})
                encryption = interface['wireless'].get('encryption', None)
                if encryption is not None:
                    protocol = encryption.get('protocol')
                    key = encryption.get('key')
                    cipher = encryption.get('cipher', None)
                    if cipher is not None:
                        temp.update({'cipher': cipher})
                result.append(temp)
        return (('wireless', result),)


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
