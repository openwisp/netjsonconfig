import os
import tarfile
import unittest

from netjsonconfig import Raspbian
from netjsonconfig.utils import _TabsMixin


class TestBackend(unittest.TestCase, _TabsMixin):

    def test_generate(self):
        o = Raspbian({
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "addresses": [
                            {
                                "address": "192.168.1.1",
                                "mask": 24,
                                "proto": "static",
                                "family": "ipv4"
                            }
                        ]
                    }
                ],
                "dns_servers": [
                    "10.11.12.13",
                    "8.8.8.8"
                ],
                "dns_search": [
                    "netjson.org",
                    "openwisp.org"
                ]
        })
        tar = tarfile.open(fileobj=o.generate(), mode='r')
        self.assertEqual(len(tar.getmembers()), 2)

        interface = tar.getmember('/etc/network/interfaces')
        contents = tar.extractfile(interface).read().decode()
        expected = self._tabs('''auto eth0
iface eth0 inet static
address 192.168.1.1
netmask 255.255.255.0

''')
        self.assertEqual(contents, expected)

        resolv = tar.getmember('/etc/resolv.conf')
        contents = tar.extractfile(resolv).read().decode()
        expected = self._tabs('''nameserver 10.11.12.13
nameserver 8.8.8.8
search netjson.org
search openwisp.org
''')
        self.assertEqual(contents, expected)

    def test_write(self):
        o = Raspbian({
            "general": {
                "hostname": "test"
            }
        })
        o.write(name='test', path='/tmp')
        tar = tarfile.open('/tmp/test.tar.gz', mode='r')
        self.assertEqual(len(tar.getmembers()), 1)
        tar.close()
        os.remove('/tmp/test.tar.gz')
