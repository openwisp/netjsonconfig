from unittest import TestCase

from netjsonconfig.backends.airos.interface import (autonegotiation, bssid, encryption,
                                                    flowcontrol, hidden_ssid, stp)


class InterfaceTest(TestCase):
    def test_autonegotiation(self):
        enabled = {
            'type': "ethernet",
            'name': "eth0",
            'autoneg': True,
        }
        disabled = {
            'type': "ethernet",
            'name': "eth0",
            'autoneg': False,
        }
        missing = {
            'type': "ethernet",
            'name': "eth0",
        }
        self.assertEqual(autonegotiation(enabled), 'enabled')
        self.assertEqual(autonegotiation(disabled), 'disabled')
        self.assertEqual(autonegotiation(missing), 'disabled')

    def test_bssid(self):
        present = {
            'type': 'wireless',
            'name': 'wlan0',
            'wireless': {
                'mode': 'station',
                'ssid': 'ubnt',
                'bssid': '00:11:22:33:44:55',
            }
        }
        missing = {
            'type': 'wireless',
            'name': 'wlan0',
            'wireless': {
                'mode': 'station',
                'ssid': 'ubnt',
            }
        }

        self.assertEqual(bssid(present), '00:11:22:33:44:55')
        self.assertEqual(bssid(missing), '')

    def test_encryption(self):
        present = {
            'type': 'wireless',
            'name': 'wlan0',
            'wireless': {
                'mode': 'station',
                'ssid': 'ubnt',
                'encryption': {
                    'protocol': 'wpa2_personal',
                    'password': 'changeme',
                },
            }
        }
        missing = {
            'type': 'wireless',
            'name': 'wlan0',
            'wireless': {
                'mode': 'station',
                'ssid': 'ubnt',
            }
        }
        self.assertEqual(encryption(present), {'protocol': 'wpa2_personal', 'password': 'changeme'})
        self.assertEqual(encryption(missing), {'protocol': 'none'})

    def test_flowcontrol(self):
        enabled = {
            'type': "ethernet",
            'name': "eth0",
            'flowcontrol': True,
        }
        disabled = {
            'type': "ethernet",
            'name': "eth0",
            'flowcontrol': False,
        }
        missing = {
            'type': "ethernet",
            'name': "eth0",
        }
        expected_enabled = {
            'rx': {
                'status': 'enabled',
            },
            'tx': {
                'status': 'enabled',
            },
        }
        expected_disabled = {
            'rx': {
                'status': 'disabled',
            },
            'tx': {
                'status': 'disabled',
            },
        }
        self.assertEqual(flowcontrol(enabled), expected_enabled)
        self.assertEqual(flowcontrol(disabled), expected_disabled)
        self.assertEqual(flowcontrol(missing), expected_disabled)

    def test_hidden_ssid(self):
        enabled = {
            'type': 'wireless',
            'name': 'wlan0',
            'wireless': {
                'mode': 'station',
                'ssid': 'ubnt',
                'hidden': True,
            }
        }
        disabled = {
            'type': 'wireless',
            'name': 'wlan0',
            'wireless': {
                'mode': 'station',
                'ssid': 'ubnt',
                'hidden': False,
            }
        }
        missing = {
            'type': 'wireless',
            'name': 'wlan0',
            'wireless': {
                'mode': 'station',
                'ssid': 'ubnt',
            }
        }
        self.assertEqual(hidden_ssid(enabled), 'enabled')
        self.assertEqual(hidden_ssid(disabled), 'disabled')
        self.assertEqual(hidden_ssid(missing), 'disabled')

    def test_stp(self):
        enabled = {
            'type': 'bridge',
            'name': 'br0',
            'stp': True,
        }
        disabled = {
            'type': 'bridge',
            'name': 'br0',
            'stp': False,
        }
        missing = {
            'type': 'bridge',
            'name': 'br0',
        }
        self.assertEqual(stp(enabled), 'enabled')
        self.assertEqual(stp(disabled), 'disabled')
        self.assertEqual(stp(missing), 'disabled')
