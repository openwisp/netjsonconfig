from ....utils import get_copy
from .base import RaspbianConverter


class DnsServers(RaspbianConverter):
    netjson_key = 'dns_servers'

    def to_intermediate(self):
        result = []
        dns_servers = get_copy(self.netjson, self.netjson_key)
        for nameserver in dns_servers:
            result.append(nameserver)
        return (('dns_servers', result),)
