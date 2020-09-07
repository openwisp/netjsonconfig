import copy
import tarfile
import unittest

from netjsonconfig import OpenVpn
from netjsonconfig.exceptions import ValidationError


class TestBackend(unittest.TestCase):
    """
    tests for OpenVpn backend
    """

    maxDiff = None

    def test_server_mode(self):
        c = OpenVpn(
            {
                "openvpn": [
                    {
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
                        "script_security": 0,
                        "secret": "",
                        "status": "/var/log/openvpn.status 10",
                        "status_version": 1,
                        "tls_server": True,
                        "tun_ipv6": False,
                        "up": "",
                        "up_delay": 0,
                        "user": "nobody",
                        "username_as_common_name": False,
                        "verb": 3,
                    }
                ]
            }
        )
        expected = """# openvpn config: test-server

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
script-security 0
status /var/log/openvpn.status 10
status-version 1
tls-server
user nobody
verb 3
"""
        self.assertEqual(c.render(), expected)

    def test_client_mode(self):
        c = OpenVpn(
            {
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
                        "engine": "",
                        "fast_io": False,
                        "fragment": 0,
                        "group": "",
                        "keepalive": "",
                        "key": "key.pem",
                        "local": "",
                        "log": "/var/log/openvpn.log",
                        "mode": "p2p",
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
                        "pull": True,
                        "remote": [
                            {"host": "vpn1.test.com", "port": 1194},
                            {"host": "176.9.43.231", "port": 1195},
                        ],
                        "resolv_retry": "infinite",
                        "script_security": 1,
                        "secret": "",
                        "status": "/var/log/openvpn.status 30",
                        "status_version": 1,
                        "tls_client": True,
                        "topology": "p2p",
                        "tun_ipv6": True,
                        "up": "/home/user/up-command.sh",
                        "up_delay": 10,
                        "user": "nobody",
                        "verb": 1,
                    }
                ]
            }
        )
        expected = """# openvpn config: test-client

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
mode p2p
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
pull
remote vpn1.test.com 1194
remote 176.9.43.231 1195
resolv-retry infinite
script-security 1
status /var/log/openvpn.status 30
status-version 1
tls-client
topology p2p
tun-ipv6
up /home/user/up-command.sh
up-delay 10
user nobody
verb 1
"""
        self.assertEqual(c.render(), expected)

    _simple_conf = {
        "openvpn": [
            {
                "name": "test",
                "ca": "ca.pem",
                "cert": "cert.pem",
                "dev": "tap0",
                "dev_type": "tap",
                "dh": "dh.pem",
                "key": "key.pem",
                "mode": "server",
                "proto": "udp",
                "status": "",
                "status_version": 1,
                "tls_server": True,
            }
        ]
    }

    def test_no_status_file(self):
        c = OpenVpn(self._simple_conf)
        output = c.render()
        self.assertNotIn('status', output)
        self.assertNotIn('status-version', output)

    def test_status_file_no_seconds(self):
        conf = copy.deepcopy(self._simple_conf)
        conf['openvpn'][0]['status'] = '/var/run/openvpn.status'
        c = OpenVpn(conf)
        self.assertIn('status /var/run/openvpn.status', c.render())

    def test_server_bridge(self):
        c = OpenVpn(
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
                        "name": "bridged",
                        "proto": "udp",
                        "server_bridge": "10.8.0.4 255.255.255.0 10.8.0.128 10.8.0.254",
                        "tls_server": True,
                    }
                ]
            }
        )
        expected = """# openvpn config: bridged

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
        self.assertEqual(c.render(), expected)

    def test_server_bridge_proxy(self):
        c = OpenVpn(
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
                        "name": "bridged-proxy",
                        "proto": "udp",
                        "server_bridge": "",
                        "tls_server": True,
                    }
                ]
            }
        )
        expected = """# openvpn config: bridged-proxy

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
        self.assertEqual(c.render(), expected)

    def test_server_routed(self):
        c = OpenVpn(
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
                        "name": "routed",
                        "proto": "udp",
                        "server": "10.8.0.0 255.255.0.0",
                        "tls_server": True,
                    }
                ]
            }
        )
        expected = """# openvpn config: routed

ca ca.pem
cert cert.pem
dev tap0
dev-type tap
dh dh.pem
key key.pem
mode server
proto udp
server 10.8.0.0 255.255.0.0
tls-server
"""
        self.assertEqual(c.render(), expected)

    def test_additional_properties(self):
        c = OpenVpn(
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
                        "z_falsy": False,
                        "z_list": ["test1", "test2"],
                        "z_number": 5,
                        "z_string": "string",
                        "z_true_val": True,
                    }
                ]
            }
        )
        expected = """# openvpn config: test-properties

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

    def test_double(self):
        o = OpenVpn(
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
        )
        expected = """# openvpn config: test-1

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
        self.assertEqual(o.render(), expected)

    def test_generate(self):
        o = OpenVpn(
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
        )
        tar = tarfile.open(fileobj=o.generate(), mode='r')
        self.assertEqual(len(tar.getmembers()), 2)
        # network
        vpn1 = tar.getmember('test-1.conf')
        contents = tar.extractfile(vpn1).read().decode()
        expected = """ca ca.pem
cert cert.pem
dev tap0
dev-type tap
dh dh.pem
key key.pem
mode server
proto udp
tls-server
"""
        self.assertEqual(contents, expected)
        # vpn 2
        vpn2 = tar.getmember('test-2.conf')
        contents = tar.extractfile(vpn2).read().decode()
        expected = """ca ca.pem
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
        self.assertEqual(contents, expected)

    def test_auto_client_simple(self):
        client_config = OpenVpn.auto_client(
            'vpn1.test.com',
            {
                "ca": "ca.pem",
                "cert": "cert.pem",
                "dev": "tap0",
                "dev_type": "tap",
                "dh": "dh.pem",
                "key": "key.pem",
                "mode": "server",
                "name": "example-vpn",
                "proto": "udp",
            },
        )
        o = OpenVpn(client_config)
        expected = """# openvpn config: example-vpn

ca ca.pem
cert cert.pem
dev tap0
dev-type tap
key key.pem
mode p2p
nobind
proto udp
remote vpn1.test.com 1195
resolv-retry infinite
"""
        self.assertEqual(o.render(), expected)

    def test_auto_client_tls(self):
        client_config = OpenVpn.auto_client(
            'vpn2.test.com',
            {
                "ca": "ca.pem",
                "cert": "cert.pem",
                "dev": "tap0",
                "dev_type": "tap",
                "dh": "dh.pem",
                "key": "key.pem",
                "mode": "server",
                "name": "example-vpn",
                "port": 1196,
                "proto": "tcp-server",
                "server_bridge": "10.8.0.4 255.255.255.0 10.8.0.128 10.8.0.254",
                "tls_server": True,
            },
        )
        o = OpenVpn(client_config)
        expected = """# openvpn config: example-vpn

ca ca.pem
cert cert.pem
dev tap0
dev-type tap
key key.pem
mode p2p
nobind
proto tcp-client
pull
remote vpn2.test.com 1196
resolv-retry infinite
tls-client
"""
        self.assertEqual(o.render(), expected)

    def test_auto_client_complex(self):
        config = {
            "dev": "tap0",
            "dev_type": "tap",
            "dh": "dh.pem",
            "mode": "server",
            "name": "example-vpn",
            "proto": "tcp-server",
            "tls_server": True,
            "comp_lzo": "yes",
            "auth": "RSA-SHA1",
            "cipher": "AES-128-CFB",
            "engine": "dynamic",
            "ns_cert_type": "client",
            "server_bridge": "",
        }
        client_config = OpenVpn.auto_client(
            'vpn1.test.com',
            config,
            ca_path='{{ca_path_1}}',
            ca_contents='{{ca_contents_1}}',
            cert_path='{{cert_path_1}}',
            cert_contents='{{cert_contents_1}}',
            key_path='{{key_path_1}}',
            key_contents='{{key_contents_1}}',
        )
        o = OpenVpn(client_config)
        expected = """# openvpn config: example-vpn

auth RSA-SHA1
ca {{ca_path_1}}
cert {{cert_path_1}}
cipher AES-128-CFB
comp-lzo yes
dev tap0
dev-type tap
key {{key_path_1}}
mode p2p
nobind
ns-cert-type server
proto tcp-client
pull
remote vpn1.test.com 1195
resolv-retry infinite
tls-client

# ---------- files ---------- #

# path: {{ca_path_1}}
# mode: 0600

{{ca_contents_1}}

# path: {{cert_path_1}}
# mode: 0600

{{cert_contents_1}}

# path: {{key_path_1}}
# mode: 0600

{{key_contents_1}}

"""
        self.assertEqual(o.render(), expected)

    def test_auto_client_ns_cert_type_empty(self):
        client_config = OpenVpn.auto_client(
            'vpn1.test.com',
            {
                "ca": "ca.pem",
                "cert": "cert.pem",
                "dev": "tap0",
                "dev_type": "tap",
                "dh": "dh.pem",
                "key": "key.pem",
                "mode": "server",
                "name": "example-vpn",
                "proto": "udp",
                "server": "10.8.0.0 255.255.0.0",
                "tls_server": True,
                "ns_cert_type": "",
            },
        )
        o = OpenVpn(client_config)
        expected = """# openvpn config: example-vpn

ca ca.pem
cert cert.pem
dev tap0
dev-type tap
key key.pem
mode p2p
nobind
proto udp
pull
remote vpn1.test.com 1195
resolv-retry infinite
tls-client
"""
        self.assertEqual(o.render(), expected)

    def _get_client(self):
        return OpenVpn.auto_client(
            'vpn1.test.com',
            {
                "ca": "ca.pem",
                "cert": "cert.pem",
                "dev": "tap0",
                "dev_type": "tap",
                "dh": "dh.pem",
                "key": "key.pem",
                "mode": "server",
                "name": "example-vpn",
                "proto": "udp",
            },
        )

    def test_resolv_retry_number(self):
        client = self._get_client()
        client['openvpn'][0]['resolv_retry'] = '10'
        o = OpenVpn(client)
        self.assertIn('resolv-retry 10', o.render())

    def test_resolv_retry_disabled(self):
        client = self._get_client()
        client['openvpn'][0]['resolv_retry'] = '0'
        o = OpenVpn(client)
        self.assertIn('resolv-retry 0', o.render())

    def test_resolv_retry_infinite(self):
        client = self._get_client()
        client['openvpn'][0]['resolv_retry'] = 'infinite'
        o = OpenVpn(client)
        self.assertIn('resolv-retry infinite', o.render())

    def test_resolv_retry_not_present(self):
        client = self._get_client()
        del client['openvpn'][0]['resolv_retry']
        o = OpenVpn(client)
        self.assertNotIn('resolv-retry', o.render())

    def test_resolv_retry_invalid(self):
        client = self._get_client()
        client['openvpn'][0]['resolv_retry'] = 'true'
        o = OpenVpn(client)
        with self.assertRaises(ValidationError):
            o.validate()

    def test_double_rendering(self):
        o = OpenVpn(self._simple_conf)
        self.assertEqual(o.render(), o.render())

    def test_override(self):
        template = {
            "openvpn": [
                {
                    "name": "test",
                    "ca": "TEST",
                    "cert": "TEST",
                    "dev": "TEST",
                    "dev_type": "TEST",
                    "dh": "TEST",
                    "key": "TEST",
                }
            ]
        }
        o = OpenVpn(self._simple_conf, templates=[template])
        # ensure dummy values in template have been overridden
        self.assertDictEqual(o.config, self._simple_conf)
