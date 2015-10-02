import os
import json
import unittest
import tarfile

from netjsonconfig import OpenWrt
from netjsonconfig.exceptions import ValidationError

from .utils import _TabsMixin


class TestBackend(unittest.TestCase, _TabsMixin):
    """
    tests for backends.openwrt.OpenWrt
    """
    def test_json_method(self):
        config = {
            "interfaces": [
                {
                    "name": "lo",
                    "type": "loopback",
                    "addresses": [
                        {
                            "address": "127.0.0.1",
                            "mask": 8,
                            "proto": "static",
                            "family": "ipv4"
                        }
                    ]
                }
            ]
        }
        o = OpenWrt(config)
        self.assertEqual(json.loads(o.json()), config)

    def test_string_argument(self):
        o = OpenWrt('{}')

    def test_validate(self):
        o = OpenWrt({'type': 'WRONG'})
        with self.assertRaises(ValidationError):
            o.validate()

        o = OpenWrt({'type': 'DeviceConfiguration'})
        o.validate()
        o.config['type'] = 'CHANGED'
        with self.assertRaises(ValidationError):
            o.validate()

    def test_find_bridge_skip_error(self):
        o = OpenWrt({'interfaces': ['WRONG']})
        with self.assertRaises(ValidationError):
            o.validate()

    def test_type_error(self):
        with self.assertRaises(TypeError):
            o = OpenWrt([])
        with self.assertRaises(TypeError):
            o = OpenWrt('NOTJSON[]\{\}')

    def test_system_invalid_timezone(self):
        o = OpenWrt({
            "general": {
                "hostname": "test_system",
                "timezone": "WRONG",
            }
        })
        with self.assertRaises(ValidationError):
            o.validate()

    def test_schema_radio_wrong_driver(self):
        o = OpenWrt({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "iamwrong",
                    "protocol": "802.11ac",
                    "channel": 132,
                    "channel_width": 80,
                    "tx_power": 8
                }
            ]
        })
        with self.assertRaises(ValidationError):
            o.validate()

    def test_schema_radio_wrong_protocol(self):
        o = OpenWrt({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11ad",  # ad is not supported by OpenWRT yet
                    "channel": 132,
                    "channel_width": 80,
                    "tx_power": 8
                }
            ]
        })
        with self.assertRaises(ValidationError):
            o.validate()

    def test_generate(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "addresses": [
                        {
                            "address": "192.168.1.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        }
                    ],
                    "wireless": [
                        {
                            "radio": "radio0",
                            "mode": "access_point",
                            "ssid": "MyWifiAP",
                            "hidden": True
                        }
                    ]
                }
            ],
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                }
            ]
        })
        o.generate()
        tar = tarfile.open('openwrt-config.tar.gz', 'r:gz')
        self.assertEqual(len(tar.getmembers()), 2)
        # network
        network = tar.getmember('/etc/config/network')
        contents = tar.extractfile(network).read().decode()
        expected = self._tabs("""config interface 'wlan0'
    option ifname 'wlan0'
    option ipaddr '192.168.1.1/24'
    option proto 'static'

""")
        # wireless
        wireless = tar.getmember('/etc/config/wireless')
        contents = tar.extractfile(wireless).read().decode()
        expected = self._tabs("""config wifi-device 'radio0'
    option channel '3'
    option htmode 'HT20'
    option hwmode '11g'
    option phy 'phy0'
    option txpower '3'
    option type 'mac80211'

config wifi-iface
    option device 'radio0'
    option hidden '1'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'MyWifiAP'
""")
        self.assertEqual(contents, expected)
        # close and delete tar.gz file
        tar.close()
        os.remove('openwrt-config.tar.gz')
