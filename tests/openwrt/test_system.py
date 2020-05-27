import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.backends.openwrt.timezones import timezones_reversed
from netjsonconfig.exceptions import ValidationError
from netjsonconfig.utils import _TabsMixin


class TestSystem(unittest.TestCase, _TabsMixin):
    maxDiff = None
    _system_netjson = {
        "general": {"hostname": "test-system", "timezone": "Europe/Rome"}
    }
    _system_uci = """package system

config system 'system'
    option hostname 'test-system'
    option timezone 'CET-1CEST,M3.5.0,M10.5.0/3'
    option zonename 'Europe/Rome'
"""

    def test_render_system(self):
        o = OpenWrt(self._system_netjson)
        expected = self._tabs(self._system_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_system(self):
        o = OpenWrt(native=self._system_uci)
        self.assertDictEqual(o.config, self._system_netjson)

    _system_simple_netjson = {"general": {"hostname": "test-system"}}
    _system_simple_uci = """package system

config system 'system'
    option hostname 'test-system'
"""

    def test_render_system_without_timezone(self):
        o = OpenWrt(self._system_simple_netjson)
        expected = self._tabs(self._system_simple_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_system_without_timezone(self):
        o = OpenWrt(native=self._system_simple_uci)
        self.assertEqual(o.config, self._system_simple_netjson)

    _system_id_netjson = {
        "general": {"id": "arbitrary", "hostname": "test-system", "timezone": "UTC"}
    }
    _system_id_uci = """package system

config system 'arbitrary'
    option hostname 'test-system'
    option timezone 'UTC'
    option zonename 'UTC'
"""

    def test_parse_system_custom_id(self):
        o = OpenWrt(native=self._system_id_uci)
        self.assertDictEqual(o.config, self._system_id_netjson)

    def test_render_system_custom_id(self):
        o = OpenWrt(self._system_id_netjson)
        expected = self._tabs(self._system_id_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_system_timezone(self):
        native = self._tabs(
            """package system

config system 'system'
    option hostname 'test-system'
    option timezone 'CET-1CEST,M3.5.0,M10.5.0/3'
"""
        )
        o = OpenWrt(native=native)
        expected = {
            "general": {
                "hostname": "test-system",
                "timezone": timezones_reversed["CET-1CEST,M3.5.0,M10.5.0/3"],
            }
        }
        self.assertDictEqual(o.config, expected)

    _ntp_netjson = {
        "ntp": {
            "enabled": True,
            "enable_server": False,
            "server": [
                "0.openwrt.pool.ntp.org",
                "1.openwrt.pool.ntp.org",
                "2.openwrt.pool.ntp.org",
                "3.openwrt.pool.ntp.org",
            ],
        }
    }
    _ntp_uci = """package system

config timeserver 'ntp'
    option enable_server '0'
    option enabled '1'
    list server '0.openwrt.pool.ntp.org'
    list server '1.openwrt.pool.ntp.org'
    list server '2.openwrt.pool.ntp.org'
    list server '3.openwrt.pool.ntp.org'
"""

    def test_render_ntp(self):
        o = OpenWrt(self._ntp_netjson)
        expected = self._tabs(self._ntp_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_ntp(self):
        o = OpenWrt(native=self._ntp_uci)
        self.assertEqual(o.config, self._ntp_netjson)

    _ntp_id_netjson = {
        "ntp": {"id": "arbitrary_id", "enabled": False, "enable_server": False}
    }
    _ntp_id_uci = """package system

config timeserver 'arbitrary_id'
    option enable_server '0'
    option enabled '0'
"""

    def test_render_ntp_id(self):
        o = OpenWrt(self._ntp_id_netjson)
        expected = self._tabs(self._ntp_id_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_ntp_id(self):
        o = OpenWrt(native=self._ntp_id_uci)
        self.assertEqual(o.config, self._ntp_id_netjson)

    _led_netjson = {
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
                "trigger": "phy0tpt",
                "default": False,
                "delayoff": 1,
                "delayon": 5,
            },
            {
                "id": "arbitrary_id",
                "name": "USB2",
                "sysfs": "tp-link:blue:usb2",
                "trigger": "usbdev",
                "dev": "1-1.2",
                "interval": 50,
            },
        ]
    }
    _led_uci = """package system

config led 'led_usb1'
    option dev '1-1.1'
    option interval '50'
    option name 'USB1'
    option sysfs 'tp-link:green:usb1'
    option trigger 'usbdev'

config led 'led_wlan2g'
    option default '0'
    option delayoff '1'
    option delayon '5'
    option name 'WLAN2G'
    option sysfs 'tp-link:blue:wlan2g'
    option trigger 'phy0tpt'

config led 'arbitrary_id'
    option dev '1-1.2'
    option interval '50'
    option name 'USB2'
    option sysfs 'tp-link:blue:usb2'
    option trigger 'usbdev'
"""

    def test_render_led(self):
        o = OpenWrt(self._led_netjson)
        expected = self._tabs(self._led_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_led(self):
        o = OpenWrt(native=(self._led_uci))
        self.assertEqual(o.config, self._led_netjson)

    def test_led_schema_validation(self):
        o = OpenWrt({"led": [{"invalid": True}]})
        with self.assertRaises(ValidationError):
            o.validate()
