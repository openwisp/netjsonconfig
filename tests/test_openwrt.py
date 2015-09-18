import json
import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.exceptions import ValidationError


class TestOpenWrt(unittest.TestCase):
    """ OpenWrt tests """

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
        self.assertEqual(json.loads(o.json(indent=4)), config)

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

    def test_loopback(self):
        o = OpenWrt({
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
        })
        expected = """package network

config interface 'lo'
    option ifname 'lo'
    option ipaddr '127.0.0.1/8'
    option proto 'static'
"""
        self.assertEqual(o.render(), expected)

    def test_multiple_ip(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "interfaces": [
                {
                    "name": "eth0.1",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "address": "192.168.1.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        },
                        {
                            "address": "192.168.2.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        },
                        {
                            "address": "fd87::1",
                            "mask": 128,
                            "proto": "static",
                            "family": "ipv6"
                        }
                    ]
                }
            ]
        })
        expected = """package network

config interface 'eth0_1'
    option ifname 'eth0.1'
    option ipaddr '192.168.1.1/24'
    option proto 'static'

config interface 'eth0_1_2'
    option ifname 'eth0.1'
    option ipaddr '192.168.2.1/24'
    option proto 'static'

config interface 'eth0_1_3'
    option ifname 'eth0.1'
    option ip6addr 'fd87::1/128'
    option proto 'static'
"""
        self.assertEqual(o.render(), expected)

    def test_dhcp(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "proto": "dhcp",
                            "family": "ipv4"
                        }
                    ]
                }
            ]
        })
        expected = """package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'dhcp'
"""
        self.assertEqual(o.render(), expected)

    def test_multiple_dhcp(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "proto": "dhcp",
                            "family": "ipv4"
                        },
                        {
                            "proto": "dhcp",
                            "family": "ipv6"
                        }
                    ]
                }
            ]
        })
        expected = """package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'dhcp'

config interface 'eth0_2'
    option ifname 'eth0'
    option proto 'dhcpv6'
"""
        self.assertEqual(o.render(), expected)

    def test_ipv4_routes(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "interfaces": [
                {
                    "name": "eth1",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "address": "192.168.1.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        }
                    ]
                }
            ],
            "routes": [
                {
                    "device": "eth1",
                    "destination": "192.168.3.1/24",
                    "next": "192.168.2.1"
                },
                {
                    "device": "eth1",
                    "destination": "192.168.4.1/24",
                    "next": "192.168.2.2",
                    "cost": 2,
                    "source": "192.168.1.10",
                    "table": 2,
                    "onlink": 1,
                    "mtu": 1450
                }
            ]
        })
        expected = """package network

config interface 'eth1'
    option ifname 'eth1'
    option ipaddr '192.168.1.1/24'
    option proto 'static'

config route 'route1'
    option gateway '192.168.2.1'
    option interface 'eth1'
    option netmask '255.255.255.0'
    option target '192.168.3.1'

config route 'route2'
    option gateway '192.168.2.2'
    option interface 'eth1'
    option metric '2'
    option mtu '1450'
    option netmask '255.255.255.0'
    option onlink '1'
    option source '192.168.1.10'
    option table '2'
    option target '192.168.4.1'
"""
        self.assertEqual(o.render(), expected)

    def test_ipv6_routes(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "interfaces": [
                {
                    "name": "eth1",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "address": "fd87::1",
                            "mask": 128,
                            "proto": "static",
                            "family": "ipv6"
                        }
                    ]
                }
            ],
            "routes": [
                {
                    "device": "eth1",
                    "destination": "fd89::1/128",
                    "next": "fd88::1"
                },
                {
                    "device": "eth1",
                    "destination": "fd90::1/128",
                    "next": "fd88::2",
                    "cost": 3,
                    "source": "fd87::10"
                }
            ]
        })
        expected = """package network

config interface 'eth1'
    option ifname 'eth1'
    option ip6addr 'fd87::1/128'
    option proto 'static'

config route6
    option gateway 'fd88::1'
    option interface 'eth1'
    option target 'fd89::1/128'

config route6
    option gateway 'fd88::2'
    option interface 'eth1'
    option metric '3'
    option source 'fd87::10'
    option target 'fd90::1/128'
"""
        self.assertEqual(o.render(), expected)

    def test_additional_proto(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "interfaces": [
                {
                    "name": "mobile0",
                    "addresses": [
                        {
                            "proto": "3g"
                        }
                    ]
                }
            ]
        })
        expected = """package network

config interface 'mobile0'
    option ifname 'mobile0'
    option proto '3g'
"""
        self.assertEqual(o.render(), expected)

    def test_interface_custom_attrs(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "interfaces": [
                {
                    "name": "mobile0",
                    "mtu": 1400,
                    "enabled": "0",
                    "custom_attr": "yes",
                    "empty": "",
                    "addresses": [
                        {
                            "proto": "3g"
                        }
                    ]
                }
            ]
        })
        expected = """package network

config interface 'mobile0'
    option custom_attr 'yes'
    option enabled '0'
    option ifname 'mobile0'
    option mtu '1400'
    option proto '3g'
"""
        self.assertEqual(o.render(), expected)

    def test_system(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "general": {
                "hostname": "test_system",
                "timezone": "Europe/Rome",
                "custom_setting": "1",
                "empty_setting1": None,
                "empty_setting2": "",
                "empty_setting3": [],
            }
        })
        expected = """package system

config system
    option custom_setting '1'
    option hostname 'test_system'
    option timezone 'CET-1CEST,M3.5.0,M10.5.0/3'
"""
        self.assertEqual(o.render(), expected)

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

    def test_radio(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 140,
                    "channel_width": 20,
                    "tx_power": 9,
                    "country": "en"
                },
                {
                    "name": "radio1",
                    "phy": "phy1",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 149,
                    "channel_width": 40,
                    "tx_power": 18,
                    "country": "en",
                    "disabled": True
                }
            ]
        })
        expected = """package wireless

config wifi-device 'radio0'
    option channel '140'
    option country 'EN'
    option htmode 'HT20'
    option hwmode '11a'
    option phy 'phy0'
    option txpower '9'
    option type 'mac80211'

config wifi-device 'radio1'
    option channel '149'
    option country 'EN'
    option disabled '1'
    option htmode 'HT40'
    option hwmode '11a'
    option phy 'phy1'
    option txpower '18'
    option type 'mac80211'
"""
        self.assertEqual(o.render(), expected)

    def test_radio_2ghz_mac80211(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                },
                {
                    "name": "radio1",
                    "phy": "phy1",
                    "driver": "mac80211",
                    "protocol": "802.11g",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                }
            ]
        })
        expected = """package wireless

config wifi-device 'radio0'
    option channel '3'
    option htmode 'HT20'
    option hwmode '11g'
    option phy 'phy0'
    option txpower '3'
    option type 'mac80211'

config wifi-device 'radio1'
    option channel '3'
    option htmode 'NONE'
    option hwmode '11g'
    option phy 'phy1'
    option txpower '3'
    option type 'mac80211'
"""
        print(o.render())
        print(expected)
        self.assertEqual(o.render(), expected)

    def test_radio_2ghz_mac80211(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                },
                {
                    "name": "radio1",
                    "phy": "phy1",
                    "driver": "mac80211",
                    "protocol": "802.11g",
                    "channel": 2,
                    "channel_width": 20,
                    "tx_power": 4
                }
            ]
        })
        expected = """package wireless

config wifi-device 'radio0'
    option channel '3'
    option htmode 'HT20'
    option hwmode '11g'
    option phy 'phy0'
    option txpower '3'
    option type 'mac80211'

config wifi-device 'radio1'
    option channel '2'
    option htmode 'NONE'
    option hwmode '11g'
    option phy 'phy1'
    option txpower '4'
    option type 'mac80211'
"""
        self.assertEqual(o.render(), expected)

    def test_radio_2ghz_athk(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "ath5k",
                    "protocol": "802.11b",
                    "channel": 3,
                    "channel_width": 5,
                    "tx_power": 3
                },
                {
                    "name": "radio1",
                    "phy": "phy1",
                    "driver": "ath9k",
                    "protocol": "802.11a",
                    "channel": 140,
                    "channel_width": 10,
                    "tx_power": 4
                }
            ]
        })
        expected = """package wireless

config wifi-device 'radio0'
    option chanbw '5'
    option channel '3'
    option hwmode '11b'
    option phy 'phy0'
    option txpower '3'
    option type 'ath5k'

config wifi-device 'radio1'
    option chanbw '10'
    option channel '140'
    option hwmode '11a'
    option phy 'phy1'
    option txpower '4'
    option type 'ath9k'
"""
        self.assertEqual(o.render(), expected)

    def test_radio_ac_and_custom_attrs(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11ac",
                    "channel": 132,
                    "channel_width": 80,
                    "tx_power": 8,
                    "diversity": "1",
                    "country_ie": "1",
                    "empty_setting": ""
                }
            ]
        })
        expected = """package wireless

config wifi-device 'radio0'
    option channel '132'
    option country_ie '1'
    option diversity '1'
    option htmode 'VHT80'
    option hwmode '11a'
    option phy 'phy0'
    option txpower '8'
    option type 'mac80211'
"""
        self.assertEqual(o.render(), expected)

    def test_radio_wrong_driver(self):
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

    def test_radio_wrong_protocol(self):
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
