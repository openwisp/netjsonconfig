import unittest

from netjsonconfig import Raspbian
from netjsonconfig.exceptions import ValidationError
from netjsonconfig.utils import _TabsMixin


class TestInterfacesRenderer(unittest.TestCase, _TabsMixin):

    def test_interface_ipv4_static(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "family": "ipv4",
                            "proto": "static",
                            "address": "10.0.0.1",
                            "mask": 28
                        }
                    ]
                }
            ]
        })

        expected = '''/etc/network/interfaces
-----------------------
auto eth0
iface eth0 inet static
    address 10.0.0.1
    netmask 255.255.255.240



/etc/resolv.conf
----------------
'''
        self.assertEqual(o.render(), expected)

    def test_interface_ipv6_static(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "family": "ipv6",
                            "proto": "static",
                            "address": "fe80::ba27:ebff:fe1c:5477",
                            "mask": 64
                        }
                    ]
                }
            ]
        })

        expected = '''/etc/network/interfaces
-----------------------
auto eth0
iface eth0 inet6 static
    address fe80::ba27:ebff:fe1c:5477
    netmask 64



/etc/resolv.conf
----------------
'''
        self.assertEqual(o.render(), expected)

    def test_interface_multiple_static(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "family": "ipv4",
                            "proto": "static",
                            "address": "10.0.0.1",
                            "mask": 28
                        },
                        {
                            "family": "ipv6",
                            "proto": "static",
                            "address": "fe80::ba27:ebff:fe1c:5477",
                            "mask": 64
                        }
                    ]
                }
            ]
        })

        expected = '''/etc/network/interfaces
-----------------------
auto eth0
iface eth0 inet static
    address 10.0.0.1
    netmask 255.255.255.240
iface eth0 inet6 static
    address fe80::ba27:ebff:fe1c:5477
    netmask 64



/etc/resolv.conf
----------------
'''


    def test_interface_ipv4_dhcp(self):
        o = Raspbian({
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

        expected = '''/etc/network/interfaces
-----------------------
auto eth0
allow-hotplug eth0
iface eth0 inet dhcp



/etc/resolv.conf
----------------
'''
        self.assertEqual(o.render(), expected)

    def test_interface_ipv6_dhcp(self):
        o = Raspbian({
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "addresses": [
                            {
                                "proto": "dhcp",
                                "family": "ipv6"
                            }
                        ]
                    }
                ]
        })

        expected = '''/etc/network/interfaces
-----------------------
auto eth0
allow-hotplug eth0
iface eth0 inet6 dhcp



/etc/resolv.conf
----------------
'''
        self.assertEqual(o.render(), expected)

    def test_interface_multiple_dhcp(self):
        o = Raspbian({
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

        expected = '''/etc/network/interfaces
-----------------------
auto eth0
allow-hotplug eth0
iface eth0 inet6 dhcp



/etc/resolv.conf
----------------
'''
        self.assertEqual(o.render(), expected)

    def test_loopback(self):
        o = Raspbian({
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

        expected = '''/etc/network/interfaces
-----------------------
auto lo
iface lo inet static
    address 127.0.0.1
    netmask 255.0.0.0



/etc/resolv.conf
----------------
'''
        self.assertEqual(o.render(), expected)
