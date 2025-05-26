import os
import unittest
from copy import deepcopy

from netjsonconfig import OpenVpn
from netjsonconfig.exceptions import ParseError, ValidationError


class TestParser(unittest.TestCase):
    maxDiff = None

    def test_parse_text(self):
        native = """# openvpn config: bridged

ca ca.pem
cert cert.pem
dev tap0
dev-type tap
dh dh.pem
key key.pem
mode server
proto udp
server-bridge 10.8.0.4 255.255.255.0 10.8.0.128 10.8.0.254
tls-server
"""
        o = OpenVpn(native=native)
        expected = {
            "openvpn": [
                {
                    "ca": "ca.pem",
                    "cert": "cert.pem",
                    "dev": "tap0",
                    "dev_type": "tap",
                    "dh": "dh.pem",
                    "key": "key.pem",
                    "mode": "server",
                    "name": "bridged",
                    "proto": "udp",
                    "server_bridge": "10.8.0.4 255.255.255.0 10.8.0.128 10.8.0.254",
                    "tls_server": True,
                }
            ]
        }
        self.assertDictEqual(o.config, expected)

    def test_parse_server(self):
        native = """# openvpn config: test-server

auth SHA1
auth-nocache
ca ca.pem
cert cert.pem
cipher AES-128-GCM
comp-lzo adaptive
crl-verify crl.pem
dev tap0
dev-type tap
dh dh.pem
duplicate-cn
engine rsax
fast-io
group nogroup
keepalive 20 60
key key.pem
log /var/log/openvpn.log
mode server
mssfix 1450
mtu-disc no
mute-replay-warnings
persist-key
persist-tun
port 1194
proto udp
script-security 0
status /var/log/openvpn.status 10
status-version 1
tls-server
user nobody
verb 3
"""
        expected = {
            "openvpn": [
                {
                    "auth": "SHA1",
                    "auth_nocache": True,
                    "ca": "ca.pem",
                    "cert": "cert.pem",
                    "cipher": "AES-128-GCM",
                    "comp_lzo": "adaptive",
                    "crl_verify": "crl.pem",
                    "dev": "tap0",
                    "dev_type": "tap",
                    "dh": "dh.pem",
                    "duplicate_cn": True,
                    "engine": "rsax",
                    "fast_io": True,
                    "group": "nogroup",
                    "keepalive": "20 60",
                    "key": "key.pem",
                    "log": "/var/log/openvpn.log",
                    "mode": "server",
                    "name": "test-server",
                    "mssfix": 1450,
                    "mtu_disc": "no",
                    "mute_replay_warnings": True,
                    "persist_key": True,
                    "persist_tun": True,
                    "port": 1194,
                    "proto": "udp",
                    "script_security": 0,
                    "status": "/var/log/openvpn.status 10",
                    "status_version": 1,
                    "tls_server": True,
                    "user": "nobody",
                    "verb": 3,
                }
            ]
        }
        o = OpenVpn(native=native)
        self.assertDictEqual(o.config, expected)

    def test_parse_data_ciphers(self):
        native = """# openvpn config: test-server

auth SHA1
auth-nocache
ca ca.pem
cert cert.pem
cipher AES-128-GCM
comp-lzo adaptive
crl-verify crl.pem
data-ciphers AES-256-GCM:AES-128-GCM:?CHACHA20-POLY1305
data-ciphers-fallback AES-128-GCM
dev tap0
dev-type tap
dh dh.pem
duplicate-cn
engine rsax
fast-io
group nogroup
keepalive 20 60
key key.pem
log /var/log/openvpn.log
mode server
mssfix 1450
mtu-disc no
mute-replay-warnings
persist-key
persist-tun
port 1194
proto udp
script-security 0
status /var/log/openvpn.status 10
status-version 1
tls-server
user nobody
verb 3
"""
        expected = {
            "openvpn": [
                {
                    "auth": "SHA1",
                    "auth_nocache": True,
                    "ca": "ca.pem",
                    "cert": "cert.pem",
                    "cipher": "AES-128-GCM",
                    "comp_lzo": "adaptive",
                    "crl_verify": "crl.pem",
                    "data_ciphers": [
                        {"cipher": "AES-256-GCM", "optional": False},
                        {"cipher": "AES-128-GCM", "optional": False},
                        {"cipher": "CHACHA20-POLY1305", "optional": True},
                    ],
                    "data_ciphers_fallback": "AES-128-GCM",
                    "dev": "tap0",
                    "dev_type": "tap",
                    "dh": "dh.pem",
                    "duplicate_cn": True,
                    "engine": "rsax",
                    "fast_io": True,
                    "group": "nogroup",
                    "keepalive": "20 60",
                    "key": "key.pem",
                    "log": "/var/log/openvpn.log",
                    "mode": "server",
                    "name": "test-server",
                    "mssfix": 1450,
                    "mtu_disc": "no",
                    "mute_replay_warnings": True,
                    "persist_key": True,
                    "persist_tun": True,
                    "port": 1194,
                    "proto": "udp",
                    "script_security": 0,
                    "status": "/var/log/openvpn.status 10",
                    "status_version": 1,
                    "tls_server": True,
                    "user": "nobody",
                    "verb": 3,
                }
            ]
        }
        o = OpenVpn(native=native)
        self.assertDictEqual(o.config, expected)

    def test_parse_exception(self):
        try:
            OpenVpn(native=10)
        except Exception as e:
            self.assertIsInstance(e, ParseError)
        else:
            self.fail("Exception not raised")

    def test_server_bridge_proxy(self):
        native = """# openvpn config: bridged-proxy

ca ca.pem
cert cert.pem
dev tap0
dev-type tap
dh dh.pem
key key.pem
mode server
proto udp
server-bridge
tls-server
"""
        o = OpenVpn(native=native)
        expected = {
            "openvpn": [
                {
                    "ca": "ca.pem",
                    "cert": "cert.pem",
                    "dev": "tap0",
                    "dev_type": "tap",
                    "dh": "dh.pem",
                    "key": "key.pem",
                    "mode": "server",
                    "name": "bridged-proxy",
                    "proto": "udp",
                    "server_bridge": "",
                    "tls_server": True,
                }
            ]
        }
        self.assertDictEqual(o.config, expected)

    _multiple_vpn = {
        "openvpn": [
            {
                "ca": "ca.pem",
                "cert": "cert.pem",
                "dev": "tap0",
                "dev_type": "tap",
                "dh": "dh.pem",
                "key": "key.pem",
                "mode": "server",
                "name": "test-1",
                "proto": "udp",
                "tls_server": True,
            },
            {
                "ca": "ca.pem",
                "cert": "cert.pem",
                "dev": "tap0",
                "dev_type": "tap",
                "dh": "dh.pem",
                "key": "key.pem",
                "mode": "server",
                "name": "test-2",
                "port": 1195,
                "proto": "udp",
                "tls_server": True,
            },
        ]
    }
    _multiple_vpn_text = """# openvpn config: test-1

ca ca.pem
cert cert.pem
dev tap0
dev-type tap
dh dh.pem
key key.pem
mode server
proto udp
tls-server

# openvpn config: test-2

ca ca.pem
cert cert.pem
dev tap0
dev-type tap
dh dh.pem
key key.pem
mode server
port 1195
proto udp
tls-server
"""

    def test_multiple_vpn(self):
        o = OpenVpn(native=self._multiple_vpn_text)
        self.assertEqual(o.config, self._multiple_vpn)

    def test_parse_tar_bytesio(self):
        conf = deepcopy(self._multiple_vpn)
        conf.update(
            {"files": [{"path": "/etc/dummy", "mode": "0644", "contents": "testing!"}]}
        )
        tar = OpenVpn(conf).generate()
        o = OpenVpn(native=tar)
        self.assertDictEqual(o.config, self._multiple_vpn)

    def test_parse_tar_file(self):
        o = OpenVpn(self._multiple_vpn)
        o.write(name="test", path="/tmp")
        with open("/tmp/test.tar.gz", "rb") as f:
            OpenVpn(native=f)
        os.remove("/tmp/test.tar.gz")
        self.assertDictEqual(o.config, self._multiple_vpn)

    def test_file_path_min_length(self):
        conf = deepcopy(self._multiple_vpn)
        conf.update({"files": [{"path": ".", "mode": "0644", "contents": "testing!"}]})
        with self.assertRaises(ValidationError) as err:
            OpenVpn(conf).generate()
        self.assertEqual("'.' is too short", err.exception.message)
