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
                    (
                        (".name", self._get_uci_name(interface["name"])),
                        (".type", "interface"),
                    )
                )
            )
            resultdict.update(interface)
            result.append(resultdict)
        return result

    def to_netjson_loop(self, block, result, index):
        result.setdefault("mwan3", {})
        _type = block.pop(".type")
        if _type == "interface":
            interface = self.__netjson_interface(block)
            result["mwan3"].setdefault("interfaces", [])
            result['mwan3']['interfaces'].append(interface)
        return result

    def __netjson_interface(self, interface):
        interface['name'] = interface.pop('.name')
        for option in [
            "enabled",
            "keep_failure_interval",
            "check_quality",
        ]:
            if option in interface:
                interface[option] = option in ["1", "yes", "on", "true", "enabled"]
        for option in [
            "reliability",
            "count",
            "timeout",
            "interval",
            "failure_interval",
            "recovery_interval",
            "failure_latency",
            "recovery_latency",
            "failure_loss",
            "recovery_loss",
            "max_ttl",
            "size",
            "up",
            "down",
        ]:
            if option in interface:
                try:
                    interface[option] = int(interface[option])
                except ValueError:
                    del interface[option]

        return self.type_cast(interface)
