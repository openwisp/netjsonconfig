import unittest

from netjsonconfig import Raspbian
from netjsonconfig.utils import _TabsMixin


class TestSystemRender(unittest.TestCase, _TabsMixin):

    def test_general(self):
        o = Raspbian({
            "general": {
                "hostname": "test-system",
                "timezone": "Europe/Rome",
                "custom_setting": True,
                "empty_setting1": None,
                "empty_setting2": ""
            }
        })

        expected = '''config: /etc/hostname
test-system

run commands:
$ timedatectl set-timezone Europe/Rome

'''
        self.assertEqual(o.render(), expected)

    def test_ntp(self):
        o = Raspbian({
            "ntp": {
                "enabled": True,
                "enable_server": False,
                "server": [
                    "0.openwrt.pool.ntp.org",
                    "1.openwrt.pool.ntp.org",
                    "2.openwrt.pool.ntp.org",
                    "3.openwrt.pool.ntp.org"
                ]
            }
        })

        expected = '''config: /etc/ntp.conf
server 0.openwrt.pool.ntp.org
server 1.openwrt.pool.ntp.org
server 2.openwrt.pool.ntp.org
server 3.openwrt.pool.ntp.org
'''
        self.assertEqual(o.render(), expected)
