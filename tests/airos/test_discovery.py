from .mock import ConverterTest, DiscoveryAirOs


class TestDiscoveryConverter(ConverterTest):

    backend = DiscoveryAirOs

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
