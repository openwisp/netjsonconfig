from .mock import ConverterTest, EbtablesAirOs


class EbtablesConverter(ConverterTest):
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
                'sys.fw.status': 'disabled',
                'sys.status': 'enabled',
                'status': 'enabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['ebtables'], expected)
