import unittest
from netjsonconfig import OpenWrt

from .utils import _TabsMixin


class TestWirelessRenderer(unittest.TestCase, _TabsMixin):
    """
    tests for backends.openwrt.renderers.WirelessRenderer
    """
    def test_radio(self):
        o = OpenWrt({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 140,
                    "channel_width": 20,
                    "tx_power": 9,
                    "country": "en"
                },
                {
                    "name": "radio1",
                    "phy": "phy1",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 149,
                    "channel_width": 40,
                    "tx_power": 18,
                    "country": "en",
                    "disabled": True
                }
            ]
        })
        expected = self._tabs("""package wireless

config wifi-device 'radio0'
    option channel '140'
    option country 'EN'
    option htmode 'HT20'
    option hwmode '11a'
    option phy 'phy0'
    option txpower '9'
    option type 'mac80211'

config wifi-device 'radio1'
    option channel '149'
    option country 'EN'
    option disabled '1'
    option htmode 'HT40'
    option hwmode '11a'
    option phy 'phy1'
    option txpower '18'
    option type 'mac80211'
""")
        self.assertEqual(o.render(), expected)

    def test_radio_2ghz_mac80211(self):
        o = OpenWrt({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                },
                {
                    "name": "radio1",
                    "phy": "phy1",
                    "driver": "mac80211",
                    "protocol": "802.11g",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                }
            ]
        })
        expected = self._tabs("""package wireless

config wifi-device 'radio0'
    option channel '3'
    option htmode 'HT20'
    option hwmode '11g'
    option phy 'phy0'
    option txpower '3'
    option type 'mac80211'

config wifi-device 'radio1'
    option channel '3'
    option htmode 'NONE'
    option hwmode '11g'
    option phy 'phy1'
    option txpower '3'
    option type 'mac80211'
""")
        self.assertEqual(o.render(), expected)

    def test_radio_2ghz_athk(self):
        o = OpenWrt({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "ath5k",
                    "protocol": "802.11b",
                    "channel": 3,
                    "channel_width": 5,
                    "tx_power": 3
                },
                {
                    "name": "radio1",
                    "phy": "phy1",
                    "driver": "ath9k",
                    "protocol": "802.11a",
                    "channel": 140,
                    "channel_width": 10,
                    "tx_power": 4
                }
            ]
        })
        expected = self._tabs("""package wireless

config wifi-device 'radio0'
    option chanbw '5'
    option channel '3'
    option hwmode '11b'
    option phy 'phy0'
    option txpower '3'
    option type 'ath5k'

config wifi-device 'radio1'
    option chanbw '10'
    option channel '140'
    option hwmode '11a'
    option phy 'phy1'
    option txpower '4'
    option type 'ath9k'
""")
        self.assertEqual(o.render(), expected)

    def test_radio_ac_and_custom_attrs(self):
        o = OpenWrt({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11ac",
                    "channel": 132,
                    "channel_width": 80,
                    "tx_power": 8,
                    "diversity": True,
                    "country_ie": True,
                    "empty_setting": ""
                }
            ]
        })
        expected = self._tabs("""package wireless

config wifi-device 'radio0'
    option channel '132'
    option country_ie '1'
    option diversity '1'
    option htmode 'VHT80'
    option hwmode '11a'
    option phy 'phy0'
    option txpower '8'
    option type 'mac80211'
""")
        self.assertEqual(o.render(), expected)

    def test_wifi_interfaces(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "addresses": [
                        {
                            "address": "192.168.1.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        }
                    ],
                    "wireless": [
                        {
                            "radio": "radio0",
                            "mode": "access_point",
                            "ssid": "MyWifiAP",
                            "hidden": True
                        }
                    ]
                }
            ],
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'wlan0'
    option ifname 'wlan0'
    option ipaddr '192.168.1.1/24'
    option proto 'static'

package wireless

config wifi-device 'radio0'
    option channel '3'
    option htmode 'HT20'
    option hwmode '11g'
    option phy 'phy0'
    option txpower '3'
    option type 'mac80211'

config wifi-iface
    option device 'radio0'
    option hidden '1'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'MyWifiAP'
""")
        self.assertEqual(o.render(), expected)

    def test_wifi_encryption_wep_open(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "addresses": [
                        {
                            "proto": "dhcp"
                        }
                    ],
                    "wireless": [
                        {
                            "radio": "radio0",
                            "mode": "access_point",
                            "ssid": "wep",
                            "encryption": {
                                "enabled": True,
                                "protocol": "wep_open",
                                "key": "wepkey1234567"
                            }
                        }
                    ]
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
                            "proto": "dhcp"
                        }
                    ],
                    "wireless": [
                        {
                            "radio": "radio0",
                            "mode": "access_point",
                            "ssid": "wep",
                            "encryption": {
                                "enabled": True,
                                "protocol": "wep_shared",
                                "key": "wepkey1234567"
                            }
                        }
                    ]
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
                            "proto": "dhcp"
                        }
                    ],
                    "wireless": [
                        {
                            "radio": "radio0",
                            "mode": "access_point",
                            "ssid": "wpa-personal",
                            "encryption": {
                                "enabled": True,
                                "protocol": "wpa_personal",
                                "ciphers": [
                                    "tkip"
                                ],
                                "key": "passphrase012345"
                            }
                        }
                    ]
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
                            "proto": "dhcp"
                        }
                    ],
                    "wireless": [
                        {
                            "radio": "radio0",
                            "mode": "access_point",
                            "ssid": "wpa2-personal",
                            "encryption": {
                                "enabled": True,
                                "protocol": "wpa2_personal",
                                "ciphers": [
                                    "tkip",
                                    "ccmp"
                                ],
                                "key": "passphrase012345"
                            }
                        }
                    ]
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
                            "proto": "dhcp"
                        }
                    ],
                    "wireless": [
                        {
                            "radio": "radio0",
                            "mode": "access_point",
                            "ssid": "MyNetwork",
                            "encryption": {
                                "enabled": False,
                                "protocol": "wpa2_personal",
                                "ciphers": [
                                    "tkip",
                                    "ccmp"
                                ],
                                "key": "passphrase012345"
                            }
                        }
                    ]
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
    option mode 'ap'
    option network 'wlan0'
    option ssid 'MyNetwork'
""")
        self.assertEqual(o.render(), expected)

    def test_multiple_ssid(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "addresses": [
                        {
                            "proto": "dhcp"
                        }
                    ],
                    "wireless": [
                        {
                            "radio": "radio0",
                            "mode": "access_point",
                            "ssid": "wpa2-personal",
                            "encryption": {
                                "enabled": True,
                                "protocol": "wpa2_personal",
                                "ciphers": [
                                    "tkip",
                                    "ccmp"
                                ],
                                "key": "passphrase012345"
                            }
                        },
                        {
                            "radio": "radio1",
                            "mode": "adhoc",
                            "ssid": "adhoc-ssid"
                        }
                    ]
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
    option key 'passphrase012345'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'wpa2-personal'

config wifi-iface
    option device 'radio1'
    option mode 'adhoc'
    option network 'wlan0'
    option ssid 'adhoc-ssid'
""")
        self.assertEqual(o.render(), expected)

    def test_wifi_bridge(self):
        o = OpenWrt({
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
                        }
                    ]
                },
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "addresses": [
                        {
                            "proto": "dhcp"
                        }
                    ],
                    "wireless": [
                        {
                            "radio": "radio0",
                            "mode": "access_point",
                            "ssid": "open"
                        }
                    ]
                },
                {
                    "name": "br-eth0",
                    "type": "bridge",
                    "bridge_members": [
                        "eth0.1",
                        "wlan0"
                    ]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth0_1'
    option ifname 'eth0.1'
    option ipaddr '192.168.1.1/24'
    option proto 'static'
    option type 'bridge'

config interface 'wlan0'
    option ifname 'wlan0'
    option proto 'dhcp'

package wireless

config wifi-iface
    option device 'radio0'
    option mode 'ap'
    option network 'wlan0 eth0_1'
    option ssid 'open'
""")
        self.assertEqual(o.render(), expected)
