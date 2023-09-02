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
            "use_curl": False,
            "providers": [
                {
                    "enabled": True,
                    "lookup_host": "myhost.dyndns.org",
                    "service_name": "dyndns.org",
                    "domain": "myhost.dyndns.org",
                    "username": "myuser",
                    "password": "mypassword",
                    "use_logfile": True,
                    "ip_source": "interface",
                    "ip_interface": "pppoe-xdsl",
                    "use_syslog": 2,
                    "interface": "xdsl",
                }
            ],
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

config service 'myhost_dyndns_org'
    option enabled '1'
    option lookup_host 'myhost.dyndns.org'
    option service_name 'dyndns.org'
    option domain 'myhost.dyndns.org'
    option username 'myuser'
    option password 'mypassword'
    option use_logfile '1'
    option ip_source 'interface'
    option ip_interface 'pppoe-xdsl'
    option use_syslog '2'
    option interface 'xdsl'
"""

    def test_render_ddns_global(self):
        result = OpenWrt(self._ddns_netjson_global).render()
        expected = self._tabs(self._ddns_uci_global)
        self.assertEqual(result, expected)

    def test_parse_ddns_global(self):
        result = OpenWrt(native=self._ddns_uci_global).config
        expected = self._ddns_netjson_global
        self.assertDictEqual(result, expected)
