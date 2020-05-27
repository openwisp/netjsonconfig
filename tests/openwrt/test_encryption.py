import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestEncryption(unittest.TestCase, _TabsMixin):
    maxDiff = None

    _wpa2_personal_netjson = {
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
                        "key": "passphrase012345",
                    },
                },
            }
        ]
    }
    _wpa2_personal_uci = """package network

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
"""

    def test_render_wpa2_personal(self):
        o = OpenWrt(self._wpa2_personal_netjson)
        expected = self._tabs(self._wpa2_personal_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_wpa2_personal(self):
        o = OpenWrt(native=self._wpa2_personal_uci)
        self.assertEqual(o.config, self._wpa2_personal_netjson)

    _wpa_personal_mixed_netjson = {
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
                        "key": "passphrase012345",
                    },
                },
            }
        ]
    }
    _wpa_personal_mixed_uci = """package network

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
"""

    def test_render_wpa_personal_mixed(self):
        o = OpenWrt(self._wpa_personal_mixed_netjson)
        expected = self._tabs(self._wpa_personal_mixed_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_wpa_personal_mixed(self):
        o = OpenWrt(native=self._wpa_personal_mixed_uci)
        self.assertEqual(o.config, self._wpa_personal_mixed_netjson)

    _wpa_personal_netjson = {
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
                        "key": "passphrase012345",
                    },
                },
            }
        ]
    }
    _wpa_personal_uci = """package network

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
"""

    def test_render_wpa_personal(self):
        o = OpenWrt(self._wpa_personal_netjson)
        expected = self._tabs(self._wpa_personal_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_wpa_personal(self):
        o = OpenWrt(native=self._wpa_personal_uci)
        self.assertEqual(o.config, self._wpa_personal_netjson)

    _wpa2_enterprise_ap_netjson = {
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
                        "nasid": "2",
                        "wpa_group_rekey": "350",
                    },
                },
            }
        ]
    }
    _wpa2_enterprise_ap_uci = """package network

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
"""

    def test_render_wpa2_enterprise(self):
        o = OpenWrt(self._wpa2_enterprise_ap_netjson)
        expected = self._tabs(self._wpa2_enterprise_ap_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_wpa2_enterprise(self):
        o = OpenWrt(native=self._wpa2_enterprise_ap_uci)
        self.assertEqual(o.config, self._wpa2_enterprise_ap_netjson)

    _wpa_enterprise_mixed_ap_netjson = {
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
                        "server": "192.168.0.1",
                    },
                },
            }
        ]
    }
    _wpa_enterprise_mixed_ap_uci = """package network

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
"""

    def test_render_wpa_enterprise_mixed_ap(self):
        o = OpenWrt(self._wpa_enterprise_mixed_ap_netjson)
        expected = self._tabs(self._wpa_enterprise_mixed_ap_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_wpa_enterprise_mixed_ap(self):
        o = OpenWrt(native=self._wpa_enterprise_mixed_ap_uci)
        self.assertEqual(o.config, self._wpa_enterprise_mixed_ap_netjson)

    _wpa_enterprise_ap_netjson = {
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
                        "server": "192.168.0.1",
                    },
                },
            }
        ]
    }
    _wpa_enterprise_ap_uci = """package network

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
"""

    def test_render_wpa_enterprise_ap(self):
        o = OpenWrt(self._wpa_enterprise_ap_netjson)
        expected = self._tabs(self._wpa_enterprise_ap_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_wpa_enterprise_ap(self):
        o = OpenWrt(native=self._wpa_enterprise_ap_uci)
        self.assertEqual(o.config, self._wpa_enterprise_ap_netjson)

    _wpa2_enterprise_client_netjson = {
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
                    },
                },
            }
        ]
    }
    _wpa2_enterprise_client_uci = """package network

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
"""

    def test_render_wpa2_enterprise_client(self):
        o = OpenWrt(self._wpa2_enterprise_client_netjson)
        expected = self._tabs(self._wpa2_enterprise_client_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_wpa2_enterprise_client(self):
        o = OpenWrt(native=self._wpa2_enterprise_client_uci)
        self.assertEqual(o.config, self._wpa2_enterprise_client_netjson)

    _wep_open_netjson = {
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
                        "key": "wepkey1234567",
                        "cipher": "auto",
                    },
                },
            }
        ]
    }
    _wep_open_uci = """package network

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
"""

    def test_render_wep_open(self):
        o = OpenWrt(self._wep_open_netjson)
        expected = self._tabs(self._wep_open_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_wep_open(self):
        o = OpenWrt(native=self._wep_open_uci)
        self.assertEqual(o.config, self._wep_open_netjson)

    _wep_shared_netjson = {
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
                        "key": "wepkey1234567",
                        "cipher": "auto",
                    },
                },
            }
        ]
    }
    _wep_shared_uci = """package network

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
"""

    def test_render_wep_shared(self):
        o = OpenWrt(self._wep_shared_netjson)
        expected = self._tabs(self._wep_shared_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_wep_shared(self):
        o = OpenWrt(native=self._wep_shared_uci)
        self.assertEqual(o.config, self._wep_shared_netjson)

    def test_encryption_disabled(self):
        o = OpenWrt(
            {
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
                                "key": "passphrase012345",
                            },
                        },
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'wlan0'
    option ifname 'wlan0'
    option proto 'none'

package wireless

config wifi-iface 'wifi_wlan0'
    option device 'radio0'
    option encryption 'none'
    option ifname 'wlan0'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'MyNetwork'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_no_encryption(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "wlan0",
                        "type": "wireless",
                        "wireless": {
                            "radio": "radio0",
                            "mode": "access_point",
                            "ssid": "open",
                            "encryption": {"protocol": "none"},
                        },
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'wlan0'
    option ifname 'wlan0'
    option proto 'none'

package wireless

config wifi-iface 'wifi_wlan0'
    option device 'radio0'
    option encryption 'none'
    option ifname 'wlan0'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'open'
"""
        )
        self.assertEqual(o.render(), expected)

    _wpa2_80211s_netjson = {
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
                        "key": "passphrase012345",
                    },
                },
            }
        ]
    }
    _wpa2_80211s_uci = """package network

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
"""

    def test_render_wpa2_80211s(self):
        o = OpenWrt(self._wpa2_80211s_netjson)
        expected = self._tabs(self._wpa2_80211s_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_wpa2_80211s(self):
        o = OpenWrt(native=self._wpa2_80211s_uci)
        self.assertEqual(o.config, self._wpa2_80211s_netjson)

    _wpa2_adhoc_netjson = {
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
                        "key": "passphrase012345",
                    },
                },
            }
        ]
    }
    _wpa2_adhoc_uci = """package network

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
"""

    def test_render_wpa2_adhoc(self):
        o = OpenWrt(self._wpa2_adhoc_netjson)
        expected = self._tabs(self._wpa2_adhoc_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_wpa2_adhoc(self):
        o = OpenWrt(native=self._wpa2_adhoc_uci)
        self.assertEqual(o.config, self._wpa2_adhoc_netjson)

    _wps_ap_netjson = {
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
                        "wps_pin": "pin1234",
                    },
                },
            }
        ]
    }
    _wps_ap_uci = """package network

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
    option wps_pin 'pin1234'
    option wps_pushbutton '1'
"""

    def test_render_wps_ap(self):
        o = OpenWrt(self._wps_ap_netjson)
        expected = self._tabs(self._wps_ap_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_wps_ap(self):
        o = OpenWrt(native=self._wps_ap_uci)
        self.assertEqual(o.config, self._wps_ap_netjson)
