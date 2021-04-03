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
        self.assertIn("'wireguard' is a required property", str(context_manager.exception))

    def test_confs(self):
        c = Wireguard(
            {
                "wireguard": [
                    {
                        "name": "test1",
                        "private_key": "QFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=",
                        "port": 40842,
                    },
                    {
                        "name": "test2",
                        "private_key": "AFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=",
                        "port": 40843,
                    },
                ]
            }
        )
        expected = """# wireguard config: test1

[Interface]
ListenPort = 40842
PrivateKey = QFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=

# wireguard config: test2

[Interface]
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
                        "peers": [
                            {
                                "public_key": "jqHs76yCH0wThMSqogDshndAiXelfffUJVcFmz352HI=",
                                "allowed_ips": "10.0.0.3/32",
                            },
                            {
                                "public_key": "94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE=",
                                "allowed_ips": "10.0.0.4/32",
                                "preshared_key": "xisFXck9KfEZga4hlkproH6+86S8ki1tmLtMtqVipjg=",
                                "endpoint": "192.168.1.35:4908",
                            },
                        ],
                    }
                ]
            }
        )
        expected = """# wireguard config: test1

[Interface]
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
ListenPort = 40842
PrivateKey = QFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=

[Peer]
AllowedIPs = 10.0.0.3/32
PublicKey = jqHs76yCH0wThMSqogDshndAiXelfffUJVcFmz352HI=
"""
        self.assertEqual(contents, expected)
