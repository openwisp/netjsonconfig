from .dummy import DyndnsAirOS, ConverterTest


class TestDyndnsConverter(ConverterTest):

    backend = DyndnsAirOS

    def test_Dyndns_key(self):
        o = self.backend({
            "general": {}
        })

        o.to_intermediate()

        expected = [
                {
                    'status': 'disabled',
                },
        ]

        self.assertEqualConfig(o.intermediate_data['dyndns'], expected)
