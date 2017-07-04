from ...utils import get_copy
from ..base.converter import BaseConverter
from ipaddress import IPv4Interface


class Interfaces(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        interfaces = get_copy(self.netjson, self.netjson_key)
        for interface in interfaces:
            new_interface = {}
            ifname = interface.get('name')
            iftype = interface.get('type')
            new_interface.update({
                'ifname': ifname,
                'iftype': iftype
            })
            if iftype in ['ethernet', 'bridge', 'loopback']:
                addresses = self._get_address(interface)
                new_interface.update({
                    'address': addresses
                })
            mac = interface.get('mac', False)
            if mac:
                new_interface.update({'mac': mac})
            mtu = interface.get('mtu', False)
            if mtu:
                new_interface.update({'mtu': mtu})
            txqueuelen = interface.get('txqueuelen', False)
            if txqueuelen:
                new_interface.update({'txqueuelen': txqueuelen})
            autostart = interface.get('autostart', False)
            if autostart:
                new_interface.update({'autostart': autostart})
            if iftype == 'wireless' and interface.get('wireless').get('mode') == 'adhoc':
                wireless = interface.get('wireless')
                new_interface.update({
                    'essid': wireless.get('ssid'),
                    'mode': wireless.get('mode')
                })
            if iftype == 'bridge':
                new_interface.update({
                    'bridge_members': interface.get('bridge_members')
                })
            result.append(new_interface)
        return (('interfaces', result),)

    def _get_address(self, interface):
        addresses = interface.get('addresses', False)
        if addresses:
            for address in addresses:
                if address.get('proto') == 'static':
                    if address.get('family') == 'ipv4':
                        address_mask = str(address.get('address')) + '/' + str(address.get('mask'))
                        address['netmask'] = IPv4Interface(address_mask).with_netmask.split('/')[1]
                        del address['mask']
                    if address.get('family') == 'ipv6':
                        address['netmask'] = address['mask']
                        del address['mask']
            return addresses


class Wireless(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        interfaces = get_copy(self.netjson, self.netjson_key)
        for interface in interfaces:
            if interface['type'] == 'wireless' and interface.get('wireless').get('mode') is not 'adhoc':
                new_interface = {
                    'ifname': interface.get('name'),
                    'iftype': interface.get('type'),
                    'ssid': interface['wireless'].get('ssid')
                }
                wireless = interface.get('wireless')
                radio_num = interface['wireless'].get('radio')
                radios = get_copy(self.netjson, 'radios')
                if radios is not None:
                    req_radio = [radio for radio in radios if radio['name'] == radio_num][0]
                    hwmode = self._get_hwmode(req_radio)
                    channel = req_radio['channel']
                    protocol = req_radio['protocol'].replace(".", "")
                    new_interface.update({
                        'hwmode': hwmode,
                        'channel': channel,
                        'protocol': protocol
                    })
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
        encryption = wireless.get('encryption', None)
        if encryption is None:
            return {}
        disabled = encryption.get('disabled', False)
        new_encryption = {}
        if encryption.get('protocol') is not 'none' and disabled is not True:
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


class Ntp(BaseConverter):
    netjson_key = 'ntp'

    def to_intermediate(self):
        result = []
        ntp = get_copy(self.netjson, self.netjson_key)
        if ntp.get('enabled', False):
            for server in ntp.get('server'):
                result.append(server)
        return (('ntp', result),)
