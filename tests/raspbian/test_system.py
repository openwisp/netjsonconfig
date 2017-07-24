import unittest

from netjsonconfig import Raspbian
from netjsonconfig.utils import _TabsMixin


class TestSystemRender(unittest.TestCase, _TabsMixin):

    def test_general(self):
        o = Raspbian({
            "general": {
                "hostname": "test-system",
                "timezone": "Europe/Rome"
            }
        })

        expected = '''# config: /etc/hostname

test-system

# script: /scripts/general.sh

/etc/init.d/hostname.sh start
echo "Hostname of device has been modified"
timedatectl set-timezone Europe/Rome
echo "Timezone has changed to Europe/Rome"

'''
        self.assertEqual(o.render(), expected)

    def test_ntp(self):
        o = Raspbian({
            "ntp": {
                "enabled": True,
                "enable_server": False,
                "server": [
                    "0.pool.ntp.org",
                    "1.pool.ntp.org",
                    "2.pool.ntp.org"
                ]
            }
        })

        expected = '''# config: /etc/ntp.conf

server 0.pool.ntp.org
server 1.pool.ntp.org
server 2.pool.ntp.org
'''
        self.assertEqual(o.render(), expected)
