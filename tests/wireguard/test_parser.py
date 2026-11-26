import io
import tarfile
import unittest

from netjsonconfig import Wireguard


class TestParser(unittest.TestCase):
    """
    Tests for netjsonconfig.backends.wireguard.parser.WireguardParser
    """

    maxDiff = None

    def test_parse_text(self):
        native = """# wireguard config: wg0

[Interface]
Address = 10.0.0.1/24
DNS = 8.8.8.8,1.1.1.1
ListenPort = 51820
MTU = 1420
PrivateKey = QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=
SaveConfig = true

[Peer]
AllowedIPs = 10.0.0.3/32
Endpoint = 192.168.1.35:4908
PreSharedKey = xisFXck9KfEZga4lQsgIrGqVTkvHgs1XbTzschTLFzE=
PublicKey = jqHs76yCH0wThMSqogDshqcnR9Ymi3wgmvxRkUyMzgU=

[Peer]
AllowedIPs = 10.0.0.4/32
PublicKey = 94a+MnZSdzHCzOy5y2K+0+Xe7lQzaG4ilMmpixEYURA=
"""
        expected = {
            "wireguard": [
                {
                    "name": "wg0",
                    "port": 51820,
                    "private_key": "QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=",
                    "address": "10.0.0.1/24",
                    "dns": ["8.8.8.8", "1.1.1.1"],
                    "mtu": 1420,
                    "save_config": True,
                    "peers": [
                        {
                            "allowed_ips": "10.0.0.3/32",
                            "endpoint_host": "192.168.1.35",
                            "endpoint_port": 4908,
                            "preshared_key": (
                                "xisFXck9KfEZga4lQsgIrGqVTkvHgs1XbTzschTLFzE="
                            ),
                            "public_key": (
                                "jqHs76yCH0wThMSqogDshqcnR9Ymi3wgmvxRkUyMzgU="
                            ),
                        },
                        {
                            "allowed_ips": "10.0.0.4/32",
                            "public_key": (
                                "94a+MnZSdzHCzOy5y2K+0+Xe7lQzaG4ilMmpixEYURA="
                            ),
                        },
                    ],
                }
            ]
        }
        self.assertDictEqual(Wireguard(native=native).config, expected)

    def test_parse_interface_without_peers(self):
        native = """# wireguard config: wg0

[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=
"""
        expected = {
            "wireguard": [
                {
                    "name": "wg0",
                    "port": 51820,
                    "private_key": "QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=",
                    "address": "10.0.0.1/24",
                }
            ]
        }
        self.assertDictEqual(Wireguard(native=native).config, expected)

    def test_parse_ipv6_endpoint(self):
        """The port is separated by the last colon of the endpoint."""
        native = """# wireguard config: wg0

[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=

[Peer]
AllowedIPs = 10.0.0.3/32
Endpoint = [2001:db8::1]:4908
PublicKey = jqHs76yCH0wThMSqogDshqcnR9Ymi3wgmvxRkUyMzgU=
"""
        peer = Wireguard(native=native).config["wireguard"][0]["peers"][0]
        self.assertEqual(peer["endpoint_host"], "[2001:db8::1]")
        self.assertEqual(peer["endpoint_port"], 4908)

    def test_parse_endpoint_without_port(self):
        native = """# wireguard config: wg0

[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=

[Peer]
AllowedIPs = 10.0.0.3/32
Endpoint = 192.168.1.35
PublicKey = jqHs76yCH0wThMSqogDshqcnR9Ymi3wgmvxRkUyMzgU=
"""
        peer = Wireguard(native=native).config["wireguard"][0]["peers"][0]
        self.assertEqual(peer["endpoint_host"], "192.168.1.35")
        self.assertNotIn("endpoint_port", peer)

    def test_parse_unrecognized_directive(self):
        """Unrecognized directives are kept, as the OpenVPN parser does."""
        native = """# wireguard config: wg0

[Interface]
Address = 10.0.0.1/24
FwMark = 0x42
ListenPort = 51820
PrivateKey = QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=
"""
        vpn = Wireguard(native=native).config["wireguard"][0]
        self.assertEqual(vpn["FwMark"], "0x42")

    def test_parse_comments_are_ignored(self):
        native = """# wireguard config: wg0

[Interface]
# this is a comment
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=
"""
        vpn = Wireguard(native=native).config["wireguard"][0]
        self.assertNotIn("# this is a comment", vpn)
        self.assertEqual(vpn["address"], "10.0.0.1/24")

    def test_parse_inline_comments(self):
        native = """# wireguard config: wg0

[Interface] # local side
Address = 10.0.0.1/24 # tunnel address
ListenPort = 51820 # listener
PrivateKey = QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=

[Peer] # remote side
AllowedIPs = 10.0.0.2/32
PublicKey = 94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE=
"""
        vpn = Wireguard(native=native).config["wireguard"][0]
        self.assertEqual(vpn["address"], "10.0.0.1/24")
        self.assertEqual(vpn["port"], 51820)
        self.assertEqual(len(vpn["peers"]), 1)
        self.assertEqual(vpn["peers"][0]["allowed_ips"], "10.0.0.2/32")

    def test_parse_repeated_list_directives(self):
        native = """# wireguard config: wg0

[Interface]
Address = 10.0.0.1/24
Address = fd00::1/64
DNS = 1.1.1.1
DNS = 8.8.8.8, 8.8.4.4
ListenPort = 51820
PrivateKey = QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=

[Peer]
AllowedIPs = 10.0.0.2/32
AllowedIPs = fd00::2/128
PublicKey = 94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE=
"""
        vpn = Wireguard(native=native).config["wireguard"][0]
        self.assertEqual(vpn["address"], "10.0.0.1/24, fd00::1/64")
        self.assertEqual(vpn["dns"], ["1.1.1.1", "8.8.8.8", "8.8.4.4"])
        self.assertEqual(vpn["peers"][0]["allowed_ips"], "10.0.0.2/32, fd00::2/128")

    def test_parse_empty_dns(self):
        native = """# wireguard config: wg0

[Interface]
Address = 10.0.0.1/24
DNS =
ListenPort = 51820
PrivateKey = QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=
"""
        vpn = Wireguard(native=native).config["wireguard"][0]
        self.assertEqual(vpn["dns"], [])

    def test_parse_repeated_dns_deduplicated(self):
        native = """# wireguard config: wg0

[Interface]
Address = 10.0.0.1/24
DNS = 1.1.1.1, 8.8.8.8
DNS = 1.1.1.1
ListenPort = 51820
PrivateKey = QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=
"""
        vpn = Wireguard(native=native).config["wireguard"][0]
        self.assertEqual(vpn["dns"], ["1.1.1.1", "8.8.8.8"])

    def test_parse_empty_optional_values(self):
        native = """# wireguard config: wg0

[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
MTU =
PrivateKey = QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=

[Peer]
AllowedIPs = 10.0.0.2/32
PersistentKeepalive =
PublicKey = 94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE=
"""
        vpn = Wireguard(native=native).config["wireguard"][0]
        self.assertNotIn("mtu", vpn)
        self.assertNotIn("PersistentKeepalive", vpn["peers"][0])
        self.assertNotIn("persistent_keepalive", vpn["peers"][0])

    def test_parse_standard_preshared_key_spelling(self):
        native = """# wireguard config: wg0

[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=

[Peer]
AllowedIPs = 10.0.0.2/32
PresharedKey = xisFXck9KfEZga4hlkproH6+86S8ki1tmLtMtqVipjg=
PublicKey = 94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE=
"""
        peer = Wireguard(native=native).config["wireguard"][0]["peers"][0]
        self.assertEqual(
            peer["preshared_key"], "xisFXck9KfEZga4hlkproH6+86S8ki1tmLtMtqVipjg="
        )
        self.assertNotIn("PresharedKey", peer)

    def test_parse_case_insensitive_directives(self):
        native = """# wireguard config: wg0

[interface]
address = 10.0.0.1/24
dns = 1.1.1.1
listenport = 51820
privatekey = QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=
CustomOption = value

[peer]
allowedips = 10.0.0.2/32
publickey = 94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE=
"""
        vpn = Wireguard(native=native).config["wireguard"][0]
        self.assertEqual(vpn["port"], 51820)
        self.assertEqual(
            vpn["private_key"], "QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg="
        )
        self.assertEqual(vpn["address"], "10.0.0.1/24")
        self.assertEqual(vpn["dns"], ["1.1.1.1"])
        # unknown directives keep their original spelling
        self.assertEqual(vpn["CustomOption"], "value")
        peer = vpn["peers"][0]
        self.assertEqual(peer["allowed_ips"], "10.0.0.2/32")
        self.assertEqual(
            peer["public_key"], "94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE="
        )

    def test_parse_multiple_vpns(self):
        native = """# wireguard config: wg0

[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=

# wireguard config: wg1

[Interface]
Address = 10.0.1.1/24
ListenPort = 51821
PrivateKey = aFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=
"""
        config = Wireguard(native=native).config
        self.assertEqual(len(config["wireguard"]), 2)
        self.assertEqual(config["wireguard"][0]["name"], "wg0")
        self.assertEqual(config["wireguard"][1]["name"], "wg1")
        self.assertEqual(config["wireguard"][1]["port"], 51821)

    def test_parse_tar(self):
        config = {
            "wireguard": [
                {
                    "name": "wg0",
                    "port": 51820,
                    "private_key": "QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=",
                    "address": "10.0.0.1/24",
                }
            ]
        }
        tar = Wireguard(config).generate()
        self.assertDictEqual(Wireguard(native=tar).config, config)

    def test_parse_tar_ignores_files_without_conf_suffix(self):
        native = (
            b"[Interface]\n"
            b"Address = 10.0.0.1/24\n"
            b"ListenPort = 51820\n"
            b"PrivateKey = QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=\n"
        )
        fileobj = io.BytesIO()
        with tarfile.open(fileobj=fileobj, mode="w:gz") as tar:
            for name, contents in (("wg0.conf", native), ("README", b"not a config")):
                info = tarfile.TarInfo(name=name)
                info.size = len(contents)
                tar.addfile(info, io.BytesIO(contents))
        fileobj.seek(0)
        config = Wireguard(native=fileobj).config
        self.assertEqual(len(config["wireguard"]), 1)
        self.assertEqual(config["wireguard"][0]["name"], "wg0")

    def test_parse_ignores_lines_without_assignment(self):
        native = """# wireguard config: wg0

[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=
not-a-directive
"""
        self.assertDictEqual(
            Wireguard(native=native).config,
            {
                "wireguard": [
                    {
                        "name": "wg0",
                        "port": 51820,
                        "private_key": "QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=",
                        "address": "10.0.0.1/24",
                    }
                ]
            },
        )

    def test_render_parse_round_trip(self):
        config = {
            "wireguard": [
                {
                    "name": "wg0",
                    "port": 51820,
                    "private_key": "QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=",
                    "address": "10.0.0.1/24",
                    "dns": ["8.8.8.8", "1.1.1.1"],
                    "mtu": 1420,
                    "save_config": True,
                    "peers": [
                        {
                            "public_key": (
                                "jqHs76yCH0wThMSqogDshqcnR9Ymi3wgmvxRkUyMzgU="
                            ),
                            "allowed_ips": "10.0.0.3/32",
                            "endpoint_host": "192.168.1.35",
                            "endpoint_port": 4908,
                            "preshared_key": (
                                "xisFXck9KfEZga4lQsgIrGqVTkvHgs1XbTzschTLFzE="
                            ),
                        },
                        {
                            "public_key": (
                                "94a+MnZSdzHCzOy5y2K+0+Xe7lQzaG4ilMmpixEYURA="
                            ),
                            "allowed_ips": "10.0.0.4/32",
                        },
                    ],
                }
            ]
        }
        native = Wireguard(config).render()
        self.assertDictEqual(Wireguard(native=native).config, config)

    def test_save_config_false_round_trip(self):
        config = {
            "wireguard": [
                {
                    "name": "wg0",
                    "port": 51820,
                    "private_key": "QFdbnuYr7rVVt3rIzDQHIjJvl3Z9IrDM1W/0oBYPThg=",
                    "address": "10.0.0.1/24",
                    "save_config": False,
                }
            ]
        }
        native = Wireguard(config).render()
        self.assertIn("SaveConfig = false", native)
        parsed = Wireguard(native=native).config["wireguard"][0]
        # "false" must not be parsed as the truthy string "false"
        self.assertIs(parsed["save_config"], False)
