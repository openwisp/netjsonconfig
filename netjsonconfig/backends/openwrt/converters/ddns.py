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
            block.update({
                '.type': 'ddns',
                '.name': block.pop('id', 'global'),
            })
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
            resultdict = OrderedDict((('.name', uci_name),
                                      ('.type', 'service')))
            resultdict.update(provider)
            result.append(resultdict)
        return result

    def to_netjson_loop(self, block, result, index):
        result['ddns'] = self.__netjson_ddns(block)
        return result

    def __netjson_ddns(self, ddns):
        del ddns['.type']
        _name = ddns.pop('.name')
        if _name != 'ddns':
            ddns['id'] = _name
        return self.type_cast(ddns)
