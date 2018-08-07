import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestDefault(unittest.TestCase, _TabsMixin):
    maxDiff = None

    def test_render_default(self):
        o = OpenWrt({
            "luci": [
                {
                    "config_name": "core",
                    "config_value": "main",
                    "lang": "auto",
                    "resourcebase": "/luci-static/resources",
                    "mediaurlbase": "/luci-static/bootstrap",
                    "number": 4,
                    "boolean": True
                }
            ],
            "firewall": {
                "rules": [
                    {
                        "config_name": "rule",
                        "name": "Allow-MLD",
                        "src": "wan",
                        "proto": "icmp",
                        "src_ip": "fe80::/10",
                        "family": "ipv6",
                        "target": "ACCEPT",
                        "icmp_type": [
                            "130/0",
                            "131/0",
                            "132/0",
                            "143/0"
                        ]
                    },
                    {
                        "config_name": "rule",
                        "name": "Rule2",
                        "src": "wan",
                        "proto": "icmp",
                        "src_ip": "192.168.1.1/24",
                        "family": "ipv4",
                        "target": "ACCEPT",
                        "icmp_type": [
                            "130/0",
                            "131/0",
                            "132/0",
                            "143/0"
                        ]
                    }
                ]
            }
        })
        expected = self._tabs("""package firewall

config rule 'rule_Allow_MLD'
    option family 'ipv6'
    list icmp_type '130/0'
    list icmp_type '131/0'
    list icmp_type '132/0'
    list icmp_type '143/0'
    option name 'Allow-MLD'
    option proto 'icmp'
    option src 'wan'
    option src_ip 'fe80::/10'
    option target 'ACCEPT'

config rule 'rule_Rule2'
    option family 'ipv4'
    list icmp_type '130/0'
    list icmp_type '131/0'
    list icmp_type '132/0'
    list icmp_type '143/0'
    option name 'Rule2'
    option proto 'icmp'
    option src 'wan'
    option src_ip '192.168.1.1/24'
    option target 'ACCEPT'

package luci

config core 'main'
    option boolean '1'
    option lang 'auto'
    option mediaurlbase '/luci-static/bootstrap'
    option number '4'
    option resourcebase '/luci-static/resources'
""")
        self.assertEqual(o.render(), expected)
        # try a second time to ensure that the usage of dict.pop
        # in templates does not cause any issue
        self.assertEqual(o.render(), expected)

    def test_parse_default(self):
        native = self._tabs("""package firewall

config rule 'rule_1'
    option family 'ipv6'
    list icmp_type '130/0'
    list icmp_type '131/0'
    list icmp_type '132/0'
    list icmp_type '143/0'
    option name 'Allow-MLD'
    option proto 'icmp'
    option src 'wan'
    option src_ip 'fe80::/10'
    option target 'ACCEPT'

package luci

config core 'main'
    option boolean '1'
    option lang 'auto'
    option mediaurlbase '/luci-static/bootstrap'
    option number '4'
    option resourcebase '/luci-static/resources'

package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'none'

package system

config led 'led_usb1'
    option dev '1-1.1'
    option interval '50'
    option name 'USB1'
    option sysfs 'tp-link:green:usb1'
    option trigger 'usbdev'

config custom 'custom'
    option test '1'
""")
        o = OpenWrt(native=native)
        expected = {
            "luci": [
                {
                    "config_name": "core",
                    "config_value": "main",
                    "lang": "auto",
                    "resourcebase": "/luci-static/resources",
                    "mediaurlbase": "/luci-static/bootstrap",
                    "number": "4",
                    "boolean": "1"
                }
            ],
            "firewall": {
                "rules": [
                    {
                        "config_name": "rule",
                        "name": "Allow-MLD",
                        "src": "wan",
                        "proto": "icmp",
                        "src_ip": "fe80::/10",
                        "family": "ipv6",
                        "target": "ACCEPT",
                        "icmp_type": ["130/0", "131/0", "132/0", "143/0"]
                    }
                ]
            },
            "led": [
                {
                    "name": "USB1",
                    "sysfs": "tp-link:green:usb1",
                    "trigger": "usbdev",
                    "dev": "1-1.1",
                    "interval": 50,
                }
            ],
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet"
                }
            ],
            "system": [
                {
                    "test": "1",
                    "config_name": "custom",
                    "config_value": "custom"
                }
            ]
        }
        self.assertDictEqual(o.config, expected)

    def test_skip(self):
        o = OpenWrt({"skipme": {"enabled": True}})
        self.assertEqual(o.render(), '')

    def test_warning(self):
        o = OpenWrt({
            "luci": [
                {
                    "unrecognized": True
                }
            ]
        })
        self.assertEqual(o.render(), '')

    def test_merge(self):
        template = {
            "luci": [
                {
                    "config_name": "core",
                    "config_value": "main",
                    "number": 3,
                    "list": ["eth0"],
                    "some_value": True
                }
            ]
        }
        config = {
            "luci": [
                {
                    "config_name": "core",
                    "config_value": "main",
                    "number": 4,
                    "list": ["wlan0"]
                }
            ]
        }
        expected = {
            "luci": [
                {
                    "config_name": "core",
                    "config_value": "main",
                    "number": 4,
                    "list": ["eth0", "wlan0"],
                    "some_value": True
                }
            ]
        }
        o = OpenWrt(config, templates=[template])
        self.assertEqual(o.config, expected)

    def test_skip_nonlists(self):
        o = OpenWrt({"custom_package": {'unknown': True}})
        self.assertEqual(o.render(), '')

    def test_render_invalid_uci_name(self):
        o = OpenWrt({
            "olsrd2": [
                {
                    "lan": "10.150.25.0/24 domain=0",
                    "config_value": "lan-hna",
                    "config_name": "olsrv2"
                },
                {
                    "lan": "0.0.0.0/24 domain=1",
                    "config_value": "internet-hna",
                    "config_name": "olsrv2"
                }
            ],
        })
        expected = self._tabs("""package olsrd2

config olsrv2 'lan_hna'
    option lan '10.150.25.0/24 domain=0'

config olsrv2 'internet_hna'
    option lan '0.0.0.0/24 domain=1'
""")
        self.assertEqual(o.render(), expected)
