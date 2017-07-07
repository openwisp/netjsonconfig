from ....utils import get_copy
from .base import RaspbianConverter


class Ntp(RaspbianConverter):
    netjson_key = 'ntp'

    def to_intermediate(self):
        result = []
        ntp = get_copy(self.netjson, self.netjson_key)
        if ntp.get('enabled', False):
            for server in ntp.get('server'):
                result.append(server)
        return (('ntp', result),)
