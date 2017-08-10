from .mock import AaaAirOs, ConverterTest


class TestAaaConverterAccess(ConverterTest):

    backend = AaaAirOs

    def test_ap_no_authentication(self):
        o = self.backend({
            "interfaces": [
                {
                    "type": "wireless",
                    "name": "wlan0",
                    "wireless": {
                        "mode": "access_point",
                        "radio": "ath0",
                        "ssid": "i-like-pasta",
                        "encryption": {
                            "protocol": "none"
                        }
                    },
                },
                {
                    "type": "bridge",
                    "name": "br0",
                    "bridge_members": [
                        "wlan0",
                    ],
                },
            ],
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'disabled',
            },
            {
                '1.radius.acct.1.port': 1813,
                '1.radius.acct.1.status': 'disabled',
                '1.radius.auth.1.port': 1812,
                '1.status': 'disabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['aaa'], expected)

    def test_ap_psk_authentication(self):
        o = self.backend({
            "interfaces": [
                {
                    "type": "wireless",
                    "name": "wlan0",
                    "wireless": {
                        "mode": "access_point",
                        "radio": "ath0",
                        "ssid": "i-like-pasta",
                        "encryption": {
                            "protocol": "wpa2_personal",
                            "key": "and-pizza-too",
                        },
                    },
                },
                {
                    "type": "bridge",
                    "name": "br0",
                    "bridge_members": [
                        "wlan0",
                    ],
                },
            ],
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                '1.radius.acct.1.port': 1813,
                '1.radius.acct.1.status': 'disabled',
                '1.radius.auth.1.port': 1812,
                '1.radius.auth.1.status': 'disabled',
                '1.status': 'enabled',
                '1.wpa.psk': 'and-pizza-too',
                '1.radius.macacl.status': 'disabled',
                '1.ssid': 'i-like-pasta',
                '1.br.devname': 'br0',  # only in bridge mode?
                '1.devname': 'ath0',
                '1.driver': 'madwifi',
                '1.wpa.1.pairwise': 'CCMP',
                '1.wpa.key.1.mgmt': 'WPA-PSK',
                '1.wpa.mode': 2,
            }
        ]
        self.assertEqualConfig(o.intermediate_data['aaa'], expected)

    def test_ap_eap_authentication(self):
        o = self.backend({
            "interfaces": [
                {
                    "type": "wireless",
                    "name": "wlan0",
                    "wireless": {
                        "mode": "access_point",
                        "radio": "ath0",
                        "ssid": "i-like-pasta",
                        "encryption": {
                            "protocol": "wpa2_enterprise",
                            "key": "secret-radius-key",
                            "server": "192.168.1.1",
                            "acct_server": "192.168.1.2",
                        },
                    },
                },
                {
                    "type": "bridge",
                    "name": "br0",
                    "bridge_members": [
                        "wlan0",
                    ],
                },
            ],
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                '1.br.devname': 'br0',  # only in bridge mode?
                '1.devname': 'ath0',
                '1.driver': 'madwifi',
                '1.radius.acct.1.port': 1813,
                '1.radius.acct.1.status': 'enabled',
                '1.radius.acct.1.ip': '192.168.1.2',
                '1.radius.auth.1.ip': '192.168.1.1',
                '1.radius.auth.1.port': 1812,
                '1.radius.auth.1.secret': 'secret-radius-key',
                '1.radius.auth.1.status': 'enabled',
                '1.radius.macacl.status': 'disabled',
                '1.ssid': 'i-like-pasta',
                '1.status': 'enabled',
                '1.wpa.1.pairwise': 'CCMP',
                '1.wpa.key.1.mgmt': 'WPA-EAP',
                '1.wpa.mode': 2,
            }
        ]
        self.assertEqualConfig(o.intermediate_data['aaa'], expected)


class TestAaaConverterStation(ConverterTest):

    backend = AaaAirOs

    def test_sta_no_authentication(self):
        o = self.backend({
            "interfaces": [
                {
                    "type": "wireless",
                    "name": "wlan0",
                    "wireless": {
                        "mode": "station",
                        "radio": "ath0",
                        "ssid": "i-like-pasta",
                        "bssid": "00:11:22:33:44:55",
                        "encryption": {
                            "protocol": "none",
                        },
                    },
                },
                {
                    "type": "bridge",
                    "name": "br0",
                    "bridge_members": [
                        "wlan0",
                    ],
                },
            ],
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'disabled',
            },
            {
                '1.radius.acct.1.port': 1813,
                '1.radius.acct.1.status': 'disabled',
                '1.radius.auth.1.port': 1812,
                '1.status': 'disabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['aaa'], expected)

    def test_sta_psk_authentication(self):
        o = self.backend({
            "interfaces": [
                {
                    "type": "wireless",
                    "name": "wlan0",
                    "wireless": {
                        "mode": "station",
                        "radio": "ath0",
                        "ssid": "i-like-pasta",
                        "bssid": "00:11:22:33:44:55",
                        "encryption": {
                            "protocol": "wpa2_personal",
                            "key": "and-pizza-too",
                        },
                    },
                },
                {
                    "type": "bridge",
                    "name": "br0",
                    "bridge_members": [
                        "wlan0",
                    ],
                },
            ],
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'disabled',
            },
            {
                '1.radius.acct.1.port': 1813,
                '1.radius.acct.1.status': 'disabled',
                '1.radius.auth.1.port': 1812,
                '1.status': 'disabled',
                '1.wpa.psk': 'and-pizza-too',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['aaa'], expected)

    def test_sta_eap_authentication(self):
        o = self.backend({
            "interfaces": [
                {
                    "type": "wireless",
                    "name": "wlan0",
                    "wireless": {
                        "mode": "station",
                        "radio": "ath0",
                        "ssid": "i-like-pasta",
                        "bssid": "00:11:22:33:44:55",
                        "encryption": {
                            "protocol": "wpa2_enterprise",
                            "identity": "some-fake-identity",
                            "password": "password1234",
                        },
                    },
                },
                {
                    "type": "bridge",
                    "name": "br0",
                    "bridge_members": [
                        "wlan0",
                    ],
                },
            ],
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'disabled',
            },
            {
                '1.radius.acct.1.port': 1813,
                '1.radius.acct.1.status': 'disabled',
                '1.radius.auth.1.port': 1812,
                '1.status': 'disabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['aaa'], expected)
