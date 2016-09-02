import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestOpenVpnRenderer(_TabsMixin, unittest.TestCase):
    """
    tests for backends.openwrt.renderers.OpenVpnRenderer
    """
    maxDiff = None

    def test_server_mode(self):
        c = OpenWrt({
            "openvpn": [{
                "auth": "SHA1",
                "auth_user_pass_verify": "",
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
                "down": "",
                "duplicate_cn": True,
                "engine": "rsax",
                "enabled": True,
                "fast_io": True,
                "fragment": 0,
                "group": "nogroup",
                "keepalive": "20 60",
                "key": "key.pem",
                "local": "",
                "log": "/var/log/openvpn.log",
                "mode": "server",
                "name": "test-server",
                "mssfix": 1450,
                "mtu_disc": "no",
                "mtu_test": False,
                "mute": 0,
                "mute_replay_warnings": True,
                "ns_cert_type": "",
                "persist_key": True,
                "persist_tun": True,
                "port": 1194,
                "proto": "udp",
                "script_security_level": 0,
                "secret": "",
                "status": "/var/log/openvpn.status 10",
                "status_version": 1,
                "tls_server": True,
                "tun_ipv6": False,
                "up": "",
                "up_delay": 0,
                "user": "nobody",
                "username_as_common_name": False,
                "verb": 3
            }]
        })
        expected = self._tabs("""package openvpn

config openvpn 'test_server'
    option auth 'SHA1'
    option ca 'ca.pem'
    option cert 'cert.pem'
    option cipher 'BF-CBC'
    option comp_lzo 'yes'
    option crl_verify 'crl.pem'
    option dev 'tap0'
    option dev_type 'tap'
    option dh 'dh.pem'
    option duplicate_cn '1'
    option enabled '1'
    option engine 'rsax'
    option fast_io '1'
    option group 'nogroup'
    option keepalive '20 60'
    option key 'key.pem'
    option log '/var/log/openvpn.log'
    option mode 'server'
    option mssfix '1450'
    option mtu_disc 'no'
    option mute_replay_warnings '1'
    option persist_key '1'
    option persist_tun '1'
    option port '1194'
    option proto 'udp'
    option script_security_level '0'
    option status '/var/log/openvpn.status 10'
    option status_version '1'
    option tls_server '1'
    option user 'nobody'
    option verb '3'
""")
        self.assertEqual(c.render(), expected)

    def test_client_mode(self):
        c = OpenWrt({
            "openvpn": [
                {
                    "auth": "SHA256",
                    "auth_user_pass": "",
                    "ca": "ca.pem",
                    "cert": "cert.pem",
                    "cipher": "AES-128-CBC",
                    "comp_lzo": "adaptive",
                    "dev": "tun0",
                    "dev_type": "tun",
                    "down": "/home/user/down-command.sh",
                    "enabled": True,
                    "engine": "",
                    "fast_io": False,
                    "fragment": 0,
                    "group": "",
                    "keepalive": "",
                    "key": "key.pem",
                    "local": "",
                    "log": "/var/log/openvpn.log",
                    "mode": "client",
                    "mssfix": 1450,
                    "mtu_disc": "yes",
                    "mtu_test": True,
                    "mute": 10,
                    "mute_replay_warnings": True,
                    "name": "test-client",
                    "nobind": True,
                    "ns_cert_type": "server",
                    "persist_key": True,
                    "persist_tun": True,
                    "port": 1195,
                    "proto": "tcp-client",
                    "remote": [
                        {
                            "host": "vpn1.test.com",
                            "port": 1194
                        },
                        {
                            "host": "vpn2.test.com",
                            "port": 1195
                        }
                    ],
                    "resolv_retry": True,
                    "script_security_level": 1,
                    "secret": "",
                    "status": "/var/log/openvpn.status 30",
                    "status_version": 1,
                    "tls_client": True,
                    "tun_ipv6": True,
                    "up": "/home/user/up-command.sh",
                    "up_delay": 10,
                    "user": "nobody",
                    "verb": 1
                }
            ]
        })
        expected = self._tabs("""package openvpn

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
    option key 'key.pem'
    option log '/var/log/openvpn.log'
    option mode 'client'
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
    option resolv_retry '1'
    option script_security_level '1'
    option status '/var/log/openvpn.status 30'
    option status_version '1'
    option tls_client '1'
    option tun_ipv6 '1'
    option up '/home/user/up-command.sh'
    option up_delay '10'
    option user 'nobody'
    option verb '1'
""")
        self.assertEqual(c.render(), expected)

    def test_no_status_file(self):
        c = OpenWrt({
            "openvpn": [{
                "ca": "ca.pem",
                "cert": "cert.pem",
                "dev": "tap0",
                "dev_type": "tap",
                "dh": "dh.pem",
                "enabled": True,
                "key": "key.pem",
                "mode": "server",
                "name": "test-no-status",
                "proto": "udp",
                "status": "",
                "status_version": 1,
                "tls_server": True
            }]
        })
        expected = self._tabs("""package openvpn

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
""")
        self.assertEqual(c.render(), expected)

    def test_additional_properties(self):
        c = OpenWrt({
            "openvpn": [{
                "ca": "ca.pem",
                "cert": "cert.pem",
                "dev": "tap0",
                "dev_type": "tap",
                "dh": "dh.pem",
                "enabled": True,
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
            }]
        })
        expected = self._tabs("""package openvpn

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
    list z_list 'test1'
    list z_list 'test2'
    option z_number '5'
    option z_string 'string'
    option z_true_val '1'
""")
        self.assertEqual(c.render(), expected)
