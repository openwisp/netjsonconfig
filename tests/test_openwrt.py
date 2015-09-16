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
    option proto 'static'
    option ipaddr '127.0.0.1/8'
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
    option proto 'static'
    option ipaddr '192.168.1.1/24'

config interface 'eth0_1_2'
    option ifname 'eth0.1'
    option proto 'static'
    option ipaddr '192.168.2.1/24'

config interface 'eth0_1_3'
    option ifname 'eth0.1'
    option proto 'static'
    option ip6addr 'fd87::1/128'
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
                    "source": "192.168.1.10"
                }
            ]
        })
        expected = """package network

config interface 'eth1'
    option ifname 'eth1'
    option proto 'static'
    option ipaddr '192.168.1.1/24'

config route 'route1'
    option interface 'eth1'
    option target '192.168.3.1'
    option netmask '255.255.255.0'
    option gateway '192.168.2.1'

config route 'route2'
    option interface 'eth1'
    option target '192.168.4.1'
    option netmask '255.255.255.0'
    option gateway '192.168.2.2'
    option metric '2'
    option source '192.168.1.10'
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
    option proto 'static'
    option ip6addr 'fd87::1/128'

config route6
    option interface 'eth1'
    option target 'fd89::1/128'
    option gateway 'fd88::1'

config route6
    option interface 'eth1'
    option target 'fd90::1/128'
    option gateway 'fd88::2'
    option metric '3'
    option source 'fd87::10'
"""
        self.assertEqual(o.render(), expected)

    def test_system(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "general": {
                "hostname": "test_system",
                "timezone": "CET-1CEST,M3.5.0,M10.5.0/3"
            }
        })
        expected = """package system

config system
    option hostname 'test_system'
    option timezone 'CET-1CEST,M3.5.0,M10.5.0/3'
"""
        self.assertEqual(o.render(), expected)
