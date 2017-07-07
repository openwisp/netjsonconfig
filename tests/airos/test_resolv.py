import unittest

from .dummy import ResolvAirOS


class TestResolvConverter(unittest.TestCase):

    backend = ResolvAirOS

    def test_resolv(self):
        o = self.backend({
            "dns_servers": [
                "10.150.42.1"
            ],
        })

        o.to_intermediate()

        expected = [
                {
                    'host.1.name' : 'airos',
                },
                {
                    'nameserver.1.ip' : '10.150.42.1',
                    'nameserver.1.status' : 'enabled',
                },
                {
                    'status' : 'enabled',
                },
        ]


        self.assertEqual(o.intermediate_data['resolv'], expected)

    def test_no_dns_server(self):
        o = self.backend({
            "dns_servers": [],
        })

        o.to_intermediate()

        expected = [
                {
                    'host.1.name' : 'airos',
                },
                {
                    'status' : 'enabled',
                },
        ]

        self.assertEqual(o.intermediate_data['resolv'], expected)
