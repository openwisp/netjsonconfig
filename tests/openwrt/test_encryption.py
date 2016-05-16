import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestEncryption(unittest.TestCase, _TabsMixin):
    """
    tests for backends.openwrt.renderers.WirelessRenderer (wireless ifaces)
    """
    maxDiff = None

    def test_wpa2_personal(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "wpa2-personal",
                        "encryption": {
                            "protocol": "wpa2_personal",
                            "cipher": "tkip+ccmp",
                            "key": "passphrase012345"
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

config wifi-iface 'wifi_wlan0'
    option device 'radio0'
    option encryption 'psk2+tkip+ccmp'
    option ifname 'wlan0'
    option key 'passphrase012345'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'wpa2-personal'
""")
        self.assertEqual(o.render(), expected)

    def test_wpa_personal_mixed(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "wpa2-personal",
                        "encryption": {
                            "protocol": "wpa_personal_mixed",
                            "cipher": "ccmp",
                            "key": "passphrase012345"
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

config wifi-iface 'wifi_wlan0'
    option device 'radio0'
    option encryption 'psk-mixed+ccmp'
    option ifname 'wlan0'
    option key 'passphrase012345'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'wpa2-personal'
""")
        self.assertEqual(o.render(), expected)

    def test_wpa_personal(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "wpa-personal",
                        "encryption": {
                            "protocol": "wpa_personal",
                            "cipher": "auto",
                            "key": "passphrase012345"
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

config wifi-iface 'wifi_wlan0'
    option device 'radio0'
    option encryption 'psk'
    option ifname 'wlan0'
    option key 'passphrase012345'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'wpa-personal'
""")
        self.assertEqual(o.render(), expected)

    def test_wpa2_enterprise_ap(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "wpa2-802.1x",
                        "encryption": {
                            "protocol": "wpa2_enterprise",
                            "cipher": "tkip",
                            "key": "radius_secret",
                            "server": "192.168.0.1",
                            "port": 1812,
                            "acct_server": "192.168.0.2",
                            "acct_port": 1813,
                            "nasid": 2,
                            "wpa_group_rekey": 350
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

config wifi-iface 'wifi_wlan0'
    option acct_port '1813'
    option acct_server '192.168.0.2'
    option device 'radio0'
    option encryption 'wpa2+tkip'
    option ifname 'wlan0'
    option key 'radius_secret'
    option mode 'ap'
    option nasid '2'
    option network 'wlan0'
    option port '1812'
    option server '192.168.0.1'
    option ssid 'wpa2-802.1x'
    option wpa_group_rekey '350'
""")
        self.assertEqual(o.render(), expected)

    def test_wpa_enterprise_mixed_ap(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "enterprise-mixed",
                        "encryption": {
                            "protocol": "wpa_enterprise_mixed",
                            "cipher": "auto",
                            "key": "radius_secret",
                            "server": "192.168.0.1"
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

config wifi-iface 'wifi_wlan0'
    option device 'radio0'
    option encryption 'wpa-mixed'
    option ifname 'wlan0'
    option key 'radius_secret'
    option mode 'ap'
    option network 'wlan0'
    option server '192.168.0.1'
    option ssid 'enterprise-mixed'
""")
        self.assertEqual(o.render(), expected)

    def test_wpa_enterprise_ap(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "enterprise",
                        "encryption": {
                            "protocol": "wpa_enterprise",
                            "cipher": "ccmp",
                            "key": "radius_secret",
                            "server": "192.168.0.1"
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

config wifi-iface 'wifi_wlan0'
    option device 'radio0'
    option encryption 'wpa+ccmp'
    option ifname 'wlan0'
    option key 'radius_secret'
    option mode 'ap'
    option network 'wlan0'
    option server '192.168.0.1'
    option ssid 'enterprise'
""")
        self.assertEqual(o.render(), expected)

    def test_wpa2_enterprise_client(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "station",
                        "ssid": "enterprise-client",
                        "bssid": "00:26:b9:20:5f:09",
                        "encryption": {
                            "protocol": "wpa2_enterprise",
                            "cipher": "auto",
                            "eap_type": "tls",
                            "identity": "test-identity",
                            "password": "test-password",
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

config wifi-iface 'wifi_wlan0'
    option bssid '00:26:b9:20:5f:09'
    option device 'radio0'
    option eap_type 'tls'
    option encryption 'wpa2'
    option identity 'test-identity'
    option ifname 'wlan0'
    option mode 'sta'
    option network 'wlan0'
    option password 'test-password'
    option ssid 'enterprise-client'
""")
        self.assertEqual(o.render(), expected)

    def test_wep_open(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
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
    option proto 'none'

package wireless

config wifi-iface 'wifi_wlan0'
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

    def test_wep_shared(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
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
    option proto 'none'

package wireless

config wifi-iface 'wifi_wlan0'
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

    def test_encryption_disabled(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "MyNetwork",
                        "encryption": {
                            "disabled": True,
                            "protocol": "wpa2_personal",
                            "cipher": "tkip+ccmp",
                            "key": "passphrase012345"
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

config wifi-iface 'wifi_wlan0'
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
                        "encryption": {"protocol": "none"}
                    }
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'wlan0'
    option ifname 'wlan0'
    option proto 'none'

package wireless

config wifi-iface 'wifi_wlan0'
    option device 'radio0'
    option ifname 'wlan0'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'open'
""")
        self.assertEqual(o.render(), expected)

    def test_wpa2_personal_80211s(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "mesh0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "802.11s",
                        "mesh_id": "encrypted-mesh",
                        "encryption": {
                            "protocol": "wpa2_personal",
                            "cipher": "tkip+ccmp",
                            "key": "passphrase012345"
                        }
                    }
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'mesh0'
    option ifname 'mesh0'
    option proto 'none'

package wireless

config wifi-iface 'wifi_mesh0'
    option device 'radio0'
    option encryption 'psk2+tkip+ccmp'
    option ifname 'mesh0'
    option key 'passphrase012345'
    option mesh_id 'encrypted-mesh'
    option mode 'mesh'
    option network 'mesh0'
""")
        self.assertEqual(o.render(), expected)

    def test_wpa2_personal_adhoc(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "adhoc",
                        "ssid": "encrypted-adhoc",
                        "bssid": "00:26:b9:20:5f:09",
                        "encryption": {
                            "protocol": "wpa2_personal",
                            "cipher": "auto",
                            "key": "passphrase012345"
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

config wifi-iface 'wifi_wlan0'
    option bssid '00:26:b9:20:5f:09'
    option device 'radio0'
    option encryption 'psk2'
    option ifname 'wlan0'
    option key 'passphrase012345'
    option mode 'adhoc'
    option network 'wlan0'
    option ssid 'encrypted-adhoc'
""")
        self.assertEqual(o.render(), expected)

    def test_wps_ap(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "wps-ssid",
                        "encryption": {
                            "protocol": "wps",
                            "wps_label": False,
                            "wps_pushbutton": True,
                            "wps_pin": ""
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

config wifi-iface 'wifi_wlan0'
    option device 'radio0'
    option encryption 'psk'
    option ifname 'wlan0'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'wps-ssid'
    option wps_label '0'
    option wps_pushbutton '1'
""")
        self.assertEqual(o.render(), expected)
