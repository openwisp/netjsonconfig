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
                    'language': 'en_US',
                },
                {
                    'network.advanced.status': 'enabled',
                },
        ]


        self.assertEqual(o.intermediate_data['gui'], expected)
