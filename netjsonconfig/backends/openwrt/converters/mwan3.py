from collections import OrderedDict

from ..schema import schema
from .base import OpenWrtConverter


class Mwan3(OpenWrtConverter):
    netjson_key = 'mwan3'
    intermediate_key = 'mwan3'
    _uci_types = ['interface']
    _schema = schema['properties']['mwan3']

    def to_intermediate_loop(self, block, result, index=None):
        interfaces = self.__intermediate_interfaces(block.pop('interfaces', {}))
        result.setdefault('mwan3', [])
        result['mwan3'] = interfaces
        return result

    def __intermediate_interfaces(self, interfaces):
        """
        converts NetJSON interface to
        UCI intermediate data structure
        """
        result = []
        for interface in interfaces:
            resultdict = OrderedDict(
                (
                    ('.name', self._get_uci_name(interface.pop('name'))),
                    ('.type', 'interface'),
                )
            )
            resultdict.update(interface)
            result.append(resultdict)
        return result

    def to_netjson_loop(self, block, result, index):
        result['mwan3'] = self.__netjson_mwan3(block)
        return result

    def __netjson_mwan3(self, mwan3):
        del mwan3['.type']
        _name = mwan3.pop('.name')
        if _name != 'mwan3':
            mwan3['id'] = _name
        return self.type_cast(mwan3)
