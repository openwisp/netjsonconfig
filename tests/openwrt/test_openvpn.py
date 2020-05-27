import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestOpenVpn(_TabsMixin, unittest.TestCase):
    maxDiff = None

    _server_netjson = {
        "openvpn": [
            {
                "auth": "SHA1",
                "ca": "ca.pem",
                "cert": "cert.pem",
                "cipher": "BF-CBC",
                "client_cert_not_required": False,
                "client_to_client": False,
                "comp_lzo": "yes",
                "crl_verify": "crl.pem",
                "dev": "tap0",
                "dev_type": "tap",
                "dh": "dh.pem",
                "duplicate_cn": True,
                "engine": "rsax",
                "disabled": False,
                "fast_io": True,
                "fragment": 0,
                "group": "nogroup",
                "keepalive": "20 60",
                "key": "key.pem",
                "log": "/var/log/openvpn.log",
                "mode": "server",
                "name": "test_server",
                "mssfix": 1450,
                "mtu_disc": "no",
                "mtu_test": False,
                "mute": 0,
                "mute_replay_warnings": True,
                "persist_key": True,
                "persist_tun": True,
                "port": 1194,
                "proto": "udp",
                "script_security": 0,
                "status": "/var/log/openvpn.status 10",
                "status_version": 1,
                "tls_server": True,
                "tun_ipv6": False,
                "up_delay": 0,
                "user": "nobody",
                "username_as_common_name": False,
                "verb": 3,
            }
        ]
    }
    _server_uci = """package openvpn

config openvpn 'test_server'
    option auth 'SHA1'
    option ca 'ca.pem'
    option cert 'cert.pem'
    option cipher 'BF-CBC'
    option client_cert_not_required '0'
    option client_to_client '0'
    option comp_lzo 'yes'
    option crl_verify 'crl.pem'
    option dev 'tap0'
    option dev_type 'tap'
    option dh 'dh.pem'
    option duplicate_cn '1'
    option enabled '1'
    option engine 'rsax'
    option fast_io '1'
    option fragment '0'
    option group 'nogroup'
    option keepalive '20 60'
    option key 'key.pem'
    option log '/var/log/openvpn.log'
    option mode 'server'
    option mssfix '1450'
    option mtu_disc 'no'
    option mtu_test '0'
    option mute '0'
    option mute_replay_warnings '1'
    option persist_key '1'
    option persist_tun '1'
    option port '1194'
    option proto 'udp'
    option script_security '0'
    option status '/var/log/openvpn.status 10'
    option status_version '1'
    option tls_server '1'
    option tun_ipv6 '0'
    option up_delay '0'
    option user 'nobody'
    option username_as_common_name '0'
    option verb '3'
"""

    def test_render_server_mode(self):
        c = OpenWrt(self._server_netjson)
        expected = self._tabs(self._server_uci)
        self.assertEqual(c.render(), expected)

    def test_parse_server_mode(self):
        c = OpenWrt(native=self._server_uci)
        self.assertEqual(c.config, self._server_netjson)

    _client_netjson = {
        "openvpn": [
            {
                "auth": "SHA256",
                "ca": "ca.pem",
                "cert": "cert.pem",
                "cipher": "AES-128-CBC",
                "comp_lzo": "adaptive",
                "dev": "tun0",
                "dev_type": "tun",
                "down": "/home/user/down-command.sh",
                "disabled": False,
                "fast_io": False,
                "fragment": 0,
                "key": "key.pem",
                "log": "/var/log/openvpn.log",
                "mode": "p2p",
                "mssfix": 1450,
                "mtu_disc": "yes",
                "mtu_test": True,
                "mute": 10,
                "mute_replay_warnings": True,
                "name": "test_client",
                "nobind": True,
                "ns_cert_type": "server",
                "persist_key": True,
                "persist_tun": True,
                "port": 1195,
                "proto": "tcp-client",
                "remote": [
                    {"host": "vpn1.test.com", "port": 1194},
                    {"host": "vpn2.test.com", "port": 1195},
                ],
                "resolv_retry": "infinite",
                "script_security": 1,
                "status": "/var/log/openvpn.status 30",
                "status_version": 1,
                "tls_client": True,
                "tun_ipv6": True,
                "up": "/home/user/up-command.sh",
                "up_delay": 10,
                "user": "nobody",
                "verb": 1,
            }
        ]
    }
    _client_uci = """package openvpn

config openvpn 'test_client'
    option auth 'SHA256'
    option ca 'ca.pem'
    option cert 'cert.pem'
    option cipher 'AES-128-CBC'
    option comp_lzo 'adaptive'
    option dev 'tun0'
    option dev_type 'tun'
    option down '/home/user/down-command.sh'
    option enabled '1'
    option fast_io '0'
    option fragment '0'
    option key 'key.pem'
    option log '/var/log/openvpn.log'
    option mode 'p2p'
    option mssfix '1450'
    option mtu_disc 'yes'
    option mtu_test '1'
    option mute '10'
    option mute_replay_warnings '1'
    option nobind '1'
    option ns_cert_type 'server'
    option persist_key '1'
    option persist_tun '1'
    option port '1195'
    option proto 'tcp-client'
    list remote 'vpn1.test.com 1194'
    list remote 'vpn2.test.com 1195'
    option resolv_retry 'infinite'
    option script_security '1'
    option status '/var/log/openvpn.status 30'
    option status_version '1'
    option tls_client '1'
    option tun_ipv6 '1'
    option up '/home/user/up-command.sh'
    option up_delay '10'
    option user 'nobody'
    option verb '1'
"""

    def test_render_client_mode(self):
        c = OpenWrt(self._client_netjson)
        expected = self._tabs(self._client_uci)
        self.assertEqual(c.render(), expected)

    def test_parse_client_mode(self):
        c = OpenWrt(native=self._client_uci)
        self.assertEqual(c.config, self._client_netjson)

    def test_no_status_file(self):
        c = OpenWrt(
            {
                "openvpn": [
                    {
                        "ca": "ca.pem",
                        "cert": "cert.pem",
                        "dev": "tap0",
                        "dev_type": "tap",
                        "dh": "dh.pem",
                        "disabled": False,
                        "key": "key.pem",
                        "mode": "server",
                        "name": "test-no-status",
                        "proto": "udp",
                        "status": "",
                        "status_version": 1,
                        "tls_server": True,
                    }
                ]
            }
        )
        expected = self._tabs(
            """package openvpn

config openvpn 'test_no_status'
    option ca 'ca.pem'
    option cert 'cert.pem'
    option dev 'tap0'
    option dev_type 'tap'
    option dh 'dh.pem'
    option enabled '1'
    option key 'key.pem'
    option mode 'server'
    option proto 'udp'
    option tls_server '1'
"""
        )
        self.assertEqual(c.render(), expected)

    def test_additional_properties(self):
        c = OpenWrt(
            {
                "openvpn": [
                    {
                        "ca": "ca.pem",
                        "cert": "cert.pem",
                        "dev": "tap0",
                        "dev_type": "tap",
                        "dh": "dh.pem",
                        "disabled": False,
                        "key": "key.pem",
                        "mode": "server",
                        "name": "test-properties",
                        "proto": "udp",
                        "tls_server": True,
                        "z_falsy": False,
                        "z_list": ["test1", "test2"],
                        "z_number": 5,
                        "z_string": "string",
                        "z_true_val": True,
                    }
                ]
            }
        )
        expected = self._tabs(
            """package openvpn

config openvpn 'test_properties'
    option ca 'ca.pem'
    option cert 'cert.pem'
    option dev 'tap0'
    option dev_type 'tap'
    option dh 'dh.pem'
    option enabled '1'
    option key 'key.pem'
    option mode 'server'
    option proto 'udp'
    option tls_server '1'
    option z_falsy '0'
    list z_list 'test1'
    list z_list 'test2'
    option z_number '5'
    option z_string 'string'
    option z_true_val '1'
"""
        )
        self.assertEqual(c.render(), expected)

    def test_enabled_missing(self):
        c = OpenWrt(
            {
                "openvpn": [
                    {
                        "ca": "ca.pem",
                        "cert": "cert.pem",
                        "dev": "tap0",
                        "dev_type": "tap",
                        "dh": "dh.pem",
                        "key": "key.pem",
                        "mode": "server",
                        "name": "test-properties",
                        "proto": "udp",
                        "tls_server": True,
                    }
                ]
            }
        )
        expected = self._tabs(
            """package openvpn

config openvpn 'test_properties'
    option ca 'ca.pem'
    option cert 'cert.pem'
    option dev 'tap0'
    option dev_type 'tap'
    option dh 'dh.pem'
    option enabled '1'
    option key 'key.pem'
    option mode 'server'
    option proto 'udp'
    option tls_server '1'
"""
        )
        self.assertEqual(c.render(), expected)

    _server_bridge_netjson = {
        "openvpn": [
            {
                "ca": "ca.pem",
                "cert": "cert.pem",
                "dev": "tap0",
                "dev_type": "tap",
                "dh": "dh.pem",
                "disabled": False,
                "key": "key.pem",
                "mode": "server",
                "name": "bridged",
                "proto": "udp",
                "server_bridge": "10.8.0.4 255.255.255.0 10.8.0.128 10.8.0.254",
                "tls_server": True,
            }
        ]
    }
    _server_bridge_uci = """package openvpn

config openvpn 'bridged'
    option ca 'ca.pem'
    option cert 'cert.pem'
    option dev 'tap0'
    option dev_type 'tap'
    option dh 'dh.pem'
    option enabled '1'
    option key 'key.pem'
    option mode 'server'
    option proto 'udp'
    option server_bridge '10.8.0.4 255.255.255.0 10.8.0.128 10.8.0.254'
    option tls_server '1'
"""

    def test_render_server_bridge(self):
        c = OpenWrt(self._server_bridge_netjson)
        expected = self._tabs(self._server_bridge_uci)
        self.assertEqual(c.render(), expected)

    def test_parse_server_bridge(self):
        c = OpenWrt(native=self._server_bridge_uci)
        self.assertEqual(c.config, self._server_bridge_netjson)

    _server_bridge_proxy_netjson = {
        "openvpn": [
            {
                "ca": "ca.pem",
                "cert": "cert.pem",
                "dev": "tap0",
                "dev_type": "tap",
                "dh": "dh.pem",
                "disabled": False,
                "key": "key.pem",
                "mode": "server",
                "name": "bridged_proxy",
                "proto": "udp",
                "server_bridge": "",
                "tls_server": True,
            }
        ]
    }
    _server_bridge_proxy_uci = """package openvpn

config openvpn 'bridged_proxy'
    option ca 'ca.pem'
    option cert 'cert.pem'
    option dev 'tap0'
    option dev_type 'tap'
    option dh 'dh.pem'
    option enabled '1'
    option key 'key.pem'
    option mode 'server'
    option proto 'udp'
    option server_bridge '1'
    option tls_server '1'
"""

    def test_render_server_bridge_proxy(self):
        c = OpenWrt(self._server_bridge_proxy_netjson)
        expected = self._tabs(self._server_bridge_proxy_uci)
        self.assertEqual(c.render(), expected)

    def test_parse_server_bridge_proxy(self):
        c = OpenWrt(native=self._server_bridge_proxy_uci)
        self.assertEqual(c.config, self._server_bridge_proxy_netjson)

    _server_bridge_routed_netjson = {
        "openvpn": [
            {
                "ca": "ca.pem",
                "cert": "cert.pem",
                "dev": "tap0",
                "dev_type": "tap",
                "dh": "dh.pem",
                "disabled": False,
                "key": "key.pem",
                "mode": "server",
                "name": "routed",
                "proto": "udp",
                "server": "10.8.0.0 255.255.0.0",
                "tls_server": True,
            }
        ]
    }
    _server_bridge_routed_uci = """package openvpn

config openvpn 'routed'
    option ca 'ca.pem'
    option cert 'cert.pem'
    option dev 'tap0'
    option dev_type 'tap'
    option dh 'dh.pem'
    option enabled '1'
    option key 'key.pem'
    option mode 'server'
    option proto 'udp'
    option server '10.8.0.0 255.255.0.0'
    option tls_server '1'
"""

    def test_render_server_bridge_routed(self):
        c = OpenWrt(self._server_bridge_routed_netjson)
        expected = self._tabs(self._server_bridge_routed_uci)
        self.assertEqual(c.render(), expected)

    def test_parse_server_bridge_routed(self):
        c = OpenWrt(native=self._server_bridge_routed_uci)
        self.assertEqual(c.config, self._server_bridge_routed_netjson)

    def test_render_disabled(self):
        c = OpenWrt(
            {
                "openvpn": [
                    {
                        "ca": "ca.pem",
                        "cert": "cert.pem",
                        "dev": "tap0",
                        "dev_type": "tap",
                        "dh": "dh.pem",
                        "disabled": True,
                        "key": "key.pem",
                        "mode": "server",
                        "name": "test_disabled",
                        "proto": "udp",
                        "tls_server": True,
                    }
                ]
            }
        )
        self.assertIn("option enabled '0'", c.render())

    def test_parse_disabled(self):
        c = OpenWrt(
            native="""package openvpn

config openvpn 'test_disabled'
    option ca 'ca.pem'
    option cert 'cert.pem'
    option dev 'tap0'
    option dev_type 'tap'
    option dh 'dh.pem'
    option enabled '0'
    option key 'key.pem'
    option mode 'server'
    option proto 'udp'
    option tls_server '1'"""
        )
        self.assertTrue(c.config['openvpn'][0]['disabled'])

    def test_parse_disabled_default(self):
        c = OpenWrt(
            native="""package openvpn

config openvpn 'test_disabled'
    option ca 'ca.pem'
    option cert 'cert.pem'
    option dev 'tap0'
    option dev_type 'tap'
    option dh 'dh.pem'
    option key 'key.pem'
    option mode 'server'
    option proto 'udp'
    option tls_server '1'"""
        )
        self.assertTrue(c.config['openvpn'][0]['disabled'])
