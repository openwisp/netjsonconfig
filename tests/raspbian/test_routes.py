import unittest

from netjsonconfig import Raspbian
from netjsonconfig.utils import _TabsMixin


class TestStaticRoute(unittest.TestCase, _TabsMixin):

    def test_ipv4_manual_route(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet"
                }
            ],
            "routes": [
                {
                    "device": "eth0",
                    "destination": "192.168.4.1/24",
                    "next": "192.168.2.2",
                    "cost": 2,
                },
            ]
        })

        expected = '''# config: /etc/network/interfaces

auto eth0
iface eth0 inet manual
post-up route add -net 192.168.4.1 netmask 255.255.255.0 gw 192.168.2.2
pre-up route del -net 192.168.4.1 netmask 255.255.255.0 gw 192.168.2.2

'''
        self.assertEqual(o.render(), expected)

    def test_ipv4_static_route(self):
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
            ],
            "routes": [
                {
                    "device": "eth0",
                    "destination": "192.168.4.1/24",
                    "next": "192.168.2.2",
                    "cost": 2,
                },
            ]
        })

        expected = '''# config: /etc/network/interfaces

auto eth0
iface eth0 inet static
address 10.0.0.1
netmask 255.255.255.240
post-up route add -net 192.168.4.1 netmask 255.255.255.0 gw 192.168.2.2
pre-up route del -net 192.168.4.1 netmask 255.255.255.0 gw 192.168.2.2

'''
        self.assertEqual(o.render(), expected)

    def test_ipv6_manual_route(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet"
                }
            ],
            "routes": [
                {
                    "device": "eth0",
                    "destination": "fd89::1/128",
                    "next": "fd88::1",
                    "cost": 0,
                }
            ]
        })

        expected = '''# config: /etc/network/interfaces

auto eth0
iface eth0 inet manual
up ip -6 route add fd89::1/128 via fd88::1 dev eth0
down ip -6 route del fd89::1/128 via fd88::1 dev eth0

'''

        self.assertEqual(o.render(), expected)

    def test_ipv6_static_route(self):
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
            ],
            "routes": [
                {
                    "device": "eth0",
                    "destination": "fd89::1/128",
                    "next": "fd88::1",
                    "cost": 0,
                }
            ]
        })

        expected = '''# config: /etc/network/interfaces

auto eth0
iface eth0 inet6 static
address fe80::ba27:ebff:fe1c:5477
netmask 64
up ip -6 route add fd89::1/128 via fd88::1 dev eth0
down ip -6 route del fd89::1/128 via fd88::1 dev eth0

'''
        self.assertEqual(o.render(), expected)
