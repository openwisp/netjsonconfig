import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestModemManager(unittest.TestCase, _TabsMixin):
    maxDiff = None

    _modemmanager_interface_netjson = {
        "interfaces": [
            {
                "name": "wwan0",
                "type": "modem-manager",
                "apn": "apn.vodafone.com",
                "pin": "1234",
                "device": "/sys/devices/platform/ahb/1b000000.usb/usb1/1-1",
                "username": "user123",
                "password": "pwd123456",
                "metric": 50,
                "iptype": "ipv4v6",
                "lowpower": False,
                "mtu": 1500,
            }
        ]
    }

    _modemmanager_interface_uci = """package network

config interface 'wwan0'
    option apn 'apn.vodafone.com'
    option device '/sys/devices/platform/ahb/1b000000.usb/usb1/1-1'
    option ifname 'wwan0'
    option iptype 'ipv4v6'
    option lowpower '0'
    option metric '50'
    option mtu '1500'
    option password 'pwd123456'
    option pincode '1234'
    option proto 'modemmanager'
    option username 'user123'
"""

    def test_render_modemmanager_interface(self):
        result = OpenWrt(self._modemmanager_interface_netjson).render()
        expected = self._tabs(self._modemmanager_interface_uci)
        self.assertEqual(result, expected)

    def test_parse_modemmanager_interface(self):
        result = OpenWrt(native=self._modemmanager_interface_uci).config
        expected = self._modemmanager_interface_netjson
        self.assertDictEqual(result, expected)
