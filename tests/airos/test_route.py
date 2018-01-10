from .mock import ConverterTest, RouteAirOs


class TestRouteConverter(ConverterTest):

    backend = RouteAirOs

    def test_gateway_interface(self):
        o = self.backend({
            'interfaces': [{
                'name': 'eth0',
                'type': 'ethernet',
                'addresses': [
                    {
                        'family': 'ipv4',
                        'proto': 'dhcp',
                        'gateway': '192.168.0.1'
                    }
                ]
                }]
        })

        o.to_intermediate()

        expected = [
            {
                '1.devname': 'eth0',
                '1.gateway': '192.168.0.1',
                '1.ip': '0.0.0.0',
                '1.netmask': 0,
                '1.status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['route'], expected)

    def test_user_route(self):
        o = self.backend({
            'routes': [
                {
                    'cost': 0,
                    'destination': '192.178.1.0/24',
                    'device': 'br0',
                    'next': '192.178.1.1',
                    'source': '192.168.1.20',
                }
            ]
        })
        o.to_intermediate()
        expected = [
            {
                '1.ip': '192.178.1.0',
                '1.netmask': '255.255.255.0',
                '1.gateway': '192.178.1.1',
                '1.status': 'enabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['route'], expected)
