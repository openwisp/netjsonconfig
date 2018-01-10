from .mock import ConverterTest, IgmpproxyAirOs


class Igmpproxyconverter(ConverterTest):
    backend = IgmpproxyAirOs

    def test_ebtables(self):
        o = self.backend({})
        o.to_intermediate()
        expected = [
            {
                'status': 'disabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['igmpproxy'], expected)
