import json
import os
import subprocess
import tarfile
import unittest

from netjsonconfig.utils import _TabsMixin


class TestBin(unittest.TestCase, _TabsMixin):
    """
    tests for netjsonconfig command line tool
    """
    @classmethod
    def tearDownClass(self):
        os.remove('test.tar.gz')

    def test_file_not_found(self):
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.check_output("netjsonconfig -c WRONG -b openwrt -m generate", shell=True)

    def test_invalid_netjson(self):
        command = '''netjsonconfig -c '{ "interfaces":["w"] }' -b openwrt -m render'''
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.check_output(command, shell=True)

    def test_invalid_netjson_verbose(self):
        command = '''netjsonconfig -c '{ "interfaces":["w"] }' -b openwrt -m render --verbose'''
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.check_output(command, shell=True)

    def test_empty_netjson(self):
        output = subprocess.check_output("netjsonconfig -c '{}' -b openwrt -m render", shell=True)
        self.assertEqual(output.decode(), '')

    def test_templates(self):
        config = json.dumps({
            'general': {'hostname': 'template-test'}
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
        command = """netjsonconfig --config '{0}' -b openwrt -m render --templates '{1}' '{2}'"""
        command = command.format(config, template1, template2)
        output = subprocess.check_output(command, shell=True).decode()
        self.assertIn("hostname 'template-test'", output)
        self.assertIn("interface 'eth0'", output)
        self.assertIn("interface 'wlan0'", output)

    def test_invalid_template(self):
        command = "netjsonconfig -c '{}' -b openwrt -t WRONG -m render"
        try:
            subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as e:
            self.assertIn('"WRONG": file not found', e.output.decode())
        else:
            self.fail('subprocess.CalledProcessError not raised')

    def test_invalid_arguments(self):
        command = "netjsonconfig -c '{}' -b openwrt -m render -a WRONG"
        try:
            subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as e:
            self.assertIn('--arg option expects', e.output.decode())
        else:
            self.fail('subprocess.CalledProcessError not raised')

    def test_arg_exception(self):
        command = "netjsonconfig -c '{}' -b openwrt -m write"
        try:
            subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as e:
            self.assertIn('write()', e.output.decode())
        else:
            self.fail('subprocess.CalledProcessError not raised')

    def test_valid_arg(self):
        config = json.dumps({
            'general': {'hostname': 'template-test'},
            'files': [
                {
                    'path': '/etc/test.txt',
                    'mode': '0644',
                    'contents': 'test_valid_arg'
                }
            ]
        })
        command = "netjsonconfig --config '{0}' -b openwrt -m render -a files=False".format(config)
        output = subprocess.check_output(command, shell=True).decode()
        self.assertNotIn('test.txt', output)
        self.assertNotIn('test_valid_arg', output)

    def test_generate_redirection(self):
        config = """'{"general": { "hostname": "example" }}'"""
        command = """netjsonconfig -c %s -b openwrt -m generate > test.tar.gz""" % config
        subprocess.check_output(command, shell=True)
        tar = tarfile.open('test.tar.gz', 'r')
        self.assertEqual(len(tar.getmembers()), 1)
        tar.close()

    def test_context(self):
        config = json.dumps({'general': {'description': '{{ DESC }}'}})
        command = "export DESC=testdesc; netjsonconfig --config '{0}' -b openwrt -m render".format(config)
        output = subprocess.check_output(command, shell=True).decode()
        self.assertNotIn('{{ DESC }}', output)
        self.assertIn('testdesc', output)
