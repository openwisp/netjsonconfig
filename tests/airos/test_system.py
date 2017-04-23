import unittest

from netjsonconfig import AirOS
from netjsonconfig.exceptions import ValidationError
from netjsonconfig.utils import _TabsMixin


class TestSystemRenderer(unittest.TestCase, _TabsMixin):
    """
    tests for backends.airos.renderers.SystemRenderer
    """
    def test_resolv(self):
        o = AirOS({
            "dns_server": [
                "10.150.42.1"
            ]
        })
        expected = self._tabs("""resolv.status=disabled
resolv.nameserver.status=enabled
resolv.nameserver.1.status=enabled
resolv.nameserver.1.ip=10.150.42.1
""")
        self.assertEqual(o.render(), expected)
