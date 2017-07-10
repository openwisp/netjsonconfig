from .dummy import DiscoveryAirOS, ConverterTest


class TestDiscoveryConverter(ConverterTest):

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


        self.assertEqualConfig(o.intermediate_data['discovery'], expected)
