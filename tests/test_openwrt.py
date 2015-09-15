import json
import unittest

from netjsonconfig import OpenWrt


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
        print(o.render())
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
        print(o.render())
        print(expected)
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
