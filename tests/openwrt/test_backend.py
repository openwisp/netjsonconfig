import json
import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.exceptions import ValidationError


class TestBackend(unittest.TestCase):
    """
    tests for backends.openwrt.OpenWrt
    """
    def test_json(self):
        config = {
            "type": "DeviceConfiguration",
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

    def test_validate(self):
        o = OpenWrt({})
        with self.assertRaises(ValidationError):
            o.validate()

        o = OpenWrt({'type': 'WRONG'})
        with self.assertRaises(ValidationError):
            o.validate()

        o = OpenWrt({'type': 'DeviceConfiguration'})
        o.validate()
        o.config['type'] = 'CHANGED'
        with self.assertRaises(ValidationError):
            o.validate()

    def test_type_error(self):
        with self.assertRaises(TypeError):
            o = OpenWrt([])

    def test_system_invalid_timezone(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "general": {
                "hostname": "test_system",
                "timezone": "WRONG",
            }
        })
        with self.assertRaises(ValidationError):
            o.validate()

    def test_schema_radio_wrong_driver(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
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
            "type": "DeviceConfiguration",
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
