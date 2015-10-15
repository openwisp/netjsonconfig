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
        command = '''netjsonconfig '{ "interfaces":["w"] }' -m render'''
        with self.assertRaises(subprocess.CalledProcessError):
            output = subprocess.check_output(command, shell=True)

    def test_invalid_netjson_verbose(self):
        command = '''netjsonconfig '{ "interfaces":["w"] }' -m render --verbose'''
        with self.assertRaises(subprocess.CalledProcessError):
            output = subprocess.check_output(command, shell=True)

    def test_empty_netjson(self):
        output = subprocess.check_output("netjsonconfig '{}' -m render", shell=True)
        self.assertEqual(output.decode(), '')
