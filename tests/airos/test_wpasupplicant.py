from unittest import skip

from netjsonconfig.exceptions import ValidationError

from .dummy import WpasupplicantAirOS, ConverterTest


class TestWpasupplicantStation(ConverterTest):
    """
    Test the wpasupplicant converter for a
    device in ``station`` mode
    """
    backend = WpasupplicantAirOS

    def test_invalid_encryption(self):

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
                        "mode": "station",
                        "ssid": "ap-ssid-example",
                    },
                    "encryption": {
                        "protocol": "wep",
                    },
                }
            ]
        })
        with self.assertRaises(ValidationError):
            o.validate()

    def test_no_encryption(self):

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
                        "mode": "station",
                        "ssid": "ap-ssid-example",
                        "bssid": "00:11:22:33:44:55",
                    },
                    "encryption": {
                        "protocol": "none",
                    },
                }
            ]
        })

        o.to_intermediate()

        expected = [
                    {
                        'device.1.profile': 'AUTO',
                        'device.1.status': 'disabled',
                        'profile.1.name': 'AUTO',
                        'profile.1.network.1.phase2=auth': 'MSCHAPV2',
                        'profile.1.network.1.ssid': 'ap-ssid-example',
                        'profile.1.network.1.priority': 100,
                        'profile.1.network.1.key_mgmt.1.name': 'NONE',
                        'profile.1.network.2.key_mgmt.1.name': 'NONE',
                        'profile.1.network.2.priority': 2,
                        'profile.1.network.2.status': 'disabled',
                    },
                    {
                        'status': 'enabled',
                    }
                ]

        self.assertEqualConfig(o.intermediate_data['wpasupplicant'], expected)

    def test_wpa2_personal(self):

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
                        "mode": "station",
                        "ssid": "ap-ssid-example",
                        "bssid": "00:11:22:33:44:55",
                    },
                    "encryption": {
                        "protocol": "wpa2_personal",
                        "key": "cucumber",
                    },
                }
            ]
        })

        o.to_intermediate()

        expected = [
                    {
                        'device.1.profile': 'AUTO',
                        'device.1.status': 'enabled',
                        'device.1.driver': 'madwifi',
                        'device.1.devname': 'radio0',
                        'profile.1.name': 'AUTO',
                        'profile.1.network.1.phase2=auth': 'MSCHAPV2',
                        'profile.1.network.1.eap.1.status': 'disabled',
                        'profile.1.network.1.psk': 'cucumber',
                        'profile.1.network.1.pairwise.1.name': 'CCMP',
                        'profile.1.network.1.proto.1.name': 'RSN',
                        'profile.1.network.1.ssid': 'ap-ssid-example',
                        'profile.1.network.1.priority': 100,
                        'profile.1.network.1.key_mgmt.1.name': 'WPA-PSK',
                        'profile.1.network.2.key_mgmt.1.name': 'NONE',
                        'profile.1.network.2.priority': 2,
                        'profile.1.network.2.status': 'disabled',
                    },
                    {
                        'status': 'enabled',
                    }
                ]

        self.assertEqualConfig(o.intermediate_data['wpasupplicant'], expected)

    @skip("target wpa2_enterprise later")
    def test_wpa2_enterprise(self):

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
                        "mode": "station",
                        "ssid": "ap-ssid-example",
                    },
                    "encryption": {
                        "protocol": "wpa2_enterprise",
                        "key": "cucumber",
                    },
                }
            ]
        })

        o.to_intermediate()

        expected = [
                    {
                        'device.1.profile': 'AUTO',
                        'device.1.status': 'enabled',
                        'device.1.driver': 'madwifi',
                        'device.1.devname': 'radio0',
                        'profile.1.name': 'AUTO',
                        'profile.1.network.1.phase2=auth': 'MSCHAPV2',
                        'profile.1.network.1.eap.1.status': 'enabled',
                        'profile.1.network.1.eap.1.name': 'TTLS',
                        'profile.1.network.1.password': 'TODO',
                        'profile.1.network.1.identity': 'TODO',
                        'profile.1.network.1.anonymous_identity': 'TODO',
                        'profile.1.network.1.psk': 'cucumber',
                        'profile.1.network.1.pairwise.1.name': 'CCMP',
                        'profile.1.network.1.proto.1.name': 'RSN',
                        'profile.1.network.1.ssid': 'ap-ssid-example',
                        'profile.1.network.1.priority': 100,
                        'profile.1.network.1.key_mgmt.1.name': 'WPA-EAP',
                        'profile.1.network.2.key_mgmt.1.name': 'NONE',
                        'profile.1.network.2.priority': 2,
                        'profile.1.network.2.status': 'disabled',
                    },
                    {
                        'status': 'enabled',
                    }
                ]

        self.assertEqualConfig(o.intermediate_data['wpasupplicant'], expected)


class TestWpasupplicantAccess(ConverterTest):
    """
    Test the wpasupplicant converter for a
    device in ``access_point`` mode
    """

    backend = WpasupplicantAirOS
