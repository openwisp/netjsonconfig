from collections import OrderedDict

from ..schema import schema
from .base import OpenWrtConverter


class Ddns(OpenWrtConverter):
    netjson_key = 'ddns'
    intermediate_key = 'ddns'
    _uci_types = ['ddns', 'service']
    _schema = schema['properties']['ddns']

    def to_intermediate_loop(self, block, result, index=None):
        if block:
            provider_list = self.__intermediate_providers(block.pop('providers', {}))
            block.update({'.type': 'ddns', '.name': block.pop('id', 'global')})
            result.setdefault('ddns', [])
            result['ddns'] = [self.sorted_dict(block)] + provider_list

        return result

    def __intermediate_providers(self, providers):
        """
        converts NetJSON provider to
        UCI intermediate data structure
        """
        result = []

        for provider in providers:
            uci_name = self._get_uci_name(provider['lookup_host'])
            resultdict = OrderedDict((('.name', uci_name), ('.type', 'service')))
            resultdict.update(provider)
            result.append(resultdict)

        return result

    def to_netjson_loop(self, block, result, index):
        result.setdefault(self.netjson_key, {})

        if block['.type'] == 'service':
            result[self.netjson_key].setdefault('providers', [])
            result[self.netjson_key]['providers'].append(self.__netjson_ddns(block))
        else:
            result['ddns'] = self.__netjson_ddns(block)

        return result

    def __netjson_ddns(self, ddns):
        _type = ddns.pop('.type')
        del ddns['.name']

        if _type == 'service':
            ddns_schema = self._schema.get('properties').get('providers').get('items')
            return self.type_cast(ddns, schema=ddns_schema)

        return self.type_cast(ddns)
