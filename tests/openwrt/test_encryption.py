import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestWirelessRenderer(unittest.TestCase, _TabsMixin):
    """
    tests for backends.openwrt.renderers.WirelessRenderer (wireless ifaces)
    """
    maxDiff = None

    def test_wifi_encryption_wep_open(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "addresses": [
                        {
                            "proto": "dhcp",
                            "family": "ipv4"
                        }
                    ],
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "wep",
                        "encryption": {
                            "protocol": "wep_open",
                            "key": "wepkey1234567"
                        }
                    }
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'wlan0'
    option ifname 'wlan0'
    option proto 'dhcp'

package wireless

config wifi-iface
    option device 'radio0'
    option encryption 'wep-open'
    option ifname 'wlan0'
    option key '1'
    option key1 's:wepkey1234567'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'wep'
""")
        self.assertEqual(o.render(), expected)

    def test_wifi_encryption_wep_shared(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "addresses": [
                        {
                            "proto": "dhcp",
                            "family": "ipv4"
                        }
                    ],
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "wep",
                        "encryption": {
                            "protocol": "wep_shared",
                            "key": "wepkey1234567"
                        }
                    }
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'wlan0'
    option ifname 'wlan0'
    option proto 'dhcp'

package wireless

config wifi-iface
    option device 'radio0'
    option encryption 'wep-shared'
    option ifname 'wlan0'
    option key '1'
    option key1 'wepkey1234567'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'wep'
""")
        self.assertEqual(o.render(), expected)

    def test_wifi_encryption_wpa_personal(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "addresses": [
                        {
                            "proto": "dhcp",
                            "family": "ipv4"
                        }
                    ],
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "wpa-personal",
                        "encryption": {
                            "protocol": "wpa_personal",
                            "ciphers": [
                                "tkip"
                            ],
                            "key": "passphrase012345"
                        }
                    }
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'wlan0'
    option ifname 'wlan0'
    option proto 'dhcp'

package wireless

config wifi-iface
    option device 'radio0'
    option encryption 'psk+tkip'
    option ifname 'wlan0'
    option key 'passphrase012345'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'wpa-personal'
""")
        self.assertEqual(o.render(), expected)

    def test_wifi_encryption_wpa2_personal(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "addresses": [
                        {
                            "proto": "dhcp",
                            "family": "ipv4"
                        }
                    ],
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "wpa2-personal",
                        "encryption": {
                            "protocol": "wpa2_personal",
                            "ciphers": [
                                "tkip",
                                "ccmp"
                            ],
                            "key": "passphrase012345"
                        }
                    }
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'wlan0'
    option ifname 'wlan0'
    option proto 'dhcp'

package wireless

config wifi-iface
    option device 'radio0'
    option encryption 'psk2+tkip+ccmp'
    option ifname 'wlan0'
    option key 'passphrase012345'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'wpa2-personal'
""")
        self.assertEqual(o.render(), expected)

    def test_encryption_disabled(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "addresses": [
                        {
                            "proto": "dhcp",
                            "family": "ipv4"
                        }
                    ],
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "MyNetwork",
                        "encryption": {
                            "disabled": True,
                            "protocol": "wpa2_personal",
                            "ciphers": [
                                "tkip",
                                "ccmp"
                            ],
                            "key": "passphrase012345"
                        }
                    }
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'wlan0'
    option ifname 'wlan0'
    option proto 'dhcp'

package wireless

config wifi-iface
    option device 'radio0'
    option ifname 'wlan0'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'MyNetwork'
""")
        self.assertEqual(o.render(), expected)

    def test_no_encryption(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "open",
                        "encryption": {
                            "protocol": "none",
                            "disabled": False,
                            "key": ""
                        }
                    }
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'wlan0'
    option ifname 'wlan0'
    option proto 'none'

package wireless

config wifi-iface
    option device 'radio0'
    option encryption 'none'
    option ifname 'wlan0'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'open'
""")
        self.assertEqual(o.render(), expected)
