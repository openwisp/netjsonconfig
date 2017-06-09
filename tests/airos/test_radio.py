import unittest

from .dummy import RadioAirOS


class TestRadioConverter(unittest.TestCase):

    backend = RadioAirOS

    def test_no_radio(self):
        o = self.backend({
            "radios": []
        })

        o.to_intermediate()

        expected = [
                {
                    'status': 'enabled',
                },
        ]

        self.assertEqual(o.intermediate_data['radio'], expected)

    def test_active_radio(self):
        o = self.backend({
            "radios": [
                {
                    'name': 'ath0',
                    'channel': 1,
                    'channel_width': 20,
                    'disabled': False,
                }
            ]
        })

        o.to_intermediate()

        expected = [
                {
                    '1.devname': 'ath0',
                    '1.status': 'enabled',
                    '1.txpower': '',
                    '1.chanbw': 20,
                },
                {
                    'status': 'enabled',
                },
        ]

        self.assertEqual(o.intermediate_data['radio'], expected)

    def test_inactive_radio(self):
        o = self.backend({
            "radios": [
                {
                    'name': 'ath0',
                    'channel': 1,
                    'channel_width': 20,
                    'disabled': True,
                }
            ]
        })

        o.to_intermediate()

        expected = [
                {
                    '1.devname': 'ath0',
                    '1.status': 'disabled',
                    '1.txpower': '',
                    '1.chanbw': 20,
                },
                {
                    'status': 'enabled',
                },
        ]

        self.assertEqual(o.intermediate_data['radio'], expected)
