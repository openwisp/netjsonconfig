import unittest

from netjsonconfig.backends.airos.converters import *

from .dummy import WirelessAirOS


class TestWirelessConverter(unittest.TestCase):

    backend = WirelessAirOS

    def test_active_wireless(self):

        o = self.backend({
            "interfaces": [
                {
                    "type": "wireless",
                    "name": "wlan0",
                    "mac" : "de:9f:db:30:c9:c5",
                    "mtu" : 1500,
                    "txqueuelen" : 1000,
                    "autostart" : True,
                    "wireless" : {
                        "radio" : "radio0",
                        "mode" : "access_point",
                        "ssid" : "ap-ssid-example",
                    },
                    "addresses" : [
                        {
                            "address" : "192.168.1.1",
                            "mask" : 24,
                            "family" : "ipv4",
                            "proto" : "static",
                        }
                    ],
                }
            ]
        })

        o.to_intermediate()

        expected = [
                    {
                        '1.addmtikie': 'enabled',
                        '1.devname': 'wlan0',
                        '1.hide_ssid': 'disabled',
                        '1.security.type': 'none',
                        '1.ssid': 'ap-ssid-example',
                        '1.status': 'enabled',
                        '1.wds.status': 'enabled',
                    },
                    {
                        'status' : 'enabled',
                    }
                ]

        self.assertEqual(o.intermediate_data['wireless'], expected)
