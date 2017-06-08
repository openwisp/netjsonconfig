from ...utils import get_copy, sorted_dict
from ..base.converter import BaseConverter


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
                if bssid != None:
                    temp.update({'bssid': bssid})
                hidden = interface['wireless'].get('hidden', None)
                if hidden != None:
                    temp.update({'hidden': hidden})
                encryption = interface['wireless'].get('encryption', None)
                if encryption  != None:
                    protocol = encryption.get('protocol')
                    key = encryption.get('key')
                    cipher = encryption.get('cipher', None)
                    if cipher != None:
                        temp.update({'cipher':cipher})
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
