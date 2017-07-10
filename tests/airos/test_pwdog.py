from .dummy import PwdogAirOS, ConverterTest


class TestPwdogConverter(ConverterTest):

    backend = PwdogAirOS

    def test_ntp_key(self):
        o = self.backend({
            "general": {}
        })

        o.to_intermediate()

        expected = [
                {
                    'delay': 300,
                    'period': 300,
                    'retry': 3,
                    'status': 'enabled',
                },
        ]

        self.assertEqualConfig(o.intermediate_data['pwdog'], expected)
