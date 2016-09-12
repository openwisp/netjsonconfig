import json
import os
import tarfile
import unittest
from hashlib import md5
from time import sleep

from netjsonconfig import OpenWrt
from netjsonconfig.exceptions import ValidationError
from netjsonconfig.utils import _TabsMixin


class TestBackend(unittest.TestCase, _TabsMixin):
    """
    tests for backends.openwrt.OpenWrt
    """
    def test_config_copy(self):
        config = {'interfaces': []}
        o = OpenWrt(config)
        o.validate()
        self.assertDictEqual(config, {'interfaces': []})

    def test_json_method(self):
        config = {
            "type": "DeviceConfiguration",
            "interfaces": [
                {
                    "name": "lo",
                    "type": "loopback",
                    "addresses": [
                        {
                            "address": "127.0.0.1",
                            "mask": 8,
                            "proto": "static",
                            "family": "ipv4"
                        }
                    ]
                }
            ]
        }
        o = OpenWrt(config)
        self.assertEqual(json.loads(o.json()), config)

    def test_string_argument(self):
        OpenWrt('{}')

    def test_validate(self):
        o = OpenWrt({'interfaces': 'WRONG'})
        with self.assertRaises(ValidationError):
            o.validate()

        o = OpenWrt({'interfaces': []})
        o.validate()

        o.config['interfaces'] = 'CHANGED'
        try:
            o.validate()
        except ValidationError as e:
            self.assertEqual(e.details.instance, 'CHANGED')
        else:
            self.fail('ValidationError not raised')

    def test_find_bridge_skip_error(self):
        o = OpenWrt({'interfaces': ['WRONG']})
        with self.assertRaises(ValidationError):
            o.validate()

    def test_type_error(self):
        with self.assertRaises(TypeError):
            OpenWrt([])
        with self.assertRaises(TypeError):
            OpenWrt('NOTJSON[]\{\}')

    def test_system_invalid_timezone(self):
        o = OpenWrt({
            "general": {
                "hostname": "test_system",
                "timezone": "WRONG",
            }
        })
        with self.assertRaises(ValidationError):
            o.validate()

    def test_schema_radio_wrong_driver(self):
        o = OpenWrt({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "iamwrong",
                    "protocol": "802.11ac",
                    "channel": 132,
                    "channel_width": 80,
                    "tx_power": 8
                }
            ]
        })
        with self.assertRaises(ValidationError):
            o.validate()

    def test_schema_radio_wrong_protocol(self):
        o = OpenWrt({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11ad",  # ad is not supported by OpenWRT yet
                    "channel": 132,
                    "channel_width": 80,
                    "tx_power": 8
                }
            ]
        })
        with self.assertRaises(ValidationError):
            o.validate()

    def test_generate(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "addresses": [
                        {
                            "address": "192.168.1.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        }
                    ],
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "MyWifiAP",
                        "hidden": True
                    }
                }
            ],
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                }
            ]
        })
        tar = tarfile.open(fileobj=o.generate(), mode='r')
        self.assertEqual(len(tar.getmembers()), 2)
        # network
        network = tar.getmember('etc/config/network')
        contents = tar.extractfile(network).read().decode()
        expected = self._tabs("""config interface 'wlan0'
    option ifname 'wlan0'
    option ipaddr '192.168.1.1'
    option netmask '255.255.255.0'
    option proto 'static'

""")
        self.assertEqual(contents, expected)
        # wireless
        wireless = tar.getmember('etc/config/wireless')
        contents = tar.extractfile(wireless).read().decode()
        expected = self._tabs("""config wifi-device 'radio0'
    option channel '3'
    option htmode 'HT20'
    option hwmode '11g'
    option phy 'phy0'
    option txpower '3'
    option type 'mac80211'

config wifi-iface 'wifi_wlan0'
    option device 'radio0'
    option hidden '1'
    option ifname 'wlan0'
    option mode 'ap'
    option network 'wlan0'
    option ssid 'MyWifiAP'
""")
        self.assertEqual(contents, expected)
        tar.close()

    def test_write(self):
        o = OpenWrt({
            "general": {
                "hostname": "test"
            }
        })
        o.write(name='test', path='/tmp')
        tar = tarfile.open('/tmp/test.tar.gz', mode='r')
        self.assertEqual(len(tar.getmembers()), 1)
        tar.close()
        os.remove('/tmp/test.tar.gz')

    def test_templates_type_error(self):
        config = {
            "general": {
                "hostname": "test_templates",
            }
        }
        with self.assertRaises(TypeError):
            OpenWrt(config, templates={})

    def test_templates_config_error(self):
        config = {
            "general": {
                "hostname": "test_templates",
            }
        }
        with self.assertRaises(TypeError):
            OpenWrt(config, templates=['O{]O'])

    def test_templates(self):
        loopback_template = {
            "interfaces": [
                {
                    "name": "lo",
                    "type": "loopback",
                    "addresses": [
                        {
                            "address": "127.0.0.1",
                            "mask": 8,
                            "proto": "static",
                            "family": "ipv4"
                        }
                    ]
                }
            ]
        }
        radio_template = {
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "addresses": [
                        {
                            "address": "192.168.1.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        }
                    ],
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "MyWifiAP",
                        "hidden": True
                    }
                }
            ],
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                }
            ]
        }
        config = {
            "general": {
                "hostname": "test_templates",
            }
        }
        o = OpenWrt(config, templates=[loopback_template, radio_template])
        self.assertEqual(o.config['general']['hostname'], 'test_templates')
        self.assertIn('radios', o.config)
        self.assertEqual(len(o.config['radios']), 1)
        self.assertEqual(o.config['radios'][0]['name'], 'radio0')
        self.assertIn('interfaces', o.config)
        self.assertEqual(len(o.config['interfaces']), 2)
        self.assertEqual(o.config['interfaces'][0]['name'], 'lo')
        self.assertEqual(o.config['interfaces'][1]['name'], 'wlan0')

    def test_file_inclusion(self):
        o = OpenWrt({
            "files": [
                {
                    "path": "/etc/crontabs/root",
                    "mode": "0644",
                    "contents": '* * * * * echo "test" > /etc/testfile\n'
                                '* * * * * echo "test2" > /etc/testfile2'
                },
                {
                    "path": "/etc/dummy.conf",
                    "mode": "0644",
                    "contents": "testing!"
                }
            ]
        })
        output = o.render()
        self.assertNotIn('package files', output)
        self.assertIn('* * * * * echo', output)
        # ensure the additional files are there present in the tar.gz archive
        tar = tarfile.open(fileobj=o.generate(), mode='r')
        self.assertEqual(len(tar.getmembers()), 2)
        # first file
        crontab = tar.getmember('etc/crontabs/root')
        contents = tar.extractfile(crontab).read().decode()
        self.assertEqual(contents, o.config['files'][0]['contents'])
        self.assertEqual(crontab.mtime, 0)
        self.assertEqual(crontab.mode, 420)
        # second file
        dummy = tar.getmember('etc/dummy.conf')
        contents = tar.extractfile(dummy).read().decode()
        self.assertEqual(contents, o.config['files'][1]['contents'])
        self.assertEqual(dummy.mode, 420)
        tar.close()

    def test_file_permissions(self):
        o = OpenWrt({
            "files": [
                {
                    "path": "/tmp/hello.sh",
                    "mode": "0755",
                    "contents": "echo 'hello world'",
                }
            ]
        })
        tar = tarfile.open(fileobj=o.generate(), mode='r')
        script = tar.getmember('tmp/hello.sh')
        # check permissions
        self.assertEqual(script.mode, 493)
        tar.close()

    def test_file_schema(self):
        c = {
            "files": [
                {
                    "path": "/tmp/hello.sh",
                    "mode": "0644",
                    "contents": "echo 'hello world'"
                }
            ]
        }
        # valid
        c['files'][0]['mode'] = '3555'
        o = OpenWrt(c)
        o.validate()
        # valid
        c['files'][0]['mode'] = '755'
        o = OpenWrt(c)
        o.validate()
        # too long
        c['files'][0]['mode'] = '00777'
        o = OpenWrt(c)
        with self.assertRaises(ValidationError):
            o.validate()
        # too short
        c['files'][0]['mode'] = '75'
        o = OpenWrt(c)
        with self.assertRaises(ValidationError):
            o.validate()
        # invalid
        c['files'][0]['mode'] = '0855'
        o = OpenWrt(c)
        with self.assertRaises(ValidationError):
            o.validate()

    def test_checksum(self):
        """ ensures checksum of same config doesn't change """
        o = OpenWrt({"general": {"hostname": "test"}})
        # md5 is good enough and won't slow down test execution too much
        checksum1 = md5(o.generate().getvalue()).hexdigest()
        sleep(1)
        checksum2 = md5(o.generate().getvalue()).hexdigest()
        self.assertEqual(checksum1, checksum2)
