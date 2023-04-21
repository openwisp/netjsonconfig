from collections import OrderedDict

from ..schema import schema
from .base import OpenWrtConverter


class Mwan3(OpenWrtConverter):
    netjson_key = "mwan3"
    intermediate_key = "mwan3"
    _uci_types = ["interface", "member"]
    _schema = schema["properties"]["mwan3"]

    def to_intermediate_loop(self, block, result, index=None):
        interfaces = self.__intermediate_interfaces(block.pop("interfaces", {}))
        members = self.__intermediate_members(block.pop("members", {}))
        result.setdefault("mwan3", [])
        result["mwan3"] = interfaces + members
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

    def __intermediate_members(self, members):
        """
        converts NetJSON member to
        UCI intermediate data structure
        """
        result = []
        for member in members:
            resultdict = OrderedDict(
                (
                    (
                        (".name", self._get_uci_name(member["name"])),
                        (".type", "member"),
                    )
                )
            )
            resultdict.update(member)
            result.append(resultdict)
        return result

    def to_netjson_loop(self, block, result, index):
        result.setdefault("mwan3", {})
        _type = block.pop(".type")
        if _type == "interface":
            interface = self.__netjson_interface(block)
            result["mwan3"].setdefault("interfaces", [])
            result['mwan3']['interfaces'].append(interface)
        if _type == "member":
            member = self.__netjson_member(block)
            result["mwan3"].setdefault("members", [])
            result['mwan3']['members'].append(member)
        return result

    def __netjson_interface(self, interface):
        interface["name"] = interface.pop(".name")
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

    def __netjson_member(self, member):
        member["name"] = member.pop(".name")
        for option in ["metric", "weight"]:
            if option in member:
                try:
                    member[option] = int(member[option])
                except ValueError:
                    del member[option]
        return self.type_cast(member)
