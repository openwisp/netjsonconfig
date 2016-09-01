import unittest

from netjsonconfig import OpenVpn


class TestBackend(unittest.TestCase):
    """
    tests for OpenWisp backend
    """
    maxDiff = None

    def test_server_mode(self):
        c = OpenVpn({
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
        expected = """# config: test-server;

auth SHA1
ca ca.pem
cert cert.pem
cipher BF-CBC
comp-lzo yes
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
script-security-level 0
status /var/log/openvpn.status 10
status-version 1
tls-server
user nobody
verb 3
"""
        self.assertEqual(c.render(), expected)

    def test_client_mode(self):
        c = OpenVpn({
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
        expected = """# config: test-client;

auth SHA256
ca ca.pem
cert cert.pem
cipher AES-128-CBC
comp-lzo adaptive
dev tun0
dev-type tun
down /home/user/down-command.sh
key key.pem
log /var/log/openvpn.log
mode client
mssfix 1450
mtu-disc yes
mtu-test
mute 10
mute-replay-warnings
nobind
ns-cert-type server
persist-key
persist-tun
port 1195
proto tcp-client
remote vpn1.test.com 1194
remote vpn2.test.com 1195
resolv-retry
script-security-level 1
status /var/log/openvpn.status 30
status-version 1
tls-client
tun-ipv6
up /home/user/up-command.sh
up-delay 10
user nobody
verb 1
"""
        self.assertEqual(c.render(), expected)

    def test_no_status_file(self):
        c = OpenVpn({
            "openvpn": [{
                "ca": "ca.pem",
                "cert": "cert.pem",
                "dev": "tap0",
                "dev-type": "tap",
                "dh": "dh.pem",
                "key": "key.pem",
                "mode": "server",
                "name": "test-no-status",
                "proto": "udp",
                "status": "",
                "status-version": 1,
                "tls-server": True
            }]
        })
        expected = """# config: test-no-status;

ca ca.pem
cert cert.pem
dev tap0
dev-type tap
dh dh.pem
key key.pem
mode server
proto udp
tls-server
"""
        self.assertEqual(c.render(), expected)

    def test_additional_properties(self):
        c = OpenVpn({
            "openvpn": [{
                "ca": "ca.pem",
                "cert": "cert.pem",
                "dev": "tap0",
                "dev-type": "tap",
                "dh": "dh.pem",
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
        expected = """# config: test-properties;

ca ca.pem
cert cert.pem
dev tap0
dev-type tap
dh dh.pem
key key.pem
mode server
proto udp
tls-server
z-list test1
z-list test2
z-number 5
z-string string
z-true-val
"""
        self.assertEqual(c.render(), expected)
