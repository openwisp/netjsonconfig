from .mock import ConverterTest, UnmsAirOs


class TestUnmsConverter(ConverterTest):
    backend = UnmsAirOs

    def test_active(self):
        o = self.backend({})
        o.to_intermediate()
        expected = [{'status': 'disabled'}]
        self.assertEqualConfig(o.intermediate_data['unms'], expected)
