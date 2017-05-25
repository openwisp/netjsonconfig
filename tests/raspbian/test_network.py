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
