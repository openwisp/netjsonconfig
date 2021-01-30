"""Firewall configuration management for OpenWRT.

See the following resource for a detailed description of the sections and parameters of
the UCI configuration for the OpenWRT firewall.

    https://openwrt.org/docs/guide-user/firewall/firewall_configuration
"""
from collections import OrderedDict

from ..schema import schema
from .base import OpenWrtConverter


class Firewall(OpenWrtConverter):
    netjson_key = "firewall"
    intermediate_key = "firewall"
    _uci_types = ["defaults", "forwarding", "zone", "rule", "redirect"]
    _schema = schema["properties"]["firewall"]

    def to_intermediate_loop(self, block, result, index=None):
        forwardings = self.__intermediate_forwardings(block.pop("forwardings", {}))
        zones = self.__intermediate_zones(block.pop("zones", {}))
        rules = self.__intermediate_rules(block.pop("rules", {}))
        redirects = self.__intermediate_redirects(block.pop("redirects", {}))
        block.update({".type": "defaults", ".name": block.pop("id", "defaults")})
        result.setdefault("firewall", [])
        result["firewall"] = (
            [self.sorted_dict(block)] + forwardings + zones + rules + redirects
        )
        return result

    def __intermediate_forwardings(self, forwardings):
        """
        converts NetJSON forwarding to
        UCI intermediate data structure
        """
        result = []
        for forwarding in forwardings:
            resultdict = OrderedDict(
                (
                    (".name", self.__get_auto_name_forwarding(forwarding)),
                    (".type", "forwarding"),
                )
            )
            resultdict.update(forwarding)
            result.append(resultdict)
        return result

    def __get_auto_name_forwarding(self, forwarding):
        if "family" in forwarding.keys():
            uci_name = self._get_uci_name(
                "_".join([forwarding["src"], forwarding["dest"], forwarding["family"]])
            )
        else:
            uci_name = self._get_uci_name(
                "_".join([forwarding["src"], forwarding["dest"]])
            )
        return "forwarding_{0}".format(uci_name)

    def __intermediate_zones(self, zones):
        """
        converts NetJSON zone to
        UCI intermediate data structure
        """
        result = []
        for zone in zones:
            resultdict = OrderedDict(
                ((".name", self.__get_auto_name_zone(zone)), (".type", "zone"))
            )
            # If network contains only a single value, force the use of a UCI "option"
            # rather than "list"".
            network = zone["network"]
            if len(network) == 1:
                zone["network"] = network[0]
            resultdict.update(zone)
            result.append(resultdict)
        return result

    def __get_auto_name_zone(self, zone):
        return "zone_{0}".format(self._get_uci_name(zone["name"]))

    def __intermediate_rules(self, rules):
        """
        converts NetJSON rule to
        UCI intermediate data structure
        """
        result = []
        for rule in rules:
            if "config_name" in rule:
                del rule["config_name"]
            resultdict = OrderedDict(
                ((".name", self.__get_auto_name_rule(rule)), (".type", "rule"))
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

    def __get_auto_name_rule(self, rule):
        return "rule_{0}".format(self._get_uci_name(rule["name"]))

    def __intermediate_redirects(self, redirects):
        """
        converts NetJSON redirect to
        UCI intermediate data structure
        """
        result = []
        for redirect in redirects:
            if "config_name" in redirect:
                del redirect["config_name"]
            resultdict = OrderedDict(
                (
                    (".name", self.__get_auto_name_redirect(redirect)),
                    (".type", "redirect"),
                )
            )
            if "proto" in redirect:
                # If proto is a single value, then force it not to be in a list so that
                # the UCI uses "option" rather than "list". If proto is only "tcp"
                # and"udp", we can force it to the single special value of "tcpudp".
                proto = redirect["proto"]
                if len(proto) == 1:
                    redirect["proto"] = proto[0]
                elif set(proto) == {"tcp", "udp"}:
                    redirect["proto"] = "tcpudp"

            resultdict.update(redirect)
            result.append(resultdict)

        return result

    def __get_auto_name_redirect(self, redirect):
        return "redirect_{0}".format(self._get_uci_name(redirect["name"]))

    def to_netjson_loop(self, block, result, index):
        result.setdefault("firewall", {})

        block.pop(".name")
        _type = block.pop(".type")

        if _type == "rule":
            rule = self.__netjson_rule(block)
            result["firewall"].setdefault("rules", [])
            result["firewall"]["rules"].append(rule)
        if _type == "zone":
            zone = self.__netjson_zone(block)
            result["firewall"].setdefault("zones", [])
            result["firewall"]["zones"].append(zone)
        if _type == "forwarding":
            forwarding = self.__netjson_forwarding(block)
            result["firewall"].setdefault("forwardings", [])
            result["firewall"]["forwardings"].append(forwarding)
        if _type == "redirect":
            redirect = self.__netjson_redirect(block)
            result["firewall"].setdefault("redirects", [])
            result["firewall"]["redirects"].append(redirect)

        return self.type_cast(result)

    def __netjson_rule(self, rule):
        for param in ["enabled", "utc_time"]:
            if param in rule:
                rule[param] = self.__netjson_generic_boolean(rule[param])

        if "proto" in rule:
            rule["proto"] = self.__netjson_generic_proto(rule["proto"])

        if "weekdays" in rule:
            rule["weekdays"] = self.__netjson_generic_weekdays(
                rule["weekdays"]
            )

        if "monthdays" in rule:
            rule["monthdays"] = self.__netjson_generic_monthdays(
                rule["monthdays"]
            )

        if "limit_burst" in rule:
            rule["limit_burst"] = int(rule["limit_burst"])

        return self.type_cast(rule)

    def __netjson_zone(self, zone):
        network = zone["network"]
        # network may be specified as a list in a single string e.g.
        #     option network 'wan wan6'
        # Here we ensure that network is always a list.
        if not isinstance(network, list):
            zone["network"] = network.split()

        for param in ["mtu_fix", "masq"]:
            if param in zone:
                zone[param] = self.__netjson_generic_boolean(zone[param])

        return self.type_cast(zone)

    def __netjson_forwarding(self, forwarding):
        return self.type_cast(forwarding)

    def __netjson_redirect(self, redirect):
        if "proto" in redirect:
            redirect["proto"] = self.__netjson_generic_proto(redirect["proto"])

        if "weekdays" in redirect:
            redirect["weekdays"] = self.__netjson_generic_weekdays(
                redirect["weekdays"]
            )

        if "monthdays" in redirect:
            redirect["monthdays"] = self.__netjson_generic_monthdays(
                redirect["monthdays"]
            )

        for param in ["utc_time", "reflection", "enabled"]:
            if param in redirect:
                redirect[param] = self.__netjson_generic_boolean(redirect[param])

        if "limit_burst" in redirect:
            redirect["limit_burst"] = int(redirect["limit_burst"])

        return self.type_cast(redirect)

    def __netjson_generic_boolean(self, boolean):
        # Per convention, boolean options may have one of the values '0', 'no', 'off',
        # 'false' or 'disabled' to specify a false value or '1' , 'yes', 'on', 'true' or
        # 'enabled' to specify a true value.
        # https://openwrt.org/docs/guide-user/base-system/uci
        return boolean in ["1", "yes", "on", "true", "enabled"]

    def __netjson_generic_proto(self, proto):
        if isinstance(proto, list):
            return proto.copy()
        else:
            if proto == "tcpudp":
                return ["tcp", "udp"]
            else:
                return proto.split()

    def __netjson_generic_weekdays(self, weekdays):
        if not isinstance(weekdays, list):
            wd = weekdays.split()
        else:
            wd = weekdays.copy()

        # UCI allows the first entry to be "!" which means negate the remaining entries
        if wd[0] == "!":
            all_days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
            wd = [day for day in all_days if day not in wd[1:]]

        return wd

    def __netjson_generic_monthdays(self, monthdays):
        if not isinstance(monthdays, list):
            md = monthdays.split()
        else:
            md = monthdays.copy()

        # UCI allows the first entry to be "!" which means negate the remaining entries
        if md[0] == "!":
            md = [int(day) for day in md[1:]]
            all_days = range(1, 32)
            md = [day for day in all_days if day not in md]
        else:
            md = [int(day) for day in md]

        return md
