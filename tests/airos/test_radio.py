from .dummy import RadioAirOS, ConverterTest


class TestRadioConverter(ConverterTest):

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

        self.assertEqualConfig(o.intermediate_data['radio'], expected)

    def test_active_radio(self):
        o = self.backend({
            "radios": [
                {
                    'name': 'ath0',
                    'channel': 1,
                    'channel_width': 20,
                    'disabled': False,
                    'protocol': '802.11n',
                }
            ]
        })

        o.to_intermediate()

        expected = [
                {
                    '1.chanbw': 20,
                    '1.devname': 'ath0',
                    '1.status': 'enabled',
                    '1.txpower': '',
                },
                {
                    'status': 'enabled',
                },
        ]

        self.assertEqualConfig(o.intermediate_data['radio'], expected)

    def test_inactive_radio(self):
        o = self.backend({
            "radios": [
                {
                    'name': 'ath0',
                    'channel': 1,
                    'channel_width': 20,
                    'disabled': True,
                    'protocol': '802.11n',
                }
            ]
        })

        o.to_intermediate()

        expected = [
                {
                    '1.chanbw': 20,
                    '1.devname': 'ath0',
                    '1.status': 'disabled',
                    '1.txpower': '',
                },
                {
                    'status': 'enabled',
                },
        ]

        self.assertEqualConfig(o.intermediate_data['radio'], expected)
