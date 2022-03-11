import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestWireguard(unittest.TestCase, _TabsMixin):
    maxDiff = None

    def test_render_wireguard_interface(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "wg0",
                        "type": "wireguard",
                        "private_key": "sGQitlaWF8LJjmNJOPoQkm9BVAtMtdfwpFT6zLSixlQ=",
                        "port": 51820,
                        "mtu": 1420,
                        "nohostroute": False,
                        "fwmark": "",
                        "addresses": [
                            {
                                "proto": "static",
                                "family": "ipv4",
                                "address": "10.0.0.3",
                                "mask": 24,
                            }
                        ],
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'wg0'
    list addresses '10.0.0.3/24'
    option listen_port '51820'
    option mtu '1420'
    option nohostroute '0'
    option private_key 'sGQitlaWF8LJjmNJOPoQkm9BVAtMtdfwpFT6zLSixlQ='
    option proto 'wireguard'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_wireguard_interface(self):
        native = self._tabs(
            """package network

config interface 'wg0'
    list addresses '10.0.0.3/24'
    option listen_port '51820'
    option mtu '1420'
    option nohostroute '0'
    option private_key 'sGQitlaWF8LJjmNJOPoQkm9BVAtMtdfwpFT6zLSixlQ='
    option proto 'wireguard'
"""
        )
        expected = {
            "interfaces": [
                {
                    "name": "wg0",
                    "type": "wireguard",
                    "private_key": "sGQitlaWF8LJjmNJOPoQkm9BVAtMtdfwpFT6zLSixlQ=",
                    "port": 51820,
                    "mtu": 1420,
                    "nohostroute": False,
                    "addresses": [
                        {
                            "proto": "static",
                            "family": "ipv4",
                            "address": "10.0.0.3",
                            "mask": 24,
                        }
                    ],
                }
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_render_wireguard_interface_with_variables(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "wg0",
                        "type": "wireguard",
                        "private_key": "{{private_key}}",
                        "port": 51820,
                        "mtu": 1420,
                        "nohostroute": False,
                        "fwmark": "",
                        "addresses": [
                            {
                                "proto": "static",
                                "family": "ipv4",
                                "address": "{{ip_address_8097b09be57a4b278e2ef2ea9ea809f3}}",
                                "mask": 32,
                            }
                        ],
                    }
                ]
            },
            context={
                "private_key": "sGQitlaWF8LJjmNJOPoQkm9BVAtMtdfwpFT6zLSixlQ=",
                "ip_address_8097b09be57a4b278e2ef2ea9ea809f3": "10.0.0.3",
            },
        )
        expected = self._tabs(
            """package network

config interface 'wg0'
    list addresses '10.0.0.3/32'
    option listen_port '51820'
    option mtu '1420'
    option nohostroute '0'
    option private_key 'sGQitlaWF8LJjmNJOPoQkm9BVAtMtdfwpFT6zLSixlQ='
    option proto 'wireguard'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_render_wireguard_peer(self):
        o = OpenWrt(
            {
                "wireguard_peers": [
                    {
                        "interface": "wg0",
                        "public_key": "rn+isMBpyQ4HX6ZzE709bKnZw5IaLZoIS3hIjmfKCkk=",
                        "allowed_ips": ["10.0.0.1/32"],
                        "endpoint_host": "192.168.1.42",
                        "endpoint_port": 40840,
                        "preshared_key": "oPZmGdHBseaV1TF0julyElNuJyeKs2Eo+o62R/09IB4=",
                        "persistent_keepalive": 30,
                        "route_allowed_ips": True,
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config wireguard_wg0 'wgpeer_wg0'
    list allowed_ips '10.0.0.1/32'
    option endpoint_host '192.168.1.42'
    option endpoint_port '40840'
    option persistent_keepalive '30'
    option preshared_key 'oPZmGdHBseaV1TF0julyElNuJyeKs2Eo+o62R/09IB4='
    option public_key 'rn+isMBpyQ4HX6ZzE709bKnZw5IaLZoIS3hIjmfKCkk='
    option route_allowed_ips '1'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_render_wireguard_peer_with_variables(self):
        o = OpenWrt(
            {
                "wireguard_peers": [
                    {
                        "interface": "wg0",
                        "public_key": "{{public_key_8097b09be57a4b278e2ef2ea9ea809f3}}",
                        "allowed_ips": [
                            "{{server_ip_network_8097b09be57a4b278e2ef2ea9ea809f3}}"
                        ],
                        "endpoint_host": "{{vpn_host_8097b09be57a4b278e2ef2ea9ea809f3}}",
                        "endpoint_port": 40840,
                        "preshared_key": "{{pre_key_8097b09be57a4b278e2ef2ea9ea809f3}}",
                        "persistent_keepalive": 30,
                        "route_allowed_ips": True,
                    }
                ]
            },
            context={
                "server_ip_network_8097b09be57a4b278e2ef2ea9ea809f3": "10.0.0.1/32",
                "vpn_host_8097b09be57a4b278e2ef2ea9ea809f3": "192.168.1.42",
                "public_key_8097b09be57a4b278e2ef2ea9ea809f3": "rn+isMBpyQ4HX6ZzE709bKnZw5IaLZoIS3hIjmfKCkk=",
                "pre_key_8097b09be57a4b278e2ef2ea9ea809f3": "oPZmGdHBseaV1TF0julyElNuJyeKs2Eo+o62R/09IB4=",
            },
        )
        expected = self._tabs(
            """package network

config wireguard_wg0 'wgpeer_wg0'
    list allowed_ips '10.0.0.1/32'
    option endpoint_host '192.168.1.42'
    option endpoint_port '40840'
    option persistent_keepalive '30'
    option preshared_key 'oPZmGdHBseaV1TF0julyElNuJyeKs2Eo+o62R/09IB4='
    option public_key 'rn+isMBpyQ4HX6ZzE709bKnZw5IaLZoIS3hIjmfKCkk='
    option route_allowed_ips '1'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_render_wireguard_peer_no_endpoint_host(self):
        o = OpenWrt(
            {
                "wireguard_peers": [
                    {
                        "interface": "wg0",
                        "public_key": "rn+isMBpyQ4HX6ZzE709bKnZw5IaLZoIS3hIjmfKCkk=",
                        "allowed_ips": ["10.0.0.1/32"],
                        "endpoint_port": 40840,
                        "preshared_key": "oPZmGdHBseaV1TF0julyElNuJyeKs2Eo+o62R/09IB4=",
                        "persistent_keepalive": 30,
                        "route_allowed_ips": True,
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config wireguard_wg0 'wgpeer_wg0'
    list allowed_ips '10.0.0.1/32'
    option persistent_keepalive '30'
    option preshared_key 'oPZmGdHBseaV1TF0julyElNuJyeKs2Eo+o62R/09IB4='
    option public_key 'rn+isMBpyQ4HX6ZzE709bKnZw5IaLZoIS3hIjmfKCkk='
    option route_allowed_ips '1'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_wireguard_peer(self):
        native = self._tabs(
            """package network

config wireguard_wg0 'wgpeer_wg0'
    list allowed_ips '10.0.0.1/32'
    option endpoint_host '192.168.1.42'
    option endpoint_port '40840'
    option persistent_keepalive '30'
    option preshared_key 'oPZmGdHBseaV1TF0julyElNuJyeKs2Eo+o62R/09IB4='
    option public_key 'rn+isMBpyQ4HX6ZzE709bKnZw5IaLZoIS3hIjmfKCkk='
    option route_allowed_ips '1'
"""
        )
        expected = {
            "wireguard_peers": [
                {
                    "allowed_ips": ["10.0.0.1/32"],
                    "endpoint_host": "192.168.1.42",
                    "endpoint_port": 40840,
                    "interface": "wg0",
                    "persistent_keepalive": 30,
                    "preshared_key": "oPZmGdHBseaV1TF0julyElNuJyeKs2Eo+o62R/09IB4=",
                    "public_key": "rn+isMBpyQ4HX6ZzE709bKnZw5IaLZoIS3hIjmfKCkk=",
                    "route_allowed_ips": True,
                }
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)
