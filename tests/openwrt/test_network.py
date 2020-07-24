import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.exceptions import ValidationError
from netjsonconfig.utils import _TabsMixin


class TestNetwork(unittest.TestCase, _TabsMixin):
    maxDiff = None
    _ula_netjson = {"general": {"ula_prefix": "fd8e:f40a:6701::/48"}}
    _ula_uci = """package network

config globals 'globals'
    option ula_prefix 'fd8e:f40a:6701::/48'
"""
    _ula_netjson_id = {
        "general": {"ula_prefix": "fd8e:f40a:6701::/48", "globals_id": "arbitrary_id"}
    }
    _ula_uci_id = """package network

config globals 'arbitrary_id'
    option ula_prefix 'fd8e:f40a:6701::/48'
"""

    def test_render_ula_prefix(self):
        o = OpenWrt(self._ula_netjson)
        expected = self._tabs(self._ula_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_ula_prefix(self):
        o = OpenWrt(native=self._ula_uci)
        self.assertEqual(o.config, self._ula_netjson)

    def test_render_ula_prefix_id(self):
        o = OpenWrt(self._ula_netjson_id)
        expected = self._tabs(self._ula_uci_id)
        self.assertEqual(o.render(), expected)

    def test_parse_ula_prefix_id(self):
        o = OpenWrt(native=self._ula_uci_id)
        self.assertEqual(o.config, self._ula_netjson_id)

    _routes_netjson = {
        "routes": [
            {
                "device": "eth1",
                "destination": "192.168.3.1/24",
                "next": "192.168.2.1",
                "cost": 0,
            },
            {
                "device": "eth1",
                "destination": "192.168.4.1/24",
                "next": "192.168.2.2",
                "cost": 2,
                "source": "192.168.1.10",
                "table": "2",
                "onlink": True,
                "mtu": "1450",
                "type": "unicast",
            },
            {
                "name": "arbitrary_name",
                "device": "eth1",
                "destination": "fd89::1/128",
                "next": "fd88::1",
                "cost": 0,
            },
            {
                "device": "eth1",
                "destination": "fd90::1/128",
                "next": "fd88::2",
                "cost": 3,
                "source": "fd87::10",
            },
        ]
    }
    _routes_uci = """package network

config route 'route1'
    option gateway '192.168.2.1'
    option interface 'eth1'
    option metric '0'
    option netmask '255.255.255.0'
    option target '192.168.3.1'

config route 'route2'
    option gateway '192.168.2.2'
    option interface 'eth1'
    option metric '2'
    option mtu '1450'
    option netmask '255.255.255.0'
    option onlink '1'
    option source '192.168.1.10'
    option table '2'
    option target '192.168.4.1'
    option type 'unicast'

config route6 'arbitrary_name'
    option gateway 'fd88::1'
    option interface 'eth1'
    option metric '0'
    option target 'fd89::1/128'

config route6 'route4'
    option gateway 'fd88::2'
    option interface 'eth1'
    option metric '3'
    option source 'fd87::10'
    option target 'fd90::1/128'
"""

    def test_render_routes(self):
        o = OpenWrt(self._routes_netjson)
        expected = self._tabs(self._routes_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_routes(self):
        o = OpenWrt(native=self._routes_uci)
        self.assertEqual(o.config, self._routes_netjson)

    _rules_netjson = {
        "ip_rules": [
            {
                "in": "eth0",
                "out": "eth1",
                "src": "192.168.1.0/24",
                "dest": "192.168.2.0/24",
                "tos": 2,
                "mark": "0x0/0x1",
                "invert": True,
                "lookup": "0",
                "action": "blackhole",
            },
            {"src": "192.168.1.0/24", "dest": "192.168.3.0/24", "goto": 0},
            {
                "name": "arbitrary_name",
                "in": "vpn",
                "dest": "fdca:1234::/64",
                "action": "prohibit",
            },
            {"in": "vpn", "src": "fdca:1235::/64", "action": "prohibit"},
        ]
    }
    _rules_uci = """package network

config rule 'rule1'
    option action 'blackhole'
    option dest '192.168.2.0/24'
    option in 'eth0'
    option invert '1'
    option lookup '0'
    option mark '0x0/0x1'
    option out 'eth1'
    option src '192.168.1.0/24'
    option tos '2'

config rule 'rule2'
    option dest '192.168.3.0/24'
    option goto '0'
    option src '192.168.1.0/24'

config rule6 'arbitrary_name'
    option action 'prohibit'
    option dest 'fdca:1234::/64'
    option in 'vpn'

config rule6 'rule4'
    option action 'prohibit'
    option in 'vpn'
    option src 'fdca:1235::/64'
"""

    def test_render_rules(self):
        o = OpenWrt(self._rules_netjson)
        expected = self._tabs(self._rules_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_rules(self):
        o = OpenWrt(native=self._rules_uci)
        self.assertEqual(o.config, self._rules_netjson)

    def test_rules_no_src_dest(self):
        o = OpenWrt(
            {
                "ip_rules": [
                    {
                        "in": "eth0",
                        "out": "eth1",
                        "tos": 2,
                        "mark": "0x0/0x1",
                        "invert": True,
                        "lookup": "0",
                        "action": "blackhole",
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config rule 'rule1'
    option action 'blackhole'
    option in 'eth0'
    option invert '1'
    option lookup '0'
    option mark '0x0/0x1'
    option out 'eth1'
    option tos '2'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_render_rule_wrong(self):
        rule = {
            "ip_rules": [
                {
                    "in": "eth0",
                    "out": "eth1",
                    "src": "wrong",
                    "dest": "wrong1",
                    "tos": 2,
                    "action": "blackhole",
                }
            ]
        }
        o = OpenWrt(rule)
        with self.assertRaisesRegex(ValidationError, "'wrong' is not a 'cidr'"):
            o.validate()
        rule['ip_rules'][0]['src'] = '192.168.1.0/24'
        o = OpenWrt(rule)
        with self.assertRaisesRegexp(ValidationError, "'wrong1' is not a 'cidr'"):
            o.validate()
        # fix 'dest' and expect no ValidationError raised
        rule['ip_rules'][0]['dest'] = '192.168.1.0/24'
        o = OpenWrt(rule)
        o.validate()

    def test_parse_rules_zone(self):
        with self.assertRaisesRegexp(ValidationError, "'wrong' is not a 'cidr'"):
            OpenWrt(
                native="""package network

config rule 'rule1'
    option action 'blackhole'
    option dest 'wrong'
    option in 'eth0'
    option out 'eth1'
    option src 'wrong'
    option tos '2'
"""
            )

    _switch_netjson = {
        "switch": [
            {
                "name": "switch0",
                "reset": True,
                "enable_vlan": True,
                "vlan": [
                    {"device": "switch0", "vlan": 1, "ports": "0t 2 3 4 5"},
                    {
                        "device": "switch0",
                        "vlan": 2,
                        "vid": None,  # ``None`` or empty string disable ``vid``
                        "ports": "0t 1",
                    },
                ],
            },
            {
                "id": "s1",
                "name": "switch1",
                "reset": True,
                "enable_vlan": True,
                "vlan": [
                    {
                        "id": "v1",
                        "device": "switch1",
                        "vlan": 3,
                        "vid": 130,
                        "ports": "0t 6 7",
                    }
                ],
            },
        ]
    }
    _switch_uci = """package network

config switch 'switch0'
    option enable_vlan '1'
    option name 'switch0'
    option reset '1'

config switch_vlan 'switch0_vlan1'
    option device 'switch0'
    option ports '0t 2 3 4 5'
    option vid '1'
    option vlan '1'

config switch_vlan 'switch0_vlan2'
    option device 'switch0'
    option ports '0t 1'
    option vlan '2'

config switch 's1'
    option enable_vlan '1'
    option name 'switch1'
    option reset '1'

config switch_vlan 'v1'
    option device 'switch1'
    option ports '0t 6 7'
    option vid '130'
    option vlan '3'
"""

    _switch_uci_reorder = """package network

config switch_vlan 'switch0_vlan1'
    option device 'switch0'
    option ports '0t 2 3 4 5'
    option vid '1'
    option vlan '1'

config switch 'switch0'
    option enable_vlan '1'
    option name 'switch0'
    option reset '1'
"""

    _switch_netjson_reorder = {
        "switch": [
            {
                "name": "switch0",
                "reset": True,
                "enable_vlan": True,
                "vlan": [{"device": "switch0", "vlan": 1, "ports": "0t 2 3 4 5"}],
            }
        ]
    }

    def test_render_switch(self):
        o = OpenWrt(self._switch_netjson)
        expected = self._tabs(self._switch_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_switch(self):
        o = OpenWrt(native=self._switch_uci)
        self.assertEqual(o.config, self._switch_netjson)

    def test_parse_switch_reorder(self):
        o = OpenWrt(native=self._switch_uci_reorder)
        self.assertEqual(o.config, self._switch_netjson_reorder)
