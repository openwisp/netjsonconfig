from .mock import ConverterTest, SystemAirOs


class TestSystemConverter(ConverterTest):
    backend = SystemAirOs

    def test_active(self):
        o = self.backend({})
        o.to_intermediate()
        expected = [
            {
                'airosx.prov.status': 'enabled',
                'cfg.version': 0,
                'date.status': 'disabled',
                'external.reset': 'enabled',
                'timezone': 'GMT'
            }
        ]
        self.assertEqualConfig(o.intermediate_data['system'], expected)
