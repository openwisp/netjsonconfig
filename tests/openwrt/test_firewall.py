import textwrap
import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestFirewall(unittest.TestCase, _TabsMixin):
    maxDiff = None

    _rule_1_netjson = {
        "firewall": {
            "rules": [
                {
                    "name": "Allow-MLD",
                    "src": "wan",
                    "src_ip": "fe80::/10",
                    "proto": ["icmp"],
                    "icmp_type": ["130/0", "131/0", "132/0", "143/0"],
                    "target": "ACCEPT",
                    "family": "ipv6",
                }
            ]
        }
    }

    _rule_1_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config rule 'rule_Allow_MLD'
            option name 'Allow-MLD'
            option src 'wan'
            option src_ip 'fe80::/10'
            option proto 'icmp'
            list icmp_type '130/0'
            list icmp_type '131/0'
            list icmp_type '132/0'
            list icmp_type '143/0'
            option target 'ACCEPT'
            option family 'ipv6'
        """
    )

    def test_render_rule_1(self):
        o = OpenWrt(self._rule_1_netjson)
        expected = self._tabs(self._rule_1_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_rule_1(self):
        o = OpenWrt(native=self._rule_1_uci)
        self.assertEqual(o.config, self._rule_1_netjson)

    _rule_2_netjson = {
        "firewall": {
            "rules": [
                {
                    "name": "Allow-DHCPv6",
                    "src": "wan",
                    "src_ip": "fc00::/6",
                    "dest_ip": "fc00::/6",
                    "dest_port": "546",
                    "proto": ["udp"],
                    "target": "ACCEPT",
                    "family": "ipv6",
                }
            ]
        }
    }

    _rule_2_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config rule 'rule_Allow_DHCPv6'
            option name 'Allow-DHCPv6'
            option src 'wan'
            option src_ip 'fc00::/6'
            option dest_ip 'fc00::/6'
            option dest_port '546'
            option proto 'udp'
            option target 'ACCEPT'
            option family 'ipv6'
        """
    )

    def test_render_rule_2(self):
        o = OpenWrt(self._rule_2_netjson)
        expected = self._tabs(self._rule_2_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_rule_2(self):
        o = OpenWrt(native=self._rule_2_uci)
        self.assertEqual(o.config, self._rule_2_netjson)

    _rule_3_netjson = {
        "firewall": {
            "rules": [
                {
                    "name": "Allow-Ping",
                    "src": "wan",
                    "proto": ["icmp"],
                    "family": "ipv4",
                    "icmp_type": ["echo-request"],
                    "target": "ACCEPT",
                    "enabled": False,
                }
            ]
        }
    }

    _rule_3_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config rule 'rule_Allow_Ping'
            option name 'Allow-Ping'
            option src 'wan'
            option proto 'icmp'
            option family 'ipv4'
            list icmp_type 'echo-request'
            option target 'ACCEPT'
            option enabled '0'
        """
    )

    def test_render_rule_3(self):
        o = OpenWrt(self._rule_3_netjson)
        expected = self._tabs(self._rule_3_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_rule_3(self):
        o = OpenWrt(native=self._rule_3_uci)
        self.assertEqual(o.config, self._rule_3_netjson)

    _rule_4_netjson = {
        "firewall": {
            "rules": [
                {
                    "name": "Allow-Isolated-DHCP",
                    "src": "isolated",
                    "proto": ["udp"],
                    "dest_port": "67-68",
                    "target": "ACCEPT",
                }
            ]
        }
    }

    _rule_4_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config rule 'rule_Allow_Isolated_DHCP'
            option name 'Allow-Isolated-DHCP'
            option src 'isolated'
            option proto 'udp'
            option dest_port '67-68'
            option target 'ACCEPT'
        """
    )

    def test_render_rule_4(self):
        o = OpenWrt(self._rule_4_netjson)
        expected = self._tabs(self._rule_4_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_rule_4(self):
        o = OpenWrt(native=self._rule_4_uci)
        self.assertEqual(o.config, self._rule_4_netjson)

    _zone_1_netjson = {
        "firewall": {
            "zones": [
                {
                    "name": "lan",
                    "input": "ACCEPT",
                    "output": "ACCEPT",
                    "forward": "ACCEPT",
                    "network": ["lan"],
                    "mtu_fix": True,
                }
            ]
        }
    }

    _zone_1_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config zone 'zone_lan'
            option name 'lan'
            option input 'ACCEPT'
            option output 'ACCEPT'
            option forward 'ACCEPT'
            option network 'lan'
            option mtu_fix '1'
        """
    )

    def test_render_zone_1(self):
        o = OpenWrt(self._zone_1_netjson)
        expected = self._tabs(self._zone_1_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_zone_1(self):
        o = OpenWrt(native=self._zone_1_uci)
        self.assertEqual(o.config, self._zone_1_netjson)

    _zone_2_netjson = {
        "firewall": {
            "zones": [
                {
                    "name": "wan",
                    "input": "DROP",
                    "output": "ACCEPT",
                    "forward": "DROP",
                    "network": ["wan", "wan6"],
                    "mtu_fix": True,
                    "masq": True,
                }
            ]
        }
    }

    _zone_2_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config zone 'zone_wan'
            option name 'wan'
            option input 'DROP'
            option output 'ACCEPT'
            option forward 'DROP'
            list network 'wan'
            list network 'wan6'
            option mtu_fix '1'
            option masq '1'
        """
    )

    # This one is the same as _zone_2_uci with the exception that the "network"
    # parameter is specified as a single string.
    _zone_3_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config zone 'zone_wan'
            option name 'wan'
            option input 'DROP'
            option output 'ACCEPT'
            option forward 'DROP'
            option network 'wan wan6'
            option mtu_fix '1'
            option masq '1'
        """
    )

    def test_render_zone_2(self):
        o = OpenWrt(self._zone_2_netjson)
        expected = self._tabs(self._zone_2_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_zone_2(self):
        o = OpenWrt(native=self._zone_2_uci)
        self.assertEqual(o.config, self._zone_2_netjson)

    def test_parse_zone_3(self):
        o = OpenWrt(native=self._zone_3_uci)
        self.assertEqual(o.config, self._zone_2_netjson)
