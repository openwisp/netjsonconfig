from .mock import ConverterTest, TelnetdAirOs


class TestTelnetdConverter(ConverterTest):
    backend = TelnetdAirOs

    def test_active(self):
        o = self.backend({})
        o.to_intermediate()
        expected = [
            {
                'port': 23,
                'status': 'disabled'
            }
        ]
        self.assertEqualConfig(o.intermediate_data['telnetd'], expected)
