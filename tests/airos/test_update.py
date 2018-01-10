from .mock import ConverterTest, UpdateAirOs


class TestUpdateConverter(ConverterTest):
    backend = UpdateAirOs

    def test_status(self):
        o = self.backend({})
        o.to_intermediate()
        expected = [
            {'check.status': 'enabled'}
        ]
        self.assertEqualConfig(o.intermediate_data['update'], expected)
