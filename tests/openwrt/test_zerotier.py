import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestZeroTier(unittest.TestCase, _TabsMixin):
    maxDiff = None
    # This configuration is used when we want to join multiple networks
    # and the ZT service is running on a single default port 9993
    _TEST_SAME_NAME_MULTIPLE_CONFIG = {
        "zerotier": [
            {
                "name": "ow_zt",
                "nwid_ifname": [
                    {"id": "9536600adf654321", "ifname": "owzt654321"},
                    {"id": "9536600adf654322", "ifname": "owzt654322"},
                ],
            },
        ]
    }
    # This ZT configuration is used when ZT services
    # are configured to run on multiple ports, e.g., 9993 and 9994.
    # For more information, refer to:
    # https://docs.zerotier.com/zerotier/zerotier.conf/#local-configuration-options
    _TEST_DIFF_NAME_MULTIPLE_CONFIG = {
        "zerotier": [
            {
                "name": "ow_zt1",
                "nwid_ifname": [{"id": "9536600adf654321", "ifname": "owzt654321"}],
            },
            {
                "name": "ow_zt2",
                "nwid_ifname": [{"id": "9536600adf654322", "ifname": "owzt654322"}],
            },
        ]
    }

    def test_zt_multiple_render_diff_name(self):
        o = OpenWrt(self._TEST_DIFF_NAME_MULTIPLE_CONFIG)
        expected = self._tabs(
            """package zerotier

config zerotier 'ow_zt1'
    option config_path '/etc/ow_zerotier_extra'
    option copy_config_path '1'
    option enabled '1'
    list join '9536600adf654321'

config zerotier 'ow_zt2'
    option config_path '/etc/ow_zerotier_extra'
    option copy_config_path '1'
    option enabled '1'
    list join '9536600adf654322'

# ---------- files ---------- #

# path: /etc/ow_zerotier_extra/devicemap
# mode: 0644

# network_id=interface_name
9536600adf654322=owzt654322

# network_id=interface_name
9536600adf654321=owzt654321

"""
        )
        self.assertEqual(o.render(), expected)

    def test_zt_mutiple_parse_diff_name(self):
        native = self._tabs(
            """package zerotier

config zerotier 'ow_zt1'
    option enabled '1'
    list join '9536600adf654321'

config zerotier 'ow_zt2'
    option enabled '1'
    list join '9536600adf654322'
"""
        )
        expected = {
            "zerotier": [
                {
                    "name": "ow_zt1",
                    "disabled": False,
                    "nwid_ifname": [{"id": "9536600adf654321", "ifname": "owzt654321"}],
                },
                {
                    "name": "ow_zt2",
                    "disabled": False,
                    "nwid_ifname": [{"id": "9536600adf654322", "ifname": "owzt654322"}],
                },
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_zt_multiple_render_same_name(self):
        o = OpenWrt(self._TEST_SAME_NAME_MULTIPLE_CONFIG)
        expected = self._tabs(
            """package zerotier

config zerotier 'ow_zt'
    option config_path '/etc/ow_zerotier_extra'
    option copy_config_path '1'
    option enabled '1'
    list join '9536600adf654321'
    list join '9536600adf654322'

# ---------- files ---------- #

# path: /etc/ow_zerotier_extra/devicemap
# mode: 0644

# network_id=interface_name
9536600adf654321=owzt654321
9536600adf654322=owzt654322

"""
        )
        self.assertEqual(o.render(), expected)

    def test_zt_mutiple_parse_same_name(self):
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
                    "nwid_ifname": [
                        {"id": "9536600adf654321", "ifname": "owzt654321"},
                        {"id": "9536600adf654322", "ifname": "owzt654322"},
                    ],
                    "name": "ow_zt",
                    "disabled": True,
                },
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)
