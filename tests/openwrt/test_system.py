import unittest
from netjsonconfig import OpenWrt
from netjsonconfig.exceptions import ValidationError

from .utils import _TabsMixin


class TestSystemRenderer(unittest.TestCase, _TabsMixin):
    """
    tests for backends.openwrt.renderers.SystemRenderer
    """
    def test_system(self):
        o = OpenWrt({
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

    def test_led_1(self):
        o = OpenWrt({
            "led": [
                {
                    "name": "USB1",
                    "sysfs": "tp-link:green:usb1",
                    "trigger": "usbdev",
                    "dev": "1-1.1",
                    "interval": 50,
                },
                {
                    "name": "WLAN2G",
                    "sysfs": "tp-link:blue:wlan2g",
                    "trigger": "phy0tpt"
                }
            ]
        })
        expected = self._tabs("""package system

config led 'led_usb1'
    option dev '1-1.1'
    option interval '50'
    option name 'USB1'
    option sysfs 'tp-link:green:usb1'
    option trigger 'usbdev'

config led 'led_wlan2g'
    option name 'WLAN2G'
    option sysfs 'tp-link:blue:wlan2g'
    option trigger 'phy0tpt'
""")
        self.assertEqual(o.render(), expected)

    def test_led_schema_validation(self):
        o = OpenWrt({
            "led": [
                {
                    "invalid": True
                }
            ]
        })
        with self.assertRaises(ValidationError):
            o.validate()
