import unittest

from .dummy import WirelessAirOS, ConverterTest


class TestWirelessConverter(ConverterTest):

    backend = WirelessAirOS

    def test_active_wireless(self):

        o = self.backend({
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
                        }
                    ],
                }
            ]
        })

        o.to_intermediate()

        expected = [
                    {
                        '1.addmtikie': 'enabled',
                        '1.devname': 'radio0',
                        '1.hide_ssid': 'disabled',
                        '1.security.type': 'none',
                        '1.signal_led1': 75,
                        '1.signal_led2': 50,
                        '1.signal_led3': 25,
                        '1.signal_led4': 15,
                        '1.signal_led_status': 'enabled',
                        '1.ssid': 'ap-ssid-example',
                        '1.status': 'enabled',
                        '1.wds.status': 'enabled',
                    },
                    {
                        'status': 'enabled',
                    }
                ]

        self.assertEqualConfig(o.intermediate_data['wireless'], expected)

    def test_inactive_wireless(self):

        o = self.backend({
            "interfaces": [
                {
                    "type": "wireless",
                    "name": "wlan0",
                    "mac": "de:9f:db:30:c9:c5",
                    "mtu": 1500,
                    "txqueuelen": 1000,
                    "autostart": True,
                    "disabled": True,
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
                        }
                    ],
                }
            ]
        })

        o.to_intermediate()

        expected = [
                    {
                        '1.addmtikie': 'enabled',
                        '1.devname': 'radio0',
                        '1.hide_ssid': 'disabled',
                        '1.security.type': 'none',
                        '1.signal_led1': 75,
                        '1.signal_led2': 50,
                        '1.signal_led3': 25,
                        '1.signal_led4': 15,
                        '1.signal_led_status': 'enabled',
                        '1.ssid': 'ap-ssid-example',
                        '1.status': 'disabled',
                        '1.wds.status': 'enabled',
                    },
                    {
                        'status': 'enabled',
                    }
                ]

        self.assertEqualConfig(o.intermediate_data['wireless'], expected)
