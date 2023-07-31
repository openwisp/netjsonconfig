import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestZeroTier(unittest.TestCase, _TabsMixin):
    maxDiff = None
    _TEST_CONFIG = {
        "zerotier": [
            {
                "id": ["9536600adf654321", "9536600adf654322"],
                "name": "ow_zt",
            },
        ]
    }

    def test_render_zerotier(self):
        o = OpenWrt(self._TEST_CONFIG)
        expected = self._tabs(
            """package zerotier

config zerotier 'ow_zt'
    option enabled '1'
    list join '9536600adf654321'
    list join '9536600adf654322'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_zerotier(self):
        native = self._tabs(
            """package zerotier

config zerotier 'ow_zt'
    option enabled '0'
    list join '9536600adf654321'
    list join '9536600adf654322'
"""
        )
        expected = {
            "zerotier": [
                {
                    "id": ["9536600adf654321", "9536600adf654322"],
                    "name": "ow_zt",
                    "disabled": True,
                },
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)
