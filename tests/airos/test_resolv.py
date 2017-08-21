from .mock import ConverterTest, ResolvAirOs


class TestResolvConverter(ConverterTest):

    backend = ResolvAirOs

    def test_resolv(self):
        o = self.backend({
            "dns_servers": [
                "10.150.42.1"
            ],
        })
        o.to_intermediate()
        expected = [
            {
                'host.1.name': 'airos',
                'host.1.status': 'enabled',
            },
            {
                'nameserver.1.ip': '10.150.42.1',
                'nameserver.1.status': 'enabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['resolv'], expected)

    def test_no_dns_server(self):
        o = self.backend({
            "dns_servers": [],
        })
        o.to_intermediate()
        expected = [
            {
                'host.1.name': 'airos',
                'host.1.status': 'enabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['resolv'], expected)

    def test_dns_server(self):
        o = self.backend({
            "dns_servers": [
                "192.168.1.1"
            ],
        })
        o.to_intermediate()
        expected = [
            {
                'host.1.name': 'airos',
                'host.1.status': 'enabled',
            },
            {
                'nameserver.1.ip': '192.168.1.1',
                'nameserver.1.status': 'enabled'
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['resolv'], expected)
