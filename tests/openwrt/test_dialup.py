import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestDialup(unittest.TestCase, _TabsMixin):
    maxDiff = None

    _dialup_interface_netjson = {
        "interfaces": [
            {
                "mtu": 1448,
                "network": "xdsl",
                "type": "dialup",
                "name": "dsl0",
                "password": "jf93nf82o023$",
                "username": "dsluser",
                "proto": "pppoe",
            },
        ]
    }

    _dialup_interface_uci = """package network

config interface 'xdsl'
    option ifname 'dsl0'
    option mtu '1448'
    option password 'jf93nf82o023$'
    option proto 'pppoe'
    option username 'dsluser'
"""

    def test_render_dialup_interface(self):
        result = OpenWrt(self._dialup_interface_netjson).render()
        expected = self._tabs(self._dialup_interface_uci)
        self.assertEqual(result, expected)

    def test_parse_dialup_interface(self):
        result = OpenWrt(native=self._dialup_interface_uci).config
        expected = self._dialup_interface_netjson
        self.assertDictEqual(result, expected)
