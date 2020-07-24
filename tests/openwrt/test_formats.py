import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.exceptions import ValidationError
from netjsonconfig.utils import _TabsMixin


class TestFormats(unittest.TestCase, _TabsMixin):
    maxDiff = None

    def test_general_hostname(self):
        o = OpenWrt({"general": {"hostname": "invalid hostname"}})
        with self.assertRaises(ValidationError):
            o.validate()
        o.config['general']['hostname'] = 'valid'
        o.validate()

    def test_interface_ipv4(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "addresses": [
                            {
                                "family": "ipv4",
                                "proto": "static",
                                "address": "10.0.0.1",
                                "mask": 28,
                            }
                        ],
                    }
                ]
            }
        )
        o.validate()
        # invalid ipv4
        o.config['interfaces'][0]['addresses'][0]['address'] = '127_0_0_1'
        with self.assertRaises(ValidationError):
            o.validate()

    def test_interface_ipv6(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "addresses": [
                            {
                                "family": "ipv6",
                                "proto": "static",
                                "address": "fe80::ba27:ebff:fe1c:5477",
                                "mask": 64,
                            }
                        ],
                    }
                ]
            }
        )
        o.validate()
        # invalid ipv6
        o.config['interfaces'][0]['addresses'][0][
            'address'
        ] = 'fe80::ba27.ebff_fe1c:5477'
        with self.assertRaises(ValidationError):
            o.validate()

    def test_ntp_servers_hostname(self):
        o = OpenWrt({"ntp": {"enabled": True, "server": ["0.openwrt.pool.ntp.org"]}})
        o.validate()
        # invalid hostname
        o.config['ntp']['server'][0] = 'totally/wrong'
        with self.assertRaises(ValidationError):
            o.validate()

    def test_dns_search_hostname(self):
        o = OpenWrt({"dns_search": ['openwisp.org', 'test.netjson.org']})
        o.validate()
        # invalid hostname
        o.config['dns_search'].append('very/wrong')
        with self.assertRaises(ValidationError):
            o.validate()
