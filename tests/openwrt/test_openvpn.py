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
                "auth-user-pass-verify": "",
                "ca": "ca.pem",
                "cert": "cert.pem",
                "cipher": "BF-CBC",
                "client-cert-not-required": False,
                "client-to-client": False,
                "comp-lzo": "yes",
                "crl-verify": "crl.pem",
                "dev": "tap0",
                "dev-type": "tap",
                "dh": "dh.pem",
                "down": "",
                "duplicate-cn": True,
                "engine": "rsax",
                "enabled": True,
                "fast-io": True,
                "fragment": 0,
                "group": "nogroup",
                "keepalive": "20 60",
                "key": "key.pem",
                "local": "",
                "log": "/var/log/openvpn.log",
                "mode": "server",
                "name": "test-server",
                "mssfix": 1450,
                "mtu-disc": "no",
                "mtu-test": False,
                "mute": 0,
                "mute-replay-warnings": True,
                "ns-cert-type": "",
                "persist-key": True,
                "persist-tun": True,
                "port": 1194,
                "proto": "udp",
                "script-security-level": 0,
                "secret": "",
                "status": "/var/log/openvpn.status 10",
                "status-version": 1,
                "tls-server": True,
                "tun-ipv6": False,
                "up": "",
                "up-delay": 0,
                "user": "nobody",
                "username-as-common-name": False,
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
                    "auth-user-pass": "",
                    "ca": "ca.pem",
                    "cert": "cert.pem",
                    "cipher": "AES-128-CBC",
                    "comp-lzo": "adaptive",
                    "dev": "tun0",
                    "dev-type": "tun",
                    "down": "/home/user/down-command.sh",
                    "enabled": True,
                    "engine": "",
                    "fast-io": False,
                    "fragment": 0,
                    "group": "",
                    "keepalive": "",
                    "key": "key.pem",
                    "local": "",
                    "log": "/var/log/openvpn.log",
                    "mode": "client",
                    "mssfix": 1450,
                    "mtu-disc": "yes",
                    "mtu-test": True,
                    "mute": 10,
                    "mute-replay-warnings": True,
                    "name": "test-client",
                    "nobind": True,
                    "ns-cert-type": "server",
                    "persist-key": True,
                    "persist-tun": True,
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
                    "resolv-retry": True,
                    "script-security-level": 1,
                    "secret": "",
                    "status": "/var/log/openvpn.status 30",
                    "status-version": 1,
                    "tls-client": True,
                    "tun-ipv6": True,
                    "up": "/home/user/up-command.sh",
                    "up-delay": 10,
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
                "dev-type": "tap",
                "dh": "dh.pem",
                "enabled": True,
                "key": "key.pem",
                "mode": "server",
                "name": "test-no-status",
                "proto": "udp",
                "status": "",
                "status-version": 1,
                "tls-server": True
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
                "dev-type": "tap",
                "dh": "dh.pem",
                "enabled": True,
                "key": "key.pem",
                "mode": "server",
                "name": "test-properties",
                "proto": "udp",
                "tls-server": True,
                "z-falsy": False,
                "z-list": ["test1", "test2"],
                "z-number": 5,
                "z-string": "string",
                "z-true-val": True,
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
