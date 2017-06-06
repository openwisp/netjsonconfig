from ...utils import get_copy, sorted_dict
from ..base.converter import BaseConverter


class Wireless(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        interfaces = get_copy(self.netjson, self.netjson_key)
        for interface in interfaces:
            if interface['type'] == 'wireless':
                radio = interface['wireless'].get('radio')
                mode = interface['wireless'].get('mode')
                ssid = interface['wireless'].get('ssid')
                temp = {
                    'radio': radio,
                    'mode': mode,
                    'ssid': ssid,
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


class DNS_Servers(BaseConverter):
    netjson_key = 'dns_servers'

    def to_intermediate(self):
        result = []
        dns_servers = get_copy(self.netjson, self.netjson_key)
        for nameserver in dns_servers:
            result.append(nameserver)
        return (('dns_servers', result),)


class DNS_Search(BaseConverter):
    netjson_key = 'dns_search'

    def to_intermediate(self):
        result = []
        dns_search = get_copy(self.netjson, self.netjson_key)
        for domain in dns_search:
            result.append(domain)
        return (('dns_search', result),)
