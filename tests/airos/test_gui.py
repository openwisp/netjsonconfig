from .mock import ConverterTest, GuiAirOs


class TestGuiConverter(ConverterTest):

    backend = GuiAirOs

    def test_gui_key(self):
        o = self.backend({
            'gui': {},
        })
        o.to_intermediate()
        expected = [
            {
                'language': 'en_US',
            },
            {
                'network.advanced.status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['gui'], expected)

    def test_language(self):
        o = self.backend({
            'gui': {
                'language' : 'it_IT',
            },
        })
        o.to_intermediate()
        expected = [
            {
                'language': 'it_IT',
            },
            {
                'network.advanced.status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['gui'], expected)
