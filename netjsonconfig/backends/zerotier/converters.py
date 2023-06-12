from copy import deepcopy

from ..base.converter import BaseConverter
from .schema import schema

zerotier_definitions = {'properties': {}}
definitions = ['zerotier_server', 'zerotier_client']

for definition in definitions:
    properties = schema['definitions'][definition]['properties']
    zerotier_definitions['properties'].update(deepcopy(properties))


class ZeroTier(BaseConverter):
    netjson_key = 'zerotier'
    intermediate_key = 'zerotier'
    _schema = zerotier_definitions

    def to_intermediate_loop(self, block, result, index=None):
        vpn = self.__intermediate_vpn(block)
        result.setdefault('zerotier', [])
        result['zerotier'].append(vpn)
        return result

    def __intermediate_vpn(self, config, remove=None):
        return self.sorted_dict(config)

    def to_netjson_loop(self, block, result, index=None):
        vpn = self.__netjson_vpn(block)
        result.setdefault('zerotier', [])
        result['zerotier'].append(vpn)
        return result

    def __netjson_vpn(self, vpn):
        vpn = self.type_cast(vpn, zerotier_definitions)
        return vpn
