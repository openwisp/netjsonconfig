from .mock import ConverterTest, DyndnsAirOs


class TestDyndnsConverter(ConverterTest):

    backend = DyndnsAirOs

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
