from .mock import ConverterTest, TshaperAirOs


class TestTshaperConverter(ConverterTest):
    backend = TshaperAirOs

    def test_active(self):
        o = self.backend({})
        o.to_intermediate()
        expected = [{'status': 'disabled'}]
        self.assertEqualConfig(o.intermediate_data['tshaper'], expected)
