import unittest

from netjsonconfig import Raspbian

class TestResovlConverter(unittest.TestCase):

    def test_dns_server(self):
        o = Raspbian({
            "dns_servers": [
                "10.254.0.1",
                "10.254.0.2"
            ],
        })

        o.to_intermediate()

        expected = [OrderedDict([
            ('nameserver', [
                {'ip': '10.254.0.1'},
                {'ip': '10.254.0.2'}
                ])
            ])
        ]
        self.assertEqual(o.intermediate_data['dns_servers'], expected)

    def test_dns_search(self):
        o = Raspbian({
            "dns_search": [
                "domain.com",
            ],
        })

        o.to_intermediate()

        expected = [OrderedDict([
            ('domain', [
                {'domain': 'domain.com'}
                ])
            ])
        ]
        self.assertEqual(o.intermediate_data['dns_search'], expected)
