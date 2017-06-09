import unittest

from .dummy import DyndnsAirOS


class TestDyndnsConverter(unittest.TestCase):

    backend = DyndnsAirOS

    def test_Dyndns_key(self):
        o = self.backend({
            "general": {}
        })

        o.to_intermediate()

        expected = [
                {
                    'status': 'disabled',
                },
        ]


        self.assertEqual(o.intermediate_data['dyndns'], expected)
