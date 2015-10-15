import json
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

    def test_templates(self):
        config = json.dumps({
            'general': {'hostname': 'template_test'}
        })
        template1 = json.dumps({
            'interfaces': [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "proto": "dhcp",
                            "family": "ipv4"
                        }
                    ]
                }
            ]
        })
        template2 = json.dumps({
            'interfaces': [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "addresses": [
                        {
                            "proto": "dhcp",
                            "family": "ipv6"
                        }
                    ]
                }
            ]
        })
        command = """netjsonconfig '{0}' -m render --templates '{1}' '{2}'"""
        command = command.format(config, template1, template2)
        output = subprocess.check_output(command, shell=True).decode()
        self.assertIn("hostname 'template_test'", output)
        self.assertIn("interface 'eth0'", output)
        self.assertIn("interface 'wlan0'", output)

    def test_invalid_template(self):
        command = "netjsonconfig '{}' -t WRONG -m render"
        try:
            output = subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as e:
            self.assertIn('"WRONG": file not found', e.output.decode())
        else:
            self.fail('subprocess.CalledProcessError not raised')
