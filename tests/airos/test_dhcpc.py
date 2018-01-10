from .mock import ConverterTest, DhcpcAirOs


class TestDhcpcConverter(ConverterTest):

    backend = DhcpcAirOs

    def test_bridge(self):
        o = self.backend({
            'netmode': 'bridge',
        })
        o.to_intermediate()

        with self.assertRaises(KeyError):
            o.intermediate_data['dhcpc']

    def test_router(self):
        o = self.backend({
            'netmode': 'router',
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            [
                {
                    'devname': 'br0',
                    'fallback': '192.168.10.1',
                    'fallback_netmask': '255.255.255.0',
                    'status': 'enabled',
                },
            ]
        ]

        self.assertEqualConfig(o.intermediate_data['dhcpc'], expected)
