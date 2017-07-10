from .dummy import GuiAirOS, ConverterTest


class TestGuiConverter(ConverterTest):

    backend = GuiAirOS

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
