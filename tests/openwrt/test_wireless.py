import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.exceptions import ValidationError
from netjsonconfig.utils import _TabsMixin


class TestWirelessRenderer(unittest.TestCase, _TabsMixin):
    """
    tests for backends.openwrt.renderers.WirelessRenderer
    """
    maxDiff = None

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
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "MyWifiAP",
                        "hidden": True,
                        "ack_distance": 300,
                        "rts_threshold": 1300,
                        "frag_threshold": 1500
                    }
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
    option distance '300'
    option frag '1500'
    option hidden '1'
    option ifname 'wlan0'
    option mode 'ap'
    option network 'wlan0'
    option rts '1300'
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

    def test_multiple_wifi(self):
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
                },
                {
                    "name": "wlan1",
                    "type": "wireless",
                    "addresses": [
                        {
                            "proto": "dhcp",
                            "family": "ipv4"
                        }
                    ],
                    "wireless": {
                        "radio": "radio1",
                        "mode": "adhoc",
                        "ssid": "adhoc-ssid",
                        "bssid": "00:11:22:33:44:55"
                    }
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'wlan0'
    option ifname 'wlan0'
    option proto 'dhcp'

config interface 'wlan1'
    option ifname 'wlan1'
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

config wifi-iface
    option bssid '00:11:22:33:44:55'
    option device 'radio1'
    option ifname 'wlan1'
    option mode 'adhoc'
    option network 'wlan1'
    option ssid 'adhoc-ssid'
""")
        self.assertEqual(o.render(), expected)

    def test_wifi_bridge(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0.1",
                    "type": "ethernet"
                },
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
                        "ssid": "open"
                    }
                },
                {
                    "name": "br-lan",
                    "type": "bridge",
                    "bridge_members": [
                        "eth0.1",
                        "wlan0"
                    ],
                    "addresses": [
                        {
                            "address": "192.168.1.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        }
                    ]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth0_1'
    option ifname 'eth0.1'
    option proto 'none'

config interface 'wlan0'
    option ifname 'wlan0'
    option proto 'dhcp'

config interface 'br_lan'
    option ifname 'eth0.1 wlan0'
    option ipaddr '192.168.1.1/24'
    option proto 'static'
    option type 'bridge'

package wireless

config wifi-iface
    option device 'radio0'
    option ifname 'wlan0'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'open'
""")
        self.assertEqual(o.render(), expected)

    def test_wifi_network(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0.1",
                    "type": "ethernet"
                },
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
                        "ssid": "open",
                        "network": ["wlan0", "eth0.1"]
                    }
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth0_1'
    option ifname 'eth0.1'
    option proto 'none'

config interface 'wlan0'
    option ifname 'wlan0'
    option proto 'dhcp'

package wireless

config wifi-iface
    option device 'radio0'
    option ifname 'wlan0'
    option mode 'ap'
    option network 'wlan0 eth0_1'
    option ssid 'open'
""")
        self.assertEqual(o.render(), expected)

    def test_wireless_empty_network_attr(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "open",
                        "network": []
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
    option ifname 'wlan0'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'open'
""")
        self.assertEqual(o.render(), expected)

    def test_wireless_network_attr_validation(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "open",
                        "network": "lan 0"
                    }
                }
            ]
        })
        # pattern does not validate
        with self.assertRaises(ValidationError):
            o.validate()
        # maxLength does not validate
        o.config['interfaces'][0]['wireless']['network'] = ['lan0123456789012345']
        with self.assertRaises(ValidationError):
            o.validate()
        # ensure fix works
        o.config['interfaces'][0]['wireless']['network'] = ['lan']
        o.validate()

    def test_network_attribute(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "network": "guests",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "open"
                    }
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'guests'
    option ifname 'wlan0'
    option proto 'none'

package wireless

config wifi-iface
    option device 'radio0'
    option ifname 'wlan0'
    option mode 'ap'
    option network 'guests'
    option ssid 'open'
""")
        self.assertEqual(o.render(), expected)

    def test_network_dot_conversion(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "open",
                        "network": ["eth0.1"],
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
    option ifname 'wlan0'
    option mode 'ap'
    option network 'eth0_1'
    option ssid 'open'
""")
        self.assertEqual(o.render(), expected)

    def test_network_dash_conversion(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "open",
                        "network": ["eth0-1"],
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
    option ifname 'wlan0'
    option mode 'ap'
    option network 'eth0_1'
    option ssid 'open'
""")
        self.assertEqual(o.render(), expected)

    def test_inherit_disabled_from_interface(self):
        """
        see issue #35
        https://github.com/openwisp/netjsonconfig/issues/35
        """
        o = OpenWrt({
            "interfaces": [
                {
                    "disabled": True,
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "station",
                        "ssid": "mywifi",
                        "bssid": "00:11:22:33:44:55"
                    }
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'wlan0'
    option enabled '0'
    option ifname 'wlan0'
    option proto 'none'

package wireless

config wifi-iface
    option bssid '00:11:22:33:44:55'
    option device 'radio0'
    option disabled '1'
    option ifname 'wlan0'
    option mode 'sta'
    option network 'wlan0'
    option ssid 'mywifi'
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

    def test_wds_ap(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "wds": True,
                        "ssid": "MyWdsAp"
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
    option ifname 'wlan0'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'MyWdsAp'
    option wds '1'
""")
        self.assertEqual(o.render(), expected)

    def test_wifi_options_zero(self):
        """
        ensure ack_distance, rts_threshold and frag_threshold
        are ignored if left empty
        """
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "MyWifiAP",
                        "wmm": True,
                        "ack_distance": 0,
                        "rts_threshold": 0,
                        "frag_threshold": 0
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
    option ifname 'wlan0'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'MyWifiAP'
    option wmm '1'
""")
        self.assertEqual(o.render(), expected)

    def test_wifi_macfilter(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "MyWifiAP",
                        "macfilter": "deny",
                        "maclist": [
                            "E8:94:F6:33:8C:1D",
                            "42:6c:8f:95:0f:00"
                        ]
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
    option ifname 'wlan0'
    option macfilter 'deny'
    list maclist 'E8:94:F6:33:8C:1D'
    list maclist '42:6c:8f:95:0f:00'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'MyWifiAP'
""")
        self.assertEqual(o.render(), expected)

    def test_wds_bridge(self):
        o = OpenWrt({
            "interfaces": [
                # client
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "mode": "station",
                        "radio": "radio0",
                        "network": ["wds_bridge"],
                        "ssid": "FreeRomaWifi",
                        "bssid": "C0:4A:00:2D:05:FD",
                        "wds": True
                    }
                },
                # repeater access point
                {
                    "name": "wlan1",
                    "type": "wireless",
                    "wireless": {
                        "mode": "access_point",
                        "radio": "radio1",
                        "network": ["wds_bridge"],
                        "ssid": "FreeRomaWifi"
                    }
                },
                # WDS bridge
                {
                    "name": "br-wds",
                    "network": "wds_bridge",
                    "type": "bridge",
                    "addresses": [
                        {
                            "proto": "dhcp",
                            "family": "ipv4"
                        }
                    ],
                    "bridge_members": [
                        "wlan0",
                        "wlan1",
                    ]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'wlan0'
    option ifname 'wlan0'
    option proto 'none'

config interface 'wlan1'
    option ifname 'wlan1'
    option proto 'none'

config interface 'wds_bridge'
    option ifname 'wlan0 wlan1'
    option proto 'dhcp'
    option type 'bridge'

package wireless

config wifi-iface
    option bssid 'C0:4A:00:2D:05:FD'
    option device 'radio0'
    option ifname 'wlan0'
    option mode 'sta'
    option network 'wds_bridge'
    option ssid 'FreeRomaWifi'
    option wds '1'

config wifi-iface
    option device 'radio1'
    option ifname 'wlan1'
    option mode 'ap'
    option network 'wds_bridge'
    option ssid 'FreeRomaWifi'
""")
        self.assertEqual(o.render(), expected)

    def test_mesh_80211s(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "mesh0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "802.11s",
                        "mesh_id": "ninux",
                        "network": ["lan"]
                    }
                },
                {
                    "name": "lan",
                    "type": "bridge",
                    "bridge_members": ["mesh0"],
                    "addresses": [
                        {
                            "address": "192.168.0.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        }
                    ]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'mesh0'
    option ifname 'mesh0'
    option proto 'none'

config interface 'lan'
    option ifname 'mesh0'
    option ipaddr '192.168.0.1/24'
    option proto 'static'
    option type 'bridge'

package wireless

config wifi-iface
    option device 'radio0'
    option ifname 'mesh0'
    option mesh_id 'ninux'
    option mode 'mesh'
    option network 'lan'
""")
        self.assertEqual(o.render(), expected)
