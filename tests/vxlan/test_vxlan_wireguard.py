import unittest

from netjsonconfig import VxlanWireguard


class TestBackend(unittest.TestCase):
    def test_auto_client(self):
        with self.subTest('No arguments are provided'):
            expected = {
                'server_ip_address': '',
                'vni': 0,
            }
            self.assertDictEqual(VxlanWireguard.auto_client(), expected)

        with self.subTest('All arguments are provided'):
            expected = {
                'server_ip_address': '10.0.0.1',
                'vni': 1,
            }
            self.assertDictEqual(
                VxlanWireguard.auto_client(
                    vni=1, server_ip_address='10.0.0.1', server={}
                ),
                expected,
            )
