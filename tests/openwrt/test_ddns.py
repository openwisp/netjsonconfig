import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestDdns(unittest.TestCase, _TabsMixin):
    maxDiff = None
    _ddns_netjson_global = {
        "ddns": {
            "ddns_dateformat": "%F %R",
            "ddns_logdir": "/var/log/ddns",
            "ddns_loglines": 250,
            "ddns_rundir": "/var/run/ddns",
            "upd_privateip": False,
            "use_curl": False
        }
    }
    _ddns_uci_global = """package ddns

config ddns 'global'
    option ddns_dateformat '%F %R'
    option ddns_logdir '/var/log/ddns'
    option ddns_loglines '250'
    option ddns_rundir '/var/run/ddns'
    option upd_privateip '0'
    option use_curl '0'
"""

    def test_render_ddns_global(self):
        o = OpenWrt(self._ddns_netjson_global)
        expected = self._tabs(self._ddns_uci_global)
        self.assertEqual(o.render(), expected)

    def test_parse_ddns_global(self):
        o = OpenWrt(native=self._ddns_uci_global)
        self.assertDictEqual(o.config, self._ddns_netjson_global)
