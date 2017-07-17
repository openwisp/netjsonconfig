from .mock import AaaAirOs, ConverterTest


class TestResolvConverter(ConverterTest):

    backend = AaaAirOs

    def test_aaa_key(self):
        o = self.backend({
            "general": {},
            "interfaces": [],
        })
        o.to_intermediate()
        expected = [
                {
                    'status': 'disabled',
                },
        ]

        self.assertEqualConfig(o.intermediate_data['aaa'], expected)
