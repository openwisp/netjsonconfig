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
    _uci_types = ["defaults", "forwarding", "zone", "rule", "redirect", "include"]
    _schema = schema["properties"]["firewall"]

    def to_intermediate_loop(self, block, result, index=None):
        defaults = self.__intermediate_defaults(block.pop("defaults", {}))
        forwardings = self.__intermediate_forwardings(block.pop("forwardings", {}))
        zones = self.__intermediate_zones(block.pop("zones", {}))
        rules = self.__intermediate_rules(block.pop("rules", {}))
        redirects = self.__intermediate_redirects(block.pop("redirects", {}))
        includes = self.__intermediate_includes(block.pop("includes", {}))
        result.setdefault("firewall", [])
        result["firewall"] = (
            defaults + forwardings + zones + rules + redirects + includes
        )
        return result

    def __intermediate_defaults(self, defaults):
        """
        converts NetJSON defaults to
        UCI intermediate data structure
        """
        result = OrderedDict(((".name", "defaults"), (".type", "defaults")))
        result.update(defaults)
        return [result]

    def __intermediate_forwardings(self, forwardings):
        """
        converts NetJSON forwarding to
        UCI intermediate data structure
        """
        result = []
        for forwarding in forwardings:
            if "name" in forwarding:
                resultdict = OrderedDict(
                    (
                        (".name", self._get_uci_name(forwarding["name"])),
                        (".type", "forwarding"),
                    )
                )
            else:
                resultdict = OrderedDict(
                    (
                        # if the forwarding has no name, will assign src_dest as name
                        (".name", forwarding["src"] + "_" + forwarding["dest"]),
                        (".type", "forwarding"),
                    )
                )
            resultdict.update(forwarding)
            result.append(resultdict)
        return result

    def __intermediate_zones(self, zones):
        """
        converts NetJSON zone to
        UCI intermediate data structure
        """
        result = []
        for zone in zones:
            resultdict = OrderedDict(
                ((".name", self._get_uci_name(zone["name"])), (".type", "zone"))
            )
            # If network contains only a single value, force the use of a UCI "option"
            # rather than "list"".
            network = zone["network"] if "network" in zone else []
            if len(network) == 1:
                zone["network"] = network[0]
            resultdict.update(zone)
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
                ((".name", self._get_uci_name(rule["name"])), (".type", "rule"))
            )
            if "proto" in rule:
                # If proto is a single value, then force it not to be in a list so that
                # the UCI uses "option" rather than "list"
                proto = rule["proto"]
                if len(proto) == 1:
                    rule["proto"] = proto[0]

            # If src_ip and dest_ip contains only a single value, force the use of a UCI "option"
            # rather than "list".
            for option in ["src_ip", "dest_ip"]:
                if option in rule:
                    ip = rule[option]
                    if len(ip) == 1:
                        rule[option] = ip[0]
            resultdict.update(rule)
            result.append(resultdict)
        return result

    def __intermediate_redirects(self, redirects):
        """
        converts NetJSON redirect to
        UCI intermediate data structure
        """
        result = []
        for redirect in redirects:
            resultdict = OrderedDict(
                (
                    (".name", self._get_uci_name(redirect["name"])),
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

            # If src_ip and dest_ip contains only a single value, force the use of a UCI "option"
            # rather than "list".
            for option in ["src_ip", "dest_ip"]:
                if option in redirect:
                    ip = redirect[option]
                    if len(ip) == 1:
                        redirect[option] = ip[0]

            resultdict.update(redirect)
            result.append(resultdict)

        return result

    def __intermediate_includes(self, includes):
        """
        converts NetJSON include to
        UCI intermediate data structure
        """
        result = []
        for include in includes:
            if "name" in include:
                resultdict = OrderedDict(
                    (
                        (".name", self._get_uci_name(include["name"])),
                        (".type", "include"),
                    )
                )
            else:
                resultdict = OrderedDict(((".type", "include"),))
            resultdict.update(include)
            result.append(resultdict)
        return result

    def to_netjson_loop(self, block, result, index):
        result.setdefault("firewall", {})

        block.pop(".name")
        _type = block.pop(".type")

        if _type == "defaults":
            defaults = self.__netjson_defaults(block)
            if defaults:  # note: default section can be empty
                result["firewall"].setdefault("defaults", {})
                result["firewall"]["defaults"].update(defaults)
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
        if _type == "include":
            include = self.__netjson_include(block)
            result["firewall"].setdefault("includes", [])
            result["firewall"]["includes"].append(include)

        return self.type_cast(result)

    def __netjson_defaults(self, defaults):
        for param in [
            "drop_invalid",
            "synflood_protect",
            "tcp_syncookies",
            "tcp_ecn",
            "tcp_window_scaling",
            "accept_redirects",
            "accept_source_route",
            "custom_chains",
            "disable_ipv6",
            "flow_offloading",
            "flow_offloading_hw",
            "auto_helper",
        ]:
            if param in defaults:
                defaults[param] = self.__netjson_generic_boolean(defaults[param])
        for param in ["synflood_limit", "synflood_burst", "synflood_rate"]:
            if param in defaults:
                defaults[param] = int(defaults[param])
        return self.type_cast(defaults)

    def __netjson_rule(self, rule):

        for option in ["src_ip", "dest_ip"]:
            if option in rule:
                ip = rule[option]
                if not isinstance(ip, list):
                    rule[option] = ip.split()

        for param in ["enabled", "utc_time"]:
            if param in rule:
                rule[param] = self.__netjson_generic_boolean(rule[param])

        if "proto" in rule:
            rule["proto"] = self.__netjson_generic_proto(rule["proto"])

        if "weekdays" in rule:
            rule["weekdays"] = self.__netjson_generic_weekdays(rule["weekdays"])

        if "monthdays" in rule:
            rule["monthdays"] = self.__netjson_generic_monthdays(rule["monthdays"])

        if "limit_burst" in rule:
            rule["limit_burst"] = int(rule["limit_burst"])

        return self.type_cast(rule)

    def __netjson_zone(self, zone):
        network = zone["network"] if "network" in zone else []
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
        if "enabled" in forwarding:
            forwarding["enabled"] = self.__netjson_generic_boolean(
                forwarding["enabled"]
            )
        return self.type_cast(forwarding)

    def __netjson_redirect(self, redirect):
        for option in ["src_ip", "dest_ip"]:
            if option in redirect:
                ip = redirect[option]
                if not isinstance(ip, list):
                    redirect[option] = ip.split()

        if "proto" in redirect:
            redirect["proto"] = self.__netjson_generic_proto(redirect["proto"])

        if "weekdays" in redirect:
            redirect["weekdays"] = self.__netjson_generic_weekdays(redirect["weekdays"])

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

    def __netjson_include(self, include):
        for param in ["reload", "enabled"]:
            if param in include:
                include[param] = self.__netjson_generic_boolean(include[param])

        return self.type_cast(include)

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
