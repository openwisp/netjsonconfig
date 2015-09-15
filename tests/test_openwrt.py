import os
import unittest

from netjsonconfig import OpenWrt


class TestOpenWrt(unittest.TestCase):
    """ OpenWrt tests """

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
    list ipaddr '127.0.0.1/8'
"""
        self.assertEqual(o.gen(), expected)

    def test_multiple_ip(self):
        o = OpenWrt({
            "type": "DeviceConfiguration",
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "address": "192.168.1.1",
                            "mask": 24,
                            "family": "ipv4"
                        },
                        {
                            "address": "192.168.2.1",
                            "mask": 24,
                            "family": "ipv4"
                        },
                        {
                            "address": "fd87::1",
                            "mask": 128,
                            "family": "ipv6"
                        }
                    ]
                }
            ]
        })
        expected = """package network

config interface 'eth0'
    option ifname 'eth0'
    list ipaddr '192.168.1.1/24'
    list ipaddr '192.168.2.1/24'
    list ip6addr 'fd87::1/128'
"""
        self.assertEqual(o.gen(), expected)
