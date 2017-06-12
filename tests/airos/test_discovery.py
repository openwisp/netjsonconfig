import unittest

from .dummy import DiscoveryAirOS


class TestDiscoveryConverter(unittest.TestCase):

    backend = DiscoveryAirOS

    def test_discovery_key(self):
        o = self.backend({
            "general": {}
        })

        o.to_intermediate()

        expected = [
                {
                    'cdp.status': 'enabled',
                    'status': 'enabled',
                },
        ]


        self.assertEqual(o.intermediate_data['discovery'], expected)
