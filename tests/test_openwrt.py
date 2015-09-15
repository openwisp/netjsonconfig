import os
import unittest

from netjsonconfig import OpenWrt


class TestOpenWrt(unittest.TestCase):
    """ OpenWrt tests """

    def test_gen_loopback(self):
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
