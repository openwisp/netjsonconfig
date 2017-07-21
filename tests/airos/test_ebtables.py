from .mock import ConverterTest, EbtablesAirOs


class EbtablesConverter(ConverterTest):
    backend = EbtablesAirOs

    def test_ebtables(self):
        o = self.backend({})
        o.to_intermediate()
        expected = [
            {
                'sys.fw.status': 'disabled',
                'sys.status': 'enabled',
                'status': 'enabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['ebtables'], expected)
