import unittest

from .dummy import GuiAirOS


class TestGuiConverter(unittest.TestCase):

    backend = GuiAirOS

    def test_gui_key(self):
        o = self.backend({
            "general": {}
        })

        o.to_intermediate()

        expected = [
                {
                    'network': {
                        'advanced': {
                            'status': 'enabled',
                        },
                    }
                },
                {
                    'language': 'en_US',
                },
        ]


        self.assertEqual(o.intermediate_data['gui'], expected)
