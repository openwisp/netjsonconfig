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

