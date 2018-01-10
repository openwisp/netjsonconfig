from .mock import ConverterTest, EbtablesAirOs


class EbtablesConverterBridge(ConverterTest):
    backend = EbtablesAirOs

    def test_station_none(self):
        o = self.backend({
            'interfaces': [
                {
                    'type': 'wireless',
                    'name': 'wlan0',
                    'wireless': {
                        'mode': 'station',
                        'radio': 'ath0',
                        'ssid': 'ubnt',
                        'bssid': '00:11:22:33:44:55',
                    }
                }
            ]
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                'sys.fw.status': 'disabled',
                'sys.status': 'enabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['ebtables'], expected)

    def test_station_psk(self):
        o = self.backend({
            'interfaces': [
                {
                    'type': 'wireless',
                    'name': 'wlan0',
                    'wireless': {
                        'mode': 'station',
                        'radio': 'ath0',
                        'ssid': 'ubnt',
                        'bssid': '00:11:22:33:44:55',
                        'encryption': {
                            'protocol': 'wpa2_personal',
                            'key': 'changeme',
                        }
                    }
                }
            ]
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                'sys.eap.1.devname': 'ath0',
                'sys.eap.1.status': 'enabled',
                'sys.eap.status': 'enabled',
                'sys.fw.status': 'disabled',
                'sys.status': 'enabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['ebtables'], expected)

    def test_station_eap(self):
        o = self.backend({
            'interfaces': [
                {
                    'type': 'wireless',
                    'name': 'wlan0',
                    'wireless': {
                        'mode': 'station',
                        'radio': 'ath0',
                        'ssid': 'ubnt',
                        'bssid': '00:11:22:33:44:55',
                        'encryption': {
                            'protocol': 'wpa2_enterprise',
                            'identity': 'name@domain.com',
                            'key': 'changeme',
                        }
                    }
                }
            ]
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                'sys.eap.1.devname': 'ath0',
                'sys.eap.1.status': 'enabled',
                'sys.eap.status': 'enabled',
                'sys.fw.status': 'disabled',
                'sys.status': 'enabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['ebtables'], expected)

    def test_access_none(self):
        o = self.backend({
            'interfaces': [
                {
                    'type': 'wireless',
                    'name': 'wlan0',
                    'wireless': {
                        'mode': 'access_point',
                        'radio': 'ath0',
                        'ssid': 'ubnt',
                    }
                }
            ]
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                'sys.fw.status': 'disabled',
                'sys.status': 'enabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['ebtables'], expected)

    def test_access_psk(self):
        o = self.backend({
            'interfaces': [
                {
                    'type': 'wireless',
                    'name': 'wlan0',
                    'wireless': {
                        'mode': 'access_point',
                        'radio': 'ath0',
                        'ssid': 'ubnt',
                        'encryption': {
                            'protocol': 'wpa2_personal',
                            'key': 'changeme',
                        }
                    }
                }
            ]
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                'sys.eap.1.devname': 'ath0',
                'sys.eap.1.status': 'enabled',
                'sys.eap.status': 'enabled',
                'sys.fw.status': 'disabled',
                'sys.status': 'enabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['ebtables'], expected)

    def test_access_eap(self):
        o = self.backend({
            'interfaces': [
                {
                    'type': 'wireless',
                    'name': 'wlan0',
                    'wireless': {
                        'mode': 'access_point',
                        'radio': 'ath0',
                        'ssid': 'ubnt',
                        'encryption': {
                            'protocol': 'wpa2_enterprise',
                            'server': '192.168.1.1',
                            'key': 'changeme',
                        }
                    }
                }
            ]
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                'sys.eap.1.devname': 'ath0',
                'sys.eap.1.status': 'enabled',
                'sys.eap.status': 'enabled',
                'sys.fw.status': 'disabled',
                'sys.status': 'enabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['ebtables'], expected)


class EbtablesConverterRouter(ConverterTest):
    backend = EbtablesAirOs

    def test_station_none(self):
        o = self.backend({
            'interfaces': [
                {
                    'type': 'wireless',
                    'name': 'wlan0',
                    'wireless': {
                        'mode': 'station',
                        'radio': 'ath0',
                        'ssid': 'ubnt',
                        'bssid': '00:11:22:33:44:55',
                    }
                }
            ],
            "netmode": "router",
        })
        o.to_intermediate()
        expected = []
        self.assertEqualConfig(o.intermediate_data['ebtables'], expected)

    def test_station_psk(self):
        o = self.backend({
            'interfaces': [
                {
                    'type': 'wireless',
                    'name': 'wlan0',
                    'wireless': {
                        'mode': 'station',
                        'radio': 'ath0',
                        'ssid': 'ubnt',
                        'bssid': '00:11:22:33:44:55',
                        'encryption': {
                            'protocol': 'wpa2_personal',
                            'key': 'changeme',
                        }
                    }
                }
            ],
            "netmode": "router",
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                'sys.eap.1.devname': 'ath0',
                'sys.eap.1.status': 'enabled',
                'sys.eap.status': 'enabled',
                'sys.status': 'enabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['ebtables'], expected)

    def test_station_eap(self):
        o = self.backend({
            'interfaces': [
                {
                    'type': 'wireless',
                    'name': 'wlan0',
                    'wireless': {
                        'mode': 'station',
                        'radio': 'ath0',
                        'ssid': 'ubnt',
                        'bssid': '00:11:22:33:44:55',
                        'encryption': {
                            'protocol': 'wpa2_enterprise',
                            'identity': 'name@domain.com',
                            'key': 'changeme',
                        }
                    }
                }
            ],
            "netmode": "router",
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                'sys.eap.1.devname': 'ath0',
                'sys.eap.1.status': 'enabled',
                'sys.eap.status': 'enabled',
                'sys.status': 'enabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['ebtables'], expected)

    def test_access_none(self):
        o = self.backend({
            'interfaces': [
                {
                    'type': 'wireless',
                    'name': 'wlan0',
                    'wireless': {
                        'mode': 'access_point',
                        'radio': 'ath0',
                        'ssid': 'ubnt',
                    }
                }
            ],
            "netmode": "router",
        })
        o.to_intermediate()
        expected = []
        self.assertEqualConfig(o.intermediate_data['ebtables'], expected)

    def test_access_psk(self):
        o = self.backend({
            'interfaces': [
                {
                    'type': 'wireless',
                    'name': 'wlan0',
                    'wireless': {
                        'mode': 'access_point',
                        'radio': 'ath0',
                        'ssid': 'ubnt',
                        'encryption': {
                            'protocol': 'wpa2_personal',
                            'key': 'changeme',
                        }
                    }
                }
            ],
            "netmode": "router",
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                'sys.eap.1.devname': 'ath0',
                'sys.eap.1.status': 'enabled',
                'sys.eap.status': 'enabled',
                'sys.status': 'enabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['ebtables'], expected)

    def test_access_eap(self):
        o = self.backend({
            'interfaces': [
                {
                    'type': 'wireless',
                    'name': 'wlan0',
                    'wireless': {
                        'mode': 'access_point',
                        'radio': 'ath0',
                        'ssid': 'ubnt',
                        'encryption': {
                            'protocol': 'wpa2_enterprise',
                            'server': '192.168.1.1',
                            'key': 'radius-change-me',
                        }
                    }
                }
            ],
            "netmode": "router",
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                'sys.eap.1.devname': 'ath0',
                'sys.eap.1.status': 'enabled',
                'sys.eap.status': 'enabled',
                'sys.status': 'enabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['ebtables'], expected)
