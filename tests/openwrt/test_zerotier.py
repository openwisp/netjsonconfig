import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestZeroTier(unittest.TestCase, _TabsMixin):
    maxDiff = None
    _TEST_CONFIG = {
        "zerotier": [
            {
                "id": "9536600adf654321",
                "name": "zerotier-openwisp-network-1",
            },
            {
                "id": "9536600adf654322",
                "name": "zerotier-openwisp-network-2",
            },
        ]
    }

    def test_render_zerotier(self):
        o = OpenWrt(self._TEST_CONFIG)
        expected = self._tabs(
            """package zerotier

config zerotier 'zerotier_openwisp_network_1'
    option enabled '1'
    list join '9536600adf654321'

config zerotier 'zerotier_openwisp_network_2'
    option enabled '1'
    list join '9536600adf654322'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_zerotier(self):
        native = self._tabs(
            """package zerotier

config zerotier 'zerotier_openwisp_network_1'
    option enabled '1'
    list join '9536600adf654321'

config zerotier 'zerotier_openwisp_network_2'
    option enabled '1'
    list join '9536600adf654322'
"""
        )
        expected = {
            "zerotier": [
                {
                    "id": "9536600adf654321",
                    "name": "zerotier-openwisp-network-1",
                    "disabled": False,
                },
                {
                    "id": "9536600adf654322",
                    "name": "zerotier-openwisp-network-2",
                    "disabled": False,
                },
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)
