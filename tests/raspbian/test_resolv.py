import unittest

from netjsonconfig import Raspbian
from netjsonconfig.exceptions import ValidationError
from netjsonconfig.utils import _TabsMixin


class TestResovlRenderer(unittest.TestCase, _TabsMixin):

    def test_dns_server(self):
        o = Raspbian({
            "dns_servers": [
                "10.254.0.1",
                "10.254.0.2"
            ],
        })

        expected = '''/etc/network/interfaces
-----------------------


/etc/resolv.conf
----------------
nameserver 10.254.0.1
nameserver 10.254.0.2
'''
        self.assertEqual(o.render(), expected)

    def test_dns_search(self):
        o = Raspbian({
            "dns_search": [
                "domain.com",
            ],
        })

        expected = '''/etc/network/interfaces
-----------------------


/etc/resolv.conf
----------------
search domain.com
'''
        self.assertEqual(o.render(), expected)

    def test_dns_server_and_dns_search(self):
        o = Raspbian({
            "dns_servers": [
                "10.11.12.13",
                "8.8.8.8"],
            "dns_search": [
                "netjson.org",
                "openwisp.org"
            ],
        })

        expected = '''/etc/network/interfaces
-----------------------


/etc/resolv.conf
----------------
nameserver 10.11.12.13
nameserver 8.8.8.8
search netjson.org
search openwisp.org
'''
        self.assertEqual(o.render(), expected)

    def test_no_dns_server_and_dns_search(self):
        o = Raspbian({
        })

        expected = '''/etc/network/interfaces
-----------------------


/etc/resolv.conf
----------------
'''
        self.assertEqual(o.render(), expected)
