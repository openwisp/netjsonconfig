import unittest
from netjsonconfig import OpenWrt

from .utils import _TabsMixin


class TestDefaultRendererer(unittest.TestCase, _TabsMixin):
    """
    tests for backends.openwrt.renderers.DefaultRendererer
    """
    maxDiff = None

    def test_default(self):
        o = OpenWrt({
            "luci": [
                {
                    "config_name": "core",
                    "config_value": "main",
                    "lang": "auto",
                    "resourcebase": "/luci-static/resources",
                    "mediaurlbase": "/luci-static/bootstrap"
                }
            ],
            "firewall": [
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
                }
            ]
        })
        expected = self._tabs("""package firewall

config rule
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
    option lang 'auto'
    option mediaurlbase '/luci-static/bootstrap'
    option resourcebase '/luci-static/resources'
""")
        self.assertEqual(o.render(), expected)

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
        self.assertEqual(o.render(), 'package luci\n\n')
