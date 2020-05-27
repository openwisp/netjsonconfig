import os
import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.exceptions import ParseError
from netjsonconfig.utils import _TabsMixin


class TestParser(unittest.TestCase, _TabsMixin):
    maxDiff = None

    _system_uci = """package system

config system system
    option custom_setting 1
    option hostname 'test-system'
    option timezone 'CET-1CEST,M3.5.0,M10.5.0/3'
    option zonename 'Europe/Rome'
    option empty
"""
    _system_intermediate = {
        "system": [
            {
                ".type": "system",
                ".name": "system",
                "hostname": "test-system",
                "timezone": "CET-1CEST,M3.5.0,M10.5.0/3",
                "zonename": "Europe/Rome",
                "custom_setting": "1",
                "empty": "",
            }
        ]
    }

    def test_parse_text(self):
        native = self._tabs(self._system_uci)
        o = OpenWrt(native=native)
        self.assertDictEqual(o.intermediate_data, self._system_intermediate)

    def test_parse_no_quotes(self):
        native = self._tabs(self._system_uci.replace('\'', ''))
        o = OpenWrt(native=native)
        self.assertDictEqual(o.intermediate_data, self._system_intermediate)

    def test_parse_double_quotes(self):
        native = self._tabs(self._system_uci.replace('\'', '"'))
        o = OpenWrt(native=native)
        self.assertDictEqual(o.intermediate_data, self._system_intermediate)

    def test_parse_text_comment(self):
        native = self._tabs(
            """package system

config system 'system'
    # this is a comment
    option hostname 'test-system'
"""
        )
        o = OpenWrt(native=native)
        expected = {
            "system": [
                {".type": "system", ".name": "system", "hostname": "test-system"}
            ]
        }
        self.assertDictEqual(o.intermediate_data, expected)

    def test_parse_text_multiple_packages(self):
        native = self._tabs(
            """package system

config system 'system'
    option hostname 'test-system'

package network

config interface 'lan'
    option ifname 'eth0'
    option proto 'none'
"""
        )
        o = OpenWrt(native=native)
        expected = {
            "system": [
                {".type": "system", ".name": "system", "hostname": "test-system"}
            ],
            "network": [
                {
                    ".type": "interface",
                    ".name": "lan",
                    "ifname": "eth0",
                    "proto": "none",
                }
            ],
        }
        self.assertDictEqual(o.intermediate_data, expected)

    def test_parse_anonymous_block(self):
        native = self._tabs(
            """package network

config interface
    option ifname 'eth0'
    option proto 'none'

config interface 'vpn'
    option ifname 'vpn'
    option proto 'none'

config interface
    option ifname 'eth1'
    option proto 'none'
"""
        )
        o = OpenWrt(native=native)
        expected = {
            "network": [
                {
                    ".type": "interface",
                    ".name": "interface_1",
                    "ifname": "eth0",
                    "proto": "none",
                },
                {
                    ".type": "interface",
                    ".name": "vpn",
                    "ifname": "vpn",
                    "proto": "none",
                },
                {
                    ".type": "interface",
                    ".name": "interface_3",
                    "ifname": "eth1",
                    "proto": "none",
                },
            ]
        }
        self.assertDictEqual(o.intermediate_data, expected)

    def test_parsed_renders_equally(self):
        native = self._tabs(
            """package system

config system 'system'
    option custom_setting '1'
    option hostname 'test-system'
    option timezone 'CET-1CEST,M3.5.0,M10.5.0/3'
    option zonename 'Europe/Rome'
"""
        )
        o = OpenWrt(native=native)
        self.assertEqual(o.render(), native)

    def test_parse_list(self):
        native = self._tabs(
            """package network
config interface 'lan'
    option ifname 'eth0'
    option proto 'static'
    list ipaddr '192.168.1.1/24'
    list ipaddr '10.0.0.1/24'
"""
        )
        o = OpenWrt(native=native)
        expected = {
            "network": [
                {
                    ".type": "interface",
                    ".name": "lan",
                    "ifname": "eth0",
                    "proto": "static",
                    "ipaddr": ["192.168.1.1/24", "10.0.0.1/24"],
                }
            ]
        }
        self.assertDictEqual(o.intermediate_data, expected)

    def test_parse_inline_list(self):
        native = self._tabs(
            """package network
config interface 'lan'
    option ifname 'eth0 eth1'
    option proto 'none'
    option type 'bridge'
"""
        )
        o = OpenWrt(native=native)
        expected = {
            "network": [
                {
                    ".type": "interface",
                    ".name": "lan",
                    "ifname": "eth0 eth1",
                    "proto": "none",
                    "type": "bridge",
                }
            ]
        }
        self.assertDictEqual(o.intermediate_data, expected)

    def test_parse_tar_bytesio(self):
        conf = {
            "general": {"hostname": "parse-tar-bytesio"},
            "files": [
                {"path": "/etc/dummy.conf", "mode": "0644", "contents": "testing!"}
            ],
        }
        tar = OpenWrt(conf).generate()
        o = OpenWrt(native=tar)
        expected = {
            "system": [
                {".type": "system", ".name": "system", "hostname": "parse-tar-bytesio"}
            ]
        }
        self.assertDictEqual(o.intermediate_data, expected)

    def test_parse_tar_file(self):
        o = OpenWrt({"general": {"hostname": "parse-tar-file"}})
        o.write(name='test', path='/tmp')
        o = OpenWrt(native=open('/tmp/test.tar.gz'))
        expected = {
            "system": [
                {".type": "system", ".name": "system", "hostname": "parse-tar-file"}
            ]
        }
        os.remove('/tmp/test.tar.gz')
        self.assertDictEqual(o.intermediate_data, expected)

    def test_parse_exception(self):
        try:
            OpenWrt(native=10)
        except Exception as e:
            self.assertIsInstance(e, ParseError)
        else:
            self.fail('Exception not raised')

    # ensure parser doesn't break when
    # dealing with dirty configurations

    def test_parse_empty(self):
        OpenWrt(native='')

    def test_parse_empty_package(self):
        native = self._tabs(
            """package network

"""
        )
        o = OpenWrt(native=native)
        self.assertDictEqual(o.intermediate_data, {"network": []})

    def test_parse_empty_config(self):
        native = self._tabs(
            """package network
config interface "lan"
"""
        )
        expected = {"network": [{".type": "interface", ".name": "lan"}]}
        o = OpenWrt(native=native)
        self.assertDictEqual(o.intermediate_data, expected)

    def test_parse_empty_option(self):
        native = self._tabs(
            """package network
config interface "lan"
    option 'ifname' eth0
    option proto 'none'
    option forgotten
    VERYWRONG hey i'm wrong
"""
        )
        o = OpenWrt(native=native)
        expected = {
            "network": [
                {
                    ".type": "interface",
                    ".name": "lan",
                    "ifname": "eth0",
                    "proto": "none",
                    "forgotten": "",
                }
            ]
        }
        self.assertDictEqual(o.intermediate_data, expected)
