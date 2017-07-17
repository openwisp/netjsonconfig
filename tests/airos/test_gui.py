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
