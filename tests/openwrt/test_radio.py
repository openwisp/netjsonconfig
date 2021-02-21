import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestRadio(unittest.TestCase, _TabsMixin):
    maxDiff = None

    def test_render_radio(self):
        o = OpenWrt(
            {
                "radios": [
                    {
                        "name": "radio0",
                        "phy": "phy0",
                        "driver": "mac80211",
                        "protocol": "802.11n",
                        "channel": 140,
                        "channel_width": 20,
                        "country": "00",
                    },
                    {
                        "name": "radio1",
                        "phy": "phy1",
                        "driver": "mac80211",
                        "protocol": "802.11n",
                        "channel": 136,
                        "channel_width": 40,
                        "tx_power": 18,
                        "country": "00",
                        "disabled": True,
                    },
                ]
            }
        )
        expected = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel '140'
    option country '00'
    option htmode 'HT20'
    option hwmode '11a'
    option phy 'phy0'
    option type 'mac80211'

config wifi-device 'radio1'
    option channel '136'
    option country '00'
    option disabled '1'
    option htmode 'HT40'
    option hwmode '11a'
    option phy 'phy1'
    option txpower '18'
    option type 'mac80211'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_radio(self):
        native = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel '140'
    option country '00'
    option htmode 'HT20'
    option hwmode '11a'
    option phy 'phy0'
    option type 'mac80211'

config wifi-device 'radio1'
    option channel '136'
    option country '00'
    option disabled '1'
    option htmode 'HT40'
    option hwmode '11a'
    option phy 'phy1'
    option txpower '18'
    option type 'mac80211'
"""
        )
        expected = {
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 140,
                    "channel_width": 20,
                    "country": "00",
                },
                {
                    "name": "radio1",
                    "phy": "phy1",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 136,
                    "channel_width": 40,
                    "tx_power": 18,
                    "country": "00",
                    "disabled": True,
                },
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_render_radio_2ghz_mac80211(self):
        o = OpenWrt(
            {
                "radios": [
                    {
                        "name": "radio0",
                        "phy": "phy0",
                        "driver": "mac80211",
                        "protocol": "802.11n",
                        "channel": 3,
                        "channel_width": 20,
                        "tx_power": 3,
                    },
                    {
                        "name": "radio1",
                        "phy": "phy1",
                        "driver": "mac80211",
                        "protocol": "802.11g",
                        "channel": 3,
                        "channel_width": 20,
                        "tx_power": 3,
                    },
                ]
            }
        )
        expected = self._tabs(
            """package wireless

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
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_radio_2ghz_mac80211(self):
        native = self._tabs(
            """package wireless

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
"""
        )
        expected = {
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3,
                },
                {
                    "name": "radio1",
                    "phy": "phy1",
                    "driver": "mac80211",
                    "protocol": "802.11g",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3,
                },
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_render_radio_ac(self):
        o = OpenWrt(
            {
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
                        "empty_setting": "",
                    }
                ]
            }
        )
        expected = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel '132'
    option country_ie '1'
    option diversity '1'
    option htmode 'VHT80'
    option hwmode '11a'
    option phy 'phy0'
    option txpower '8'
    option type 'mac80211'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_radio_ac(self):
        native = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel '132'
    option country_ie '1'
    option diversity '1'
    option htmode 'VHT80'
    option hwmode '11a'
    option phy 'phy0'
    option txpower '8'
    option type 'mac80211'
"""
        )
        expected = {
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11ac",
                    "channel": 132,
                    "channel_width": 80,
                    "tx_power": 8,
                    "diversity": "1",
                    "country_ie": "1",
                }
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_80211n(self):
        o = OpenWrt(
            {
                "radios": [
                    {
                        "name": "radio0",
                        "phy": "phy0",
                        "driver": "mac80211",
                        "protocol": "802.11n",
                        "channel": 3,
                        "channel_width": 20,
                        "tx_power": 3,
                    }
                ]
            }
        )
        expected = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel '3'
    option htmode 'HT20'
    option hwmode '11g'
    option phy 'phy0'
    option txpower '3'
    option type 'mac80211'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_render_radio_mac80211b(self):
        o = OpenWrt(
            {
                "radios": [
                    {
                        "name": "radio0",
                        "phy": "phy0",
                        "driver": "mac80211",
                        "protocol": "802.11b",
                        "channel": 3,
                        "channel_width": 20,
                        "tx_power": 3,
                    }
                ]
            }
        )
        expected = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel '3'
    option htmode 'NONE'
    option hwmode '11b'
    option phy 'phy0'
    option txpower '3'
    option type 'mac80211'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_radio_mac80211b(self):
        native = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel '3'
    option htmode 'NONE'
    option hwmode '11b'
    option phy 'phy0'
    option txpower '3'
    option type 'mac80211'
"""
        )
        expected = {
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11b",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3,
                }
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_render_auto_80211n_2ghz_channel(self):
        o = OpenWrt(
            {
                "radios": [
                    {
                        "name": "radio0",
                        "phy": "phy0",
                        "driver": "mac80211",
                        "protocol": "802.11n",
                        "channel": 0,
                        "channel_width": 20,
                        "hwmode": "11g",
                    }
                ]
            }
        )
        expected = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel 'auto'
    option htmode 'HT20'
    option hwmode '11g'
    option phy 'phy0'
    option type 'mac80211'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_auto_80211n_2ghz_channel(self):
        native = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel 'auto'
    option htmode 'HT20'
    option hwmode '11g'
    option phy 'phy0'
    option type 'mac80211'
"""
        )
        expected = {
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 0,
                    "channel_width": 20,
                    "hwmode": "11g",
                }
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_render_auto_80211n_5ghz_channel(self):
        o = OpenWrt(
            {
                "radios": [
                    {
                        "name": "radio0",
                        "phy": "phy0",
                        "driver": "mac80211",
                        "protocol": "802.11n",
                        "channel": 0,
                        "channel_width": 20,
                        "hwmode": "11a",
                    }
                ]
            }
        )
        expected = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel 'auto'
    option htmode 'HT20'
    option hwmode '11a'
    option phy 'phy0'
    option type 'mac80211'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_auto_80211n_5ghz_channel(self):
        native = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel 'auto'
    option htmode 'HT20'
    option hwmode '11a'
    option phy 'phy0'
    option type 'mac80211'
"""
        )
        expected = {
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 0,
                    "channel_width": 20,
                    "hwmode": "11a",
                }
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_auto_80211ac_2ghz_channel(self):
        o = OpenWrt(
            {
                "radios": [
                    {
                        "name": "radio0",
                        "phy": "phy0",
                        "driver": "mac80211",
                        "protocol": "802.11ac",
                        "channel": 0,
                        "channel_width": 80,
                        "hwmode": "11g",
                    }
                ]
            }
        )
        expected = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel 'auto'
    option htmode 'VHT80'
    option hwmode '11g'
    option phy 'phy0'
    option type 'mac80211'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_auto_80211ac_5ghz_channel(self):
        o = OpenWrt(
            {
                "radios": [
                    {
                        "name": "radio0",
                        "phy": "phy0",
                        "driver": "mac80211",
                        "protocol": "802.11ac",
                        "channel": 0,
                        "channel_width": 160,
                        "hwmode": "11a",
                    }
                ]
            }
        )
        expected = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel 'auto'
    option htmode 'VHT160'
    option hwmode '11a'
    option phy 'phy0'
    option type 'mac80211'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_auto_80211g_channel(self):
        o = OpenWrt(
            {
                "radios": [
                    {
                        "name": "radio0",
                        "phy": "phy0",
                        "driver": "mac80211",
                        "protocol": "802.11g",
                        "channel": 0,
                        "channel_width": 20,
                    }
                ]
            }
        )
        expected = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel 'auto'
    option htmode 'NONE'
    option hwmode '11g'
    option phy 'phy0'
    option type 'mac80211'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_auto_80211a_channel(self):
        o = OpenWrt(
            {
                "radios": [
                    {
                        "name": "radio0",
                        "phy": "phy0",
                        "driver": "mac80211",
                        "protocol": "802.11a",
                        "channel": 0,
                        "channel_width": 20,
                    }
                ]
            }
        )
        expected = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel 'auto'
    option htmode 'NONE'
    option hwmode '11a'
    option phy 'phy0'
    option type 'mac80211'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_render_radio_list_option(self):
        o = OpenWrt(
            {
                "radios": [
                    {
                        "name": "radio0",
                        "phy": "phy0",
                        "driver": "mac80211",
                        "protocol": "802.11n",
                        "channel": 1,
                        "channel_width": 20,
                        "ht_capab": ["SMPS-STATIC", "SHORT-GI-20"],
                    }
                ]
            }
        )
        expected = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel '1'
    list ht_capab 'SMPS-STATIC'
    list ht_capab 'SHORT-GI-20'
    option htmode 'HT20'
    option hwmode '11g'
    option phy 'phy0'
    option type 'mac80211'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_render_atheros_driver(self):
        expected = self._tabs(
            """package wireless

config wifi-device 'wifi0'
    option channel '6'
    option channel_width '20'
    option disabled '0'
    option hwmode '11g'
    option phy 'wifi0'
    option type 'atheros'
"""
        )
        o = OpenWrt(
            {
                "radios": [
                    {
                        "protocol": "802.11g",
                        "name": "wifi0",
                        "phy": "wifi0",
                        "channel": 6,
                        "channel_width": 20,
                        "disabled": False,
                        "driver": "atheros",
                    }
                ]
            }
        )
        self.assertEqual(o.render(), expected)

    def test_parse_radio_list_option(self):
        native = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel '1'
    list ht_capab 'SMPS-STATIC'
    list ht_capab 'SHORT-GI-20'
    option htmode 'HT20'
    option hwmode '11g'
    option phy 'phy0'
    option type 'mac80211'
"""
        )
        expected = {
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 1,
                    "channel_width": 20,
                    "ht_capab": ["SMPS-STATIC", "SHORT-GI-20"],
                }
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_render_htmode_override(self):
        o = OpenWrt(
            {
                "radios": [
                    {
                        "name": "radio0",
                        "phy": "phy0",
                        "driver": "mac80211",
                        "protocol": "802.11n",
                        "channel": 140,
                        "channel_width": 40,
                        "htmode": "HT40+",
                    },
                ]
            }
        )
        expected = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel '140'
    option htmode 'HT40+'
    option hwmode '11a'
    option phy 'phy0'
    option type 'mac80211'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_htmode_override(self):
        native = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel '140'
    option htmode 'HT40+'
    option hwmode '11a'
    option phy 'phy0'
    option type 'mac80211'
"""
        )
        expected = {
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 140,
                    "channel_width": 40,
                    "htmode": "HT40+",
                },
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_default_driver(self):
        o = OpenWrt(
            {
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
                ]
            }
        )
        expected = self._tabs(
            """package wireless

config wifi-device 'radio0'
    option channel '1'
    option country 'US'
    option disabled '0'
    option htmode 'VHT80'
    option hwmode '11g'
    option phy 'phy0'
    option txpower '10'
    option type 'mac80211'
"""
        )
        self.assertEqual(o.render(), expected)
