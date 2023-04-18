import textwrap
import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.exceptions import ValidationError
from netjsonconfig.utils import _TabsMixin


class TestFirewall(unittest.TestCase, _TabsMixin):
    maxDiff = None

    _defaults_1_netjson = {
        "firewall": {
            "defaults": {
                "input": "ACCEPT",
                "forward": "REJECT",
                "output": "ACCEPT",
                "synflood_protect": True,
            }
        }
    }

    _defaults_1_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'
            option input 'ACCEPT'
            option forward 'REJECT'
            option output 'ACCEPT'
            option synflood_protect '1'
       """
    )

    def test_render_defaults_1(self):
        o = OpenWrt(self._defaults_1_netjson)
        expected = self._tabs(self._defaults_1_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_defaults_1(self):
        o = OpenWrt(native=self._defaults_1_uci)
        self.assertEqual(o.config, self._defaults_1_netjson)

    _defaults_2_netjson = {
        "firewall": {
            "defaults": {
                "input": "ACCEPT",
                "output": "ACCEPT",
                "forward": "REJECT",
                "custom_chains": True,
                "drop_invalid": True,
                "synflood_protect": True,
                "synflood_burst": 50,
                "tcp_ecn": True,
                "tcp_syncookies": True,
                "tcp_window_scaling": True,
                "disable_ipv6": False,
                "flow_offloading": False,
                "flow_offloading_hw": False,
                "auto_helper": True,
            }
        }
    }

    _defaults_2_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'
            option input 'ACCEPT'
            option output 'ACCEPT'
            option forward 'REJECT'
            option custom_chains '1'
            option drop_invalid '1'
            option synflood_protect '1'
            option synflood_burst '50'
            option tcp_ecn '1'
            option tcp_syncookies '1'
            option tcp_window_scaling '1'
            option disable_ipv6 '0'
            option flow_offloading '0'
            option flow_offloading_hw '0'
            option auto_helper '1'
       """
    )

    def test_render_defaults_2(self):
        o = OpenWrt(self._defaults_2_netjson)
        expected = self._tabs(self._defaults_2_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_defaults_2(self):
        o = OpenWrt(native=self._defaults_2_uci)
        self.assertEqual(o.config, self._defaults_2_netjson)

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

        config rule 'Allow_MLD'
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

        config rule 'Allow_DHCPv6'
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

        config rule 'Allow_Ping'
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

        config rule 'Allow_Isolated_DHCP'
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

    _rule_5_netjson = {
        "firewall": {
            "rules": [
                {
                    "name": "Allow-Isolated-DHCP",
                    "src_ip": "10.10.10.10",
                    "src_mac": "fc:aa:14:18:12:98",
                    "src": "isolated",
                    "proto": ["udp"],
                    "dest_port": "67-68",
                    "target": "ACCEPT",
                }
            ]
        }
    }

    _rule_5_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config rule 'Allow_Isolated_DHCP'
            option name 'Allow-Isolated-DHCP'
            option src_ip '10.10.10.10'
            option src_mac 'fc:aa:14:18:12:98'
            option src 'isolated'
            option proto 'udp'
            option dest_port '67-68'
            option target 'ACCEPT'
        """
    )

    def test_render_rule_5(self):
        o = OpenWrt(self._rule_5_netjson)
        expected = self._tabs(self._rule_5_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_rule_5(self):
        o = OpenWrt(native=self._rule_5_uci)
        self.assertEqual(o.config, self._rule_5_netjson)

    _rule_6_netjson = {
        "firewall": {
            "rules": [
                {
                    "name": "Allow-Isolated-DHCP",
                    "src_ip": "10.10.10.10",
                    "src_mac": "fc:aa:14:18:12:98",
                    "src": "isolated",
                    "proto": ["udp"],
                    "dest_port": "67-68",
                    "target": "ACCEPT",
                    "dest": "dest_zone",
                    "dest_ip": "192.168.1.2",
                    "ipset": "my_ipset",
                    "mark": "DROP",
                    "start_date": "2021-01-21",
                    "stop_date": "2021-01-22",
                    "start_time": "01:01:01",
                    "stop_time": "11:11:11",
                    "weekdays": ["sun", "mon"],
                    "monthdays": [2, 10],
                    "utc_time": True,
                    "family": "any",
                    "limit": "3/second",
                    "limit_burst": 30,
                    "enabled": True,
                }
            ]
        }
    }

    _rule_6_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config rule 'Allow_Isolated_DHCP'
            option name 'Allow-Isolated-DHCP'
            option src_ip '10.10.10.10'
            option src_mac 'fc:aa:14:18:12:98'
            option src 'isolated'
            option proto 'udp'
            option dest_port '67-68'
            option target 'ACCEPT'
            option dest 'dest_zone'
            option dest_ip '192.168.1.2'
            option ipset 'my_ipset'
            option mark 'DROP'
            option start_date '2021-01-21'
            option stop_date '2021-01-22'
            option start_time '01:01:01'
            option stop_time '11:11:11'
            list weekdays 'sun'
            list weekdays 'mon'
            list monthdays '2'
            list monthdays '10'
            option utc_time '1'
            option family 'any'
            option limit '3/second'
            option limit_burst '30'
            option enabled '1'
        """
    )

    def test_render_rule_6(self):
        o = OpenWrt(self._rule_6_netjson)
        expected = self._tabs(self._rule_6_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_rule_6(self):
        o = OpenWrt(native=self._rule_6_uci)
        self.assertEqual(o.config, self._rule_6_netjson)

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

        config zone 'lan'
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

        config zone 'wan'
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

        config zone 'wan'
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

    _forwarding_1_netjson = {
        "firewall": {
            "forwardings": [{"name": "isolated-wan", "src": "isolated", "dest": "wan"}]
        }
    }

    _forwarding_1_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config forwarding 'isolated_wan'
            option name 'isolated-wan'
            option src 'isolated'
            option dest 'wan'
        """
    )

    def test_render_forwarding_1(self):
        o = OpenWrt(self._forwarding_1_netjson)
        expected = self._tabs(self._forwarding_1_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_forwarding_1(self):
        o = OpenWrt(native=self._forwarding_1_uci)
        self.assertEqual(o.config, self._forwarding_1_netjson)

    _forwarding_2_netjson = {
        "firewall": {
            "forwardings": [
                {
                    "name": "isolated-wan-ipv4",
                    "src": "isolated",
                    "dest": "wan",
                    "family": "ipv4",
                }
            ]
        }
    }

    _forwarding_2_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config forwarding 'isolated_wan_ipv4'
            option name 'isolated-wan-ipv4'
            option src 'isolated'
            option dest 'wan'
            option family 'ipv4'
        """
    )

    def test_render_forwarding_2(self):
        o = OpenWrt(self._forwarding_2_netjson)
        expected = self._tabs(self._forwarding_2_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_forwarding_2(self):
        o = OpenWrt(native=self._forwarding_2_uci)
        self.assertEqual(o.config, self._forwarding_2_netjson)

    _forwarding_3_netjson = {
        "firewall": {
            "forwardings": [
                {
                    "name": "lan-wan-any",
                    "src": "lan",
                    "dest": "wan",
                    "family": "any",
                    "enabled": False,
                }
            ]
        }
    }

    _forwarding_3_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config forwarding 'lan_wan_any'
            option name 'lan-wan-any'
            option src 'lan'
            option dest 'wan'
            option family 'any'
            option enabled '0'
        """
    )

    def test_render_forwarding_3(self):
        o = OpenWrt(self._forwarding_3_netjson)
        expected = self._tabs(self._forwarding_3_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_forwarding_3(self):
        o = OpenWrt(native=self._forwarding_3_uci)
        self.assertEqual(o.config, self._forwarding_3_netjson)

    _forwarding_4_netjson = {
        "firewall": {
            "forwardings": [
                {
                    "name": "forward_name",
                    "src": "lan",
                    "dest": "wan",
                    "family": "any",
                    "enabled": False,
                }
            ]
        }
    }

    _forwarding_4_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config forwarding 'forward_name'
            option name 'forward_name'
            option src 'lan'
            option dest 'wan'
            option family 'any'
            option enabled '0'
        """
    )

    def test_render_forwarding_4(self):
        o = OpenWrt(self._forwarding_4_netjson)
        expected = self._tabs(self._forwarding_4_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_forwarding_4(self):
        o = OpenWrt(native=self._forwarding_4_uci)
        self.assertEqual(o.config, self._forwarding_4_netjson)

    def test_forwarding_validation_error(self):
        o = OpenWrt(
            {
                "firewall": {
                    "forwardings": [{"src": "lan", "dest": "wan", "family": "XXXXXX"}]
                }
            }
        )
        with self.assertRaises(ValidationError):
            o.validate()

    _redirect_1_netjson = {
        "firewall": {
            "redirects": [
                {
                    "name": "Adblock DNS, port 53",
                    "src": "lan",
                    "proto": ["tcp", "udp"],
                    "src_dport": "53",
                    "dest_port": "53",
                    "target": "DNAT",
                }
            ]
        }
    }

    _redirect_1_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config redirect 'Adblock DNS, port 53'
            option name 'Adblock DNS, port 53'
            option src 'lan'
            option proto 'tcpudp'
            option src_dport '53'
            option dest_port '53'
            option target 'DNAT'
        """
    )

    def test_render_redirect_1(self):
        o = OpenWrt(self._redirect_1_netjson)
        expected = self._tabs(self._redirect_1_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_redirect_1(self):
        o = OpenWrt(native=self._redirect_1_uci)
        self.assertEqual(o.config, self._redirect_1_netjson)

    _redirect_2_netjson = {
        "firewall": {
            "redirects": [
                {
                    "name": "Adblock DNS, port 53",
                    "src": "lan",
                    "proto": ["tcp", "udp"],
                    "src_dport": "53",
                    "dest_port": "53",
                    "target": "DNAT",
                    # Contrived, unrealistic example for testing
                    "weekdays": ["mon", "tue", "wed"],
                    "monthdays": [1, 2, 3, 29, 30],
                }
            ]
        }
    }

    _redirect_2_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config redirect 'Adblock DNS, port 53'
            option name 'Adblock DNS, port 53'
            option src 'lan'
            option proto 'tcpudp'
            option src_dport '53'
            option dest_port '53'
            option target 'DNAT'
            list weekdays 'mon'
            list weekdays 'tue'
            list weekdays 'wed'
            list monthdays '1'
            list monthdays '2'
            list monthdays '3'
            list monthdays '29'
            list monthdays '30'
        """
    )

    def test_render_redirect_2(self):
        o = OpenWrt(self._redirect_2_netjson)
        expected = self._tabs(self._redirect_2_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_redirect_2(self):
        o = OpenWrt(native=self._redirect_2_uci)
        self.assertEqual(o.config, self._redirect_2_netjson)

    def test_redirect_weekdays_validation_error_1(self):
        o = OpenWrt({"firewall": {"redirects": [{"weekdays": ["mon", "xxx"]}]}})
        with self.assertRaises(ValidationError):
            o.validate()

    def test_redirect_weekdays_validation_error_2(self):
        o = OpenWrt({"firewall": {"redirects": [{"weekdays": ["mon", 1]}]}})
        with self.assertRaises(ValidationError):
            o.validate()

    def test_redirect_monthdays_validation_error_1(self):
        o = OpenWrt({"firewall": {"redirects": [{"monthdays": [2, 8, 32]}]}})
        with self.assertRaises(ValidationError):
            o.validate()

    def test_redirect_monthdays_validation_error_2(self):
        o = OpenWrt({"firewall": {"redirects": [{"monthdays": [0, 2, 8]}]}})
        with self.assertRaises(ValidationError):
            o.validate()

    _redirect_3_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config redirect 'Adblock DNS, port 53'
            option name 'Adblock DNS, port 53'
            option src 'lan'
            option proto 'tcpudp'
            option src_dport '53'
            option dest_port '53'
            option target 'DNAT'
            option weekdays '! mon tue wed'
            option monthdays '! 1 2 3 4 5'
        """
    )

    _redirect_3_netjson = {
        "firewall": {
            "redirects": [
                {
                    "name": "Adblock DNS, port 53",
                    "src": "lan",
                    "proto": ["tcp", "udp"],
                    "src_dport": "53",
                    "dest_port": "53",
                    "target": "DNAT",
                    "weekdays": ["sun", "thu", "fri", "sat"],
                    "monthdays": [
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23,
                        24,
                        25,
                        26,
                        27,
                        28,
                        29,
                        30,
                        31,
                    ],
                }
            ]
        }
    }

    def test_parse_redirect_3(self):
        o = OpenWrt(native=self._redirect_3_uci)
        self.assertEqual(o.config, self._redirect_3_netjson)

    _redirect_4_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config redirect 'Adblock DNS, port 53'
            option name 'Adblock DNS, port 53'
            option src 'lan'
            option proto 'tcpudp'
            option src_dport '53'
            option dest_port '53'
            option target 'DNAT'
            list weekdays 'mon'
            list weekdays 'tue'
            list weekdays 'wed'
            list monthdays '1'
            list monthdays '2'
            list monthdays '31'
            option src_ip '192.168.1.1'
            option src_dip '192.168.1.1'
            option src_mac 'AA:AA:AA:AA:AA:AA'
            option src_port '1-1064'
            option dest 'wan'
            option dest_ip '10.0.0.1'
            option ipset 'myipset'
            option mark '0xff'
            option start_date '2020-02-02'
            option stop_date '2020-03-02'
            option start_time '12:12:12'
            option stop_time '23:23:23'
            option utc_time '1'
            option family 'any'
            option reflection '0'
            option reflection_src 'external'
            option limit '3/sec'
            option limit_burst '5'
            option enabled '0'
        """
    )

    _redirect_4_netjson = {
        "firewall": {
            "redirects": [
                {
                    "name": "Adblock DNS, port 53",
                    "src": "lan",
                    "proto": ["tcp", "udp"],
                    "src_dport": "53",
                    "dest_port": "53",
                    "target": "DNAT",
                    "weekdays": ["mon", "tue", "wed"],
                    "monthdays": [1, 2, 31],
                    "src_ip": "192.168.1.1",
                    "src_dip": "192.168.1.1",
                    "src_mac": "AA:AA:AA:AA:AA:AA",
                    "src_port": "1-1064",
                    "dest": "wan",
                    "dest_ip": "10.0.0.1",
                    "ipset": "myipset",
                    "mark": "0xff",
                    "start_date": "2020-02-02",
                    "stop_date": "2020-03-02",
                    "start_time": "12:12:12",
                    "stop_time": "23:23:23",
                    "utc_time": True,
                    "family": "any",
                    "reflection": False,
                    "reflection_src": "external",
                    "limit": "3/sec",
                    "limit_burst": 5,
                    "enabled": False,
                }
            ]
        }
    }

    def test_render_redirect_4(self):
        o = OpenWrt(self._redirect_4_netjson)
        expected = self._tabs(self._redirect_4_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_redirect_4(self):
        o = OpenWrt(native=self._redirect_4_uci)
        self.assertEqual(o.config, self._redirect_4_netjson)

    _include_1_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config include 'Include Test'
            option name 'Include Test'
            option type 'script'
            option family 'any'
            option path '/a/b/c.ipt'
            option reload '1'
            option enabled '0'
        """
    )

    _include_1_netjson = {
        "firewall": {
            "includes": [
                {
                    "name": "Include Test",
                    "type": "script",
                    "family": "any",
                    "path": "/a/b/c.ipt",
                    "reload": True,
                    "enabled": False,
                }
            ]
        }
    }

    def test_render_include_1(self):
        o = OpenWrt(self._include_1_netjson)
        expected = self._tabs(self._include_1_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_include_1(self):
        o = OpenWrt(native=self._include_1_uci)
        self.assertEqual(o.config, self._include_1_netjson)
