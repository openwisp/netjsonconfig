import unittest
import subprocess

from .openwrt.utils import _TabsMixin


class TestBin(unittest.TestCase, _TabsMixin):
    """
    tests for netjsonconfig command line tool
    """
    def test_file_not_found(self):
        with self.assertRaises(subprocess.CalledProcessError):
            output = subprocess.check_output("netjsonconfig WRONG", shell=True)

    def test_invalid_netjson(self):
        with self.assertRaises(subprocess.CalledProcessError):
            output = subprocess.check_output('''netjsonconfig '{ "interfaces":["w"] }' -m render''', shell=True)

    def test_invalid_netjson_verbose(self):
        with self.assertRaises(subprocess.CalledProcessError):
            output = subprocess.check_output('''netjsonconfig '{ "interfaces":["w"] }' -m render --verbose''', shell=True)

    def test_invalid_netjson(self):
        output = subprocess.check_output('''netjsonconfig '{}' -m render''', shell=True)
        self.assertEqual(output.decode(), '')
