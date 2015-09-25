import unittest

from netjsonconfig import OpenWrt


class TestSystemRendererer(unittest.TestCase):
    """
    tests for backends.openwrt.renderers.SystemRendererer
    """
    def _tabs(self, string):
        """
        replace 4 spaces with 1 tab
        """
        return string.replace('    ', '\t')

    def test_system(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "general": {
                "hostname": "test_system",
                "timezone": "Europe/Rome",
                "custom_setting": True,
                "empty_setting1": None,
                "empty_setting2": ""
            }
        })
        expected = self._tabs("""package system

config system
    option custom_setting '1'
    option hostname 'test_system'
    option timezone 'CET-1CEST,M3.5.0,M10.5.0/3'
""")
        self.assertEqual(o.render(), expected)

    def test_ntp(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "ntp": {
                "enabled": True,
                "enable_server": False,
                "server": [
                    "0.openwrt.pool.ntp.org",
                    "1.openwrt.pool.ntp.org",
                    "2.openwrt.pool.ntp.org",
                    "3.openwrt.pool.ntp.org"
                ]
            }
        })
        expected = self._tabs("""package system

config timeserver 'ntp'
    list server '0.openwrt.pool.ntp.org'
    list server '1.openwrt.pool.ntp.org'
    list server '2.openwrt.pool.ntp.org'
    list server '3.openwrt.pool.ntp.org'
    option enable_server '0'
    option enabled '1'
""")
        self.assertEqual(o.render(), expected)
