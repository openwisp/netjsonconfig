import unittest

from netjsonconfig import OpenWrt

netjson_example = {
    "type": "DeviceConfiguration",
    "general": {
        "hostname": "DeviceNameExample",
        "maintainer": "email@example.org",
        "description": "general info here",
        "ula_prefix": "fd8e:f40a:6701::/48",
    },
    "hardware": {
        "manufacturer": "Example inc.",
        "model": "Example model",
        "version": 1,
        "cpu": "Atheros AR2317",
    },
    "operating_system": {
        "name": "OpenWRT",
        "kernel": "3.10.49",
        "version": "Barrier Breaker",
        "revision": "r43321",
        "description": "OpenWrt Barrier Breaker 14.07",
    },
    "radios": [
        {
            "name": "radio0",
            "protocol": "802.11ac",
            "channel": 1,
            "channel_width": 80,
            "phy": "phy0",
            "country": "US",
            "tx_power": 10,
            "disabled": False,
        }
    ],
    "interfaces": [
        {
            "type": "wireless",
            "name": "wlan0",
            "mac": "de:9f:db:30:c9:c5",
            "mtu": 1500,
            "txqueuelen": 1000,
            "autostart": True,
            "wireless": {
                "radio": "radio0",
                "mode": "access_point",
                "ssid": "ap-ssid-example",
            },
            "addresses": [
                {
                    "address": "192.168.1.1",
                    "mask": 24,
                    "family": "ipv4",
                    "proto": "static",
                },
                {
                    "address": "fe80::216:44ff:fe60:32d2",
                    "mask": 64,
                    "family": "ipv6",
                    "proto": "static",
                },
            ],
        },
        {
            "type": "wireless",
            "name": "adhoc0",
            "mac": "02:CA:FF:EE:BA:BE",
            "mtu": 1500,
            "txqueuelen": 1000,
            "autostart": True,
            "wireless": {
                "radio": "radio0",
                "mode": "adhoc",
                "ssid": "adhoc-ssid-example",
                "bssid": "02:CA:FF:EE:BA:BE",
            },
            "addresses": [
                {"address": "10.0.1.1", "mask": 24, "family": "ipv4", "proto": "static"}
            ],
        },
        {
            "type": "ethernet",
            "name": "eth0",
            "mac": "52:54:00:56:46:d0",
            "mtu": 1500,
            "txqueuelen": 1000,
            "autostart": True,
            "addresses": [
                {
                    "address": "176.9.211.214",
                    "mask": 28,
                    "gateway": "176.9.211.209",
                    "family": "ipv4",
                    "proto": "static",
                },
                {
                    "address": "2a01:4f8:150:8ffc::214",
                    "mask": 64,
                    "family": "ipv6",
                    "proto": "static",
                },
                {
                    "address": "fe80::5054:ff:fe56:46d0",
                    "mask": 64,
                    "family": "ipv6",
                    "proto": "static",
                },
            ],
        },
        {
            "type": "ethernet",
            "name": "eth1",
            "mac": "52:54:00:56:46:c0",
            "mtu": 1500,
            "txqueuelen": 1000,
            "autostart": True,
            "addresses": [
                {"proto": "dhcp", "family": "ipv4"},
                {"proto": "dhcp", "family": "ipv6"},
            ],
        },
        {
            "type": "wireless",
            "name": "wlan1",
            "mac": "de:9f:db:30:c9:c4",
            "mtu": 1500,
            "txqueuelen": 1000,
            "autostart": True,
            "wireless": {
                "radio": "radio0",
                "mode": "access_point",
                "ssid": "private-network-example",
                "encryption": {
                    "protocol": "wpa_personal_mixed",
                    "cipher": "tkip+ccmp",
                    "key": "passphrase012345",
                },
            },
            "addresses": [
                {"proto": "dhcp", "family": "ipv4"},
                {"proto": "dhcp", "family": "ipv6"},
            ],
        },
        {
            "type": "virtual",
            "name": "vpn",
            "mac": "82:29:23:7d:c2:14",
            "mtu": 1500,
            "txqueuelen": 100,
            "autostart": True,
            "addresses": [
                {
                    "address": "fe80::8029:23ff:fe7d:c214",
                    "mask": 64,
                    "family": "ipv6",
                    "proto": "static",
                }
            ],
        },
        {
            "type": "virtual",
            "name": "vpn.40",
            "mac": "82:29:23:7d:c2:14",
            "mtu": 1500,
            "txqueuelen": 100,
            "autostart": True,
        },
        {
            "type": "bridge",
            "name": "brwifi",
            "mac": "82:29:23:7d:c2:14",
            "mtu": 1500,
            "txqueuelen": 0,
            "autostart": True,
            "bridge_members": ["wlan0", "vpn.40"],
            "addresses": [
                {
                    "address": "fe80::8029:23ff:fe7d:c214",
                    "mask": 64,
                    "family": "ipv6",
                    "proto": "static",
                }
            ],
        },
    ],
    "routes": [
        {"device": "eth0", "destination": "10.0.3.1", "next": "10.0.2.1", "cost": 1}
    ],
    "dns_servers": ["10.254.0.1", "10.254.0.2"],
    "dns_search": ["domain.com"],
}


class TestNetJson(unittest.TestCase):
    """
    ensures OpenWrt backend is compatible with
    NetJSON DeviceConfiguration example
    """

    def test_netjson_example(self):
        o = OpenWrt(netjson_example)
        o.validate()
