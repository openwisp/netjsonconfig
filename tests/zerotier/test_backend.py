import tarfile
import unittest

from netjsonconfig import ZeroTier
from netjsonconfig.exceptions import ValidationError


class TestBackend(unittest.TestCase):
    """
    Tests for ZeroTier backend
    """

    maxDiff = None
    _TEST_CONFIG = {
        "zerotier": [
            {
                "id": "9536600adf0af076",
                "nwid": "9536600adf0af076",
                "objtype": "network",
                "revision": 1,
                "creationTime": 1632012345,
                "name": "zerotier-openwisp-network",
                "private": True,
                "enableBroadcast": True,
                "v4AssignMode": {"zt": True},
                "v6AssignMode": {"6plane": False, "rfc4193": True, "zt": True},
                "mtu": 2700,
                "multicastLimit": 16,
                "routes": [{"target": "10.0.0.0/24", "via": "10.0.0.1"}],
                "ipAssignmentPools": [
                    {"ipRangeStart": "10.0.0.10", "ipRangeEnd": "10.0.0.100"}
                ],
                "dns": {"domain": "zerotier.openwisp.io", "servers": ["10.147.20.3"]},
                "rules": [
                    {
                        "etherType": 2048,
                        "not": True,
                        "or": False,
                        "type": "MATCH_ETHERTYPE",
                    },
                    {"type": "ACTION_DROP"},
                ],
                "capabilities": [
                    {
                        "default": True,
                        "id": 1,
                        "rules": [
                            {
                                "etherType": 2048,
                                "not": True,
                                "or": False,
                                "type": "MATCH_ETHERTYPE",
                            }
                        ],
                    }
                ],
                "tags": [{"default": 1, "id": 1}],
                "remoteTraceTarget": "7f5d90eb87",
                "remoteTraceLevel": 1,
            }
        ]
    }

    def test_test_schema(self):
        with self.assertRaises(ValidationError) as context_manager:
            ZeroTier({}).validate()
        self.assertIn(
            "'zerotier' is a required property", str(context_manager.exception)
        )

    def test_confs(self):
        c = ZeroTier(self._TEST_CONFIG)
        expected = """# zerotier config: 9536600adf0af076

CAP={'default': True, 'id': 1, 'rules': [{'etherType': 2048, 'not': True, 'or': False, 'type': 'MATCH_ETHERTYPE'}]}
DNS=domain
DNS=servers
I={'ipRangeStart': '10.0.0.10', 'ipRangeEnd': '10.0.0.100'}
R={'etherType': 2048, 'not': True, 'or': False, 'type': 'MATCH_ETHERTYPE'}
R={'type': 'ACTION_DROP'}
RT={'target': '10.0.0.0/24', 'via': '10.0.0.1'}
TAG={'default': 1, 'id': 1}
eb=True
ml=16
mtu=2700
n=zerotier-openwisp-network
nwid=9536600adf0af076
p=True
r=1
t=network
tl=1
ts=1632012345
tt=7f5d90eb87
v4s=zt
v6s=6plane
v6s=rfc4193
v6s=zt
"""  # noqa
        self.assertEqual(c.render(), expected)

    def test_generate(self):
        c = ZeroTier(self._TEST_CONFIG)
        expected = """CAP={'default': True, 'id': 1, 'rules': [{'etherType': 2048, 'not': True, 'or': False, 'type': 'MATCH_ETHERTYPE'}]}
DNS=domain
DNS=servers
I={'ipRangeStart': '10.0.0.10', 'ipRangeEnd': '10.0.0.100'}
R={'etherType': 2048, 'not': True, 'or': False, 'type': 'MATCH_ETHERTYPE'}
R={'type': 'ACTION_DROP'}
RT={'target': '10.0.0.0/24', 'via': '10.0.0.1'}
TAG={'default': 1, 'id': 1}
eb=True
ml=16
mtu=2700
n=zerotier-openwisp-network
nwid=9536600adf0af076
p=True
r=1
t=network
tl=1
ts=1632012345
tt=7f5d90eb87
v4s=zt
v6s=6plane
v6s=rfc4193
v6s=zt
"""  # noqa
        tar = tarfile.open(fileobj=c.generate(), mode="r")
        self.assertEqual(len(tar.getmembers()), 1)
        vpn = tar.getmember("9536600adf0af076.conf")
        contents = tar.extractfile(vpn).read().decode()
        self.assertEqual(contents, expected)

    def test_auto_client(self):
        expected = {
            "zerotier": [
                {
                    "id": "9536600adf0af076",
                    "name": "zerotier-openwisp-network",
                }
            ]
        }
        self.assertEqual(
            ZeroTier.auto_client(server=self._TEST_CONFIG["zerotier"][0]), expected
        )
