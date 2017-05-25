import unittest

from netjsonconfig import Raspbian
from netjsonconfig.exceptions import ValidationError
from netjsonconfig.utils import _TabsMixin

class TestNetworkRenderer(unittest.TestCase, _TabsMixin):
    def test_dns_server(self):
        o = Raspbian({
            "dns_servers": [
                "10.254.0.1",
                "10.254.0.2"
            ]
        })
        expected = self._tabs("""nameserver​ 10.254.0.1
nameserver​ 10.254.0.2""")
        self.assertEqual(o.render(), expected)

    def test_dns_search(self):
        o = Raspbian({
            "dns_search": [
                "domain.com"
            ]
        })
        expected = self._tabs("""search​ domain.com""")
        self.assertEqual(o.render(), expected)
