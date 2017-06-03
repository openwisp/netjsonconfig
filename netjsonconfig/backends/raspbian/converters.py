from ...utils import get_copy, sorted_dict
from ..base.converter import BaseConverter


class DNS_Servers(BaseConverter):
    netjson_key = 'dns_servers'

    def to_intermediate(self):
        result = []
        dns_servers = get_copy(self.netjson, self.netjson_key)
        temp = {
            'nameserver': [],
        }
        for nameserver in dns_servers:
            temp['nameserver'].append({
                'ip': nameserver,
            })
        result.append(sorted_dict(temp))
        print result
        return (('dns_servers', result),)


class DNS_Search(BaseConverter):
    netjson_key = 'dns_search'

    def to_intermediate(self):
        result = []
        dns_search = get_copy(self.netjson, self.netjson_key)
        temp = {
            'domain': [],
        }
        for domain in dns_search:
            temp['domain'].append({
                'domain': domain
            })
        result.append(sorted_dict(temp))
        print result
        return (('dns_search', result),)
