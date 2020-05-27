import os
import unittest
from copy import deepcopy

from netjsonconfig import OpenVpn
from netjsonconfig.exceptions import ParseError


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

    def test_parse_exception(self):
        try:
            OpenVpn(native=10)
        except Exception as e:
            self.assertIsInstance(e, ParseError)
        else:
            self.fail('Exception not raised')

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
        o.write(name='test', path='/tmp')
        OpenVpn(native=open('/tmp/test.tar.gz'))
        os.remove('/tmp/test.tar.gz')
        self.assertDictEqual(o.config, self._multiple_vpn)
