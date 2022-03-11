import tarfile
import unittest

from netjsonconfig import Wireguard
from netjsonconfig.exceptions import ValidationError


class TestBackend(unittest.TestCase):
    """
    tests for Wireguard backend
    """

    maxDiff = None

    def test_test_schema(self):
        with self.assertRaises(ValidationError) as context_manager:
            Wireguard({}).validate()
        self.assertIn(
            "'wireguard' is a required property", str(context_manager.exception)
        )

    def test_confs(self):
        c = Wireguard(
            {
                "wireguard": [
                    {
                        "name": "test1",
                        "private_key": "QFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=",
                        "port": 40842,
                        "address": "10.0.0.1/24",
                    },
                    {
                        "name": "test2",
                        "private_key": "AFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=",
                        "port": 40843,
                        "address": "10.0.1.1/24",
                    },
                ]
            }
        )
        expected = """# wireguard config: test1

[Interface]
Address = 10.0.0.1/24
ListenPort = 40842
PrivateKey = QFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=

# wireguard config: test2

[Interface]
Address = 10.0.1.1/24
ListenPort = 40843
PrivateKey = AFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=
"""
        self.assertEqual(c.render(), expected)

    def test_peers(self):
        c = Wireguard(
            {
                "wireguard": [
                    {
                        "name": "test1",
                        "private_key": "QFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=",
                        "port": 40842,
                        "address": "10.0.0.1/24",
                        "peers": [
                            {
                                "public_key": "jqHs76yCH0wThMSqogDshndAiXelfffUJVcFmz352HI=",
                                "allowed_ips": "10.0.0.3/32",
                            },
                            {
                                "public_key": "94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE=",
                                "allowed_ips": "10.0.0.4/32",
                                "preshared_key": "xisFXck9KfEZga4hlkproH6+86S8ki1tmLtMtqVipjg=",
                                "endpoint_host": "192.168.1.35",
                                "endpoint_port": 4908,
                            },
                        ],
                    }
                ]
            }
        )
        expected = """# wireguard config: test1

[Interface]
Address = 10.0.0.1/24
ListenPort = 40842
PrivateKey = QFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=

[Peer]
AllowedIPs = 10.0.0.3/32
PublicKey = jqHs76yCH0wThMSqogDshndAiXelfffUJVcFmz352HI=

[Peer]
AllowedIPs = 10.0.0.4/32
Endpoint = 192.168.1.35:4908
PreSharedKey = xisFXck9KfEZga4hlkproH6+86S8ki1tmLtMtqVipjg=
PublicKey = 94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE=
"""
        self.assertEqual(c.render(), expected)

    def test_generate(self):
        c = Wireguard(
            {
                "wireguard": [
                    {
                        "name": "test1",
                        "private_key": "QFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=",
                        "port": 40842,
                        "address": "10.0.0.1/24",
                        "peers": [
                            {
                                "public_key": "jqHs76yCH0wThMSqogDshndAiXelfffUJVcFmz352HI=",
                                "allowed_ips": "10.0.0.3/32",
                            }
                        ],
                    }
                ]
            }
        )
        tar = tarfile.open(fileobj=c.generate(), mode='r')
        self.assertEqual(len(tar.getmembers()), 1)
        # network
        vpn1 = tar.getmember('test1.conf')
        contents = tar.extractfile(vpn1).read().decode()
        expected = """[Interface]
Address = 10.0.0.1/24
ListenPort = 40842
PrivateKey = QFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=

[Peer]
AllowedIPs = 10.0.0.3/32
PublicKey = jqHs76yCH0wThMSqogDshndAiXelfffUJVcFmz352HI=
"""
        self.assertEqual(contents, expected)

    def test_auto_client(self):
        with self.subTest('No arguments are provided'):
            expected = {
                'interface_name': '',
                'client': {
                    'port': 51820,
                    'private_key': '{{private_key}}',
                    'ip_address': None,
                },
                'server': {
                    'public_key': '',
                    'endpoint_host': '',
                    'endpoint_port': 51820,
                    'allowed_ips': [''],
                },
            }
            self.assertDictEqual(Wireguard.auto_client(), expected)
        with self.subTest('Required arguments are provided'):
            expected = {
                'interface_name': 'wg',
                'client': {
                    'port': 51820,
                    'private_key': '{{private_key}}',
                    'ip_address': '10.0.0.2',
                },
                'server': {
                    'public_key': 'server_public_key',
                    'endpoint_host': '0.0.0.0',
                    'endpoint_port': 51820,
                    'allowed_ips': ['10.0.0.1/24'],
                },
            }
            self.assertDictEqual(
                Wireguard.auto_client(
                    host='0.0.0.0',
                    public_key='server_public_key',
                    server={'name': 'wg', 'port': 51820},
                    server_ip_network='10.0.0.1/24',
                    ip_address='10.0.0.2',
                ),
                expected,
            )
