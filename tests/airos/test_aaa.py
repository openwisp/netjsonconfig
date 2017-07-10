from .dummy import AaaAirOS, ConverterTest


class TestResolvConverter(ConverterTest):

    backend = AaaAirOS

    def test_aaa_key(self):
        o = self.backend({
            "general": {}
        })

        o.to_intermediate()

        expected = [
                {
                    'status': 'disabled',
                },
        ]

        self.assertEqualConfig(o.intermediate_data['aaa'], expected)
