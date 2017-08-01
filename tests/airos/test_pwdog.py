from .mock import ConverterTest, PwdogAirOs


class TestPwdogConverter(ConverterTest):

    backend = PwdogAirOs

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
                'status': 'disabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['pwdog'], expected)
