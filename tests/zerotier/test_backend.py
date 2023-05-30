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
                "id": "79vgjhks7ae448c5",
                "name": "network-network-1",
                "private": True,
            },
            {
                "id": "yt6c2e21c0fhhtyu",
                "name": "zerotier-network-2",
                "private": False,
            },
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
        expected = """# zerotier config: 79vgjhks7ae448c5

n=network-network-1
nwid=79vgjhks7ae448c5
private=True

# zerotier config: yt6c2e21c0fhhtyu

n=zerotier-network-2
nwid=yt6c2e21c0fhhtyu
private=False
"""
        self.assertEqual(c.render(), expected)

    def test_generate(self):
        c = ZeroTier(self._TEST_CONFIG)
        tar = tarfile.open(fileobj=c.generate(), mode="r")
        # tar object should contain both zerotier configuration
        self.assertEqual(len(tar.getmembers()), 2)
        vpn1 = tar.getmember("79vgjhks7ae448c5.conf")
        contents = tar.extractfile(vpn1).read().decode()
        expected = """n=network-network-1
nwid=79vgjhks7ae448c5
private=True
"""
        self.assertEqual(contents, expected)

    def test_auto_client(self):
        expected = {
            "zerotier": [
                {
                    "id": "79vgjhks7ae448c5",
                    "name": "network-network-1",
                }
            ]
        }
        self.assertEqual(
            ZeroTier.auto_client(server=self._TEST_CONFIG["zerotier"][0]), expected
        )
