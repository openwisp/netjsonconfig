import unittest

from .dummy import AaaAirOS


class TestResolvConverter(unittest.TestCase):

    backend = AaaAirOS

    def test_aaa_key(self):
        o = self.backend({
            "general": {}
        })

        o.to_intermediate()

        expected = [
                {
                    'status': 'disabled',
                },
        ]


        self.assertEqual(o.intermediate_data['aaa'], expected)
