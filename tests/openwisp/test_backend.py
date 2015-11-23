import os
import unittest
import tarfile

from netjsonconfig import OpenWisp
from netjsonconfig.utils import _TabsMixin


class TestBackend(unittest.TestCase, _TabsMixin):
    """
    tests for OpenWisp backend
    """
    def test_uci(self):
        o = OpenWisp({
            "general": {
                "hostname": "openwisp_test"
            }
        })
        o.generate()
        tar = tarfile.open('openwrt-config.tar.gz', 'r:gz')
        self.assertEqual(len(tar.getmembers()), 1)
        system = tar.getmember('uci/system.conf')
        contents = tar.extractfile(system).read().decode()
        expected = self._tabs("""package system

config system
    option hostname 'openwisp_test'
    option timezone 'UTC'
""")
        self.assertEqual(contents, expected)
        # close and delete tar.gz file
        tar.close()
        os.remove('openwrt-config.tar.gz')
