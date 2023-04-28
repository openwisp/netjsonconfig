from collections import OrderedDict

from ..schema import schema
from .base import OpenWrtConverter


class Mwan3(OpenWrtConverter):
    netjson_key = "mwan3"
    intermediate_key = "mwan3"
    _uci_types = ["globals", "interface", "member", "policy", "rule"]
    _schema = schema["properties"]["mwan3"]

    def to_intermediate_loop(self, block, result, index=None):
        globals = self.__intermediate_globals(block.pop("globals", {}))
        interfaces = self.__intermediate_interfaces(block.pop("interfaces", {}))
        members = self.__intermediate_members(block.pop("members", {}))
        policies = self.__intermediate_policies(block.pop("policies", {}))
        rules = self.__intermediate_rules(block.pop("rules", {}))
        result.setdefault("mwan3", [])
        result["mwan3"] = globals + interfaces + members + policies + rules
        return result

    def __intermediate_globals(self, globals):
        """
        converts NetJSON globals to
        UCI intermediate data structure
        """
        result = OrderedDict(((".name", "globals"), (".type", "globals")))
        result.update(globals)
        return [result]

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

    def __intermediate_policies(self, policies):
        """
        converts NetJSON policy to
        UCI intermediate data structure
        """
        result = []
        for policy in policies:
            resultdict = OrderedDict(
                (
                    (
                        (".name", self._get_uci_name(policy["name"])),
                        (".type", "policy"),
                    )
                )
            )
            resultdict.update(policy)
            result.append(resultdict)
        return result

    def __intermediate_rules(self, rules):
        """
        converts NetJSON rule to
        UCI intermediate data structure
        """
        result = []
        for rule in rules:
            resultdict = OrderedDict(
                (
                    (
                        (".name", self._get_uci_name(rule["name"])),
                        (".type", "rule"),
                    )
                )
            )
            if "proto" in rule:
                # If proto is a single value, then force it not to be in a list so that
                # the UCI uses "option" rather than "list". If proto is only "tcp"
                # and"udp", we can force it to the single special value of "tcpudp".
                proto = rule["proto"]
                if len(proto) == 1:
                    rule["proto"] = proto[0]
                elif set(proto) == {"tcp", "udp"}:
                    rule["proto"] = "tcpudp"
            resultdict.update(rule)
            result.append(resultdict)
        return result

    def to_netjson_loop(self, block, result, index):
        result.setdefault("mwan3", {})
        _name = block.pop(".name")
        _type = block.pop(".type")
        if _type == "globals":
            globals = self.__netjson_globals(block)
            if globals:
                result["mwan3"].setdefault("globals", {})
                result['mwan3']['globals'].update(globals)
        if _type == "interface":
            interface = self.__netjson_interface(block)
            result["mwan3"].setdefault("interfaces", [])
            result['mwan3']['interfaces'].append(interface)
        if _type == "member":
            member = self.__netjson_member(block)
            result["mwan3"].setdefault("members", [])
            result['mwan3']['members'].append(member)
        if _type == "policy":
            member = self.__netjson_policy(block)
            result["mwan3"].setdefault("policies", [])
            result['mwan3']['policies'].append(member)
        if _type == "rules":
            rule = self.__netjson_rule(block)
            result["mwan3"].setdefault("rules", [])
            result['mwan3']['rules'].append(rule)
        return result

    def __netjson_globals(self, globals):
        if "logging" in globals:
            globals["logging"] = globals["logging"] in [
                "1",
                "yes",
                "on",
                "true",
                "enabled",
            ]
        return self.type_cast(globals)

    def __netjson_interface(self, interface):
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
        for option in ["metric", "weight"]:
            if option in member:
                try:
                    member[option] = int(member[option])
                except ValueError:
                    del member[option]
        return self.type_cast(member)

    def __netjson_policy(self, policy):
        return self.type_cast(policy)

    def __netjson_rule(self, rule):
        for option in [
            "sticky",
            "logging",
        ]:
            if option in rule:
                rule[option] = option in ["1", "yes", "on", "true", "enabled"]

        if "timeout" in rule:
            try:
                rule["timeout"] = int(rule["timeout"])
            except ValueError:
                del rule["timeout"]
        if "proto" in rule:
            rule["proto"] = self.__netjson_generic_proto(rule["proto"])

        return self.type_cast(rule)

    def __netjson_generic_proto(self, proto):
        if isinstance(proto, list):
            return proto.copy()
        else:
            if proto == "tcpudp":
                return ["tcp", "udp"]
            else:
                return proto.split()
