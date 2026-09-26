import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestVxlan(unittest.TestCase, _TabsMixin):
    maxDiff = None

    def test_render_vxlan(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "vxlan1",
                        "type": "vxlan",
                        "vtep": "10.0.0.1",
                        "port": 4789,
                        "vni": 1,
                        "tunlink": "wg0",
                        "rxcsum": True,
                        "txcsum": True,
                        "mtu": 1280,
                        "ttl": 64,
                    }
                ]
            }
        )
        expected = self._tabs("""package network

config interface 'vxlan1'
    option device 'vxlan1'
    option mtu '1280'
    option peeraddr '10.0.0.1'
    option port '4789'
    option proto 'vxlan'
    option rxcsum '1'
    option ttl '64'
    option tunlink 'wg0'
    option txcsum '1'
    option vid '1'
""")
        self.assertEqual(o.render(), expected)

    def test_parse_vxlan(self):
        native = self._tabs("""package network

config interface 'vxlan1'
    option {option} 'vxlan1'
    option mtu '1280'
    option peeraddr '10.0.0.1'
    option port '4789'
    option proto 'vxlan'
    option rxcsum '1'
    option ttl '64'
    option tunlink 'wg0'
    option txcsum '1'
    option vid '1'
""")
        expected = {
            "interfaces": [
                {
                    "name": "vxlan1",
                    "type": "vxlan",
                    "vtep": "10.0.0.1",
                    "port": 4789,
                    "vni": 1,
                    "tunlink": "wg0",
                    "rxcsum": True,
                    "txcsum": True,
                    "mtu": 1280,
                    "ttl": 64,
                }
            ]
        }
        # "ifname" is what older netjsonconfig versions rendered
        for option in ["device", "ifname"]:
            with self.subTest(option=option):
                o = OpenWrt(native=native.format(option=option))
                self.assertEqual(o.config, expected)

    def test_vxlan_legacy_syntax(self):
        config = {
            "interfaces": [
                {
                    "name": "vxlan1",
                    "type": "vxlan",
                    "vtep": "10.0.0.1",
                    "port": 4789,
                    "vni": 1,
                    "tunlink": "wg0",
                    "rxcsum": True,
                    "txcsum": True,
                    "mtu": 1280,
                    "ttl": 64,
                }
            ]
        }
        native = self._tabs("""package network

config interface 'vxlan1'
    option ifname 'vxlan1'
    option mtu '1280'
    option peeraddr '10.0.0.1'
    option port '4789'
    option proto 'vxlan'
    option rxcsum '1'
    option ttl '64'
    option tunlink 'wg0'
    option txcsum '1'
    option vid '1'
""")
        self.assertEqual(OpenWrt(config, dsa=False).render(), native)
        self.assertEqual(OpenWrt(native=native, dsa=False).config, config)

    def test_render_vxlan_with_variables(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "type": "vxlan",
                        "name": "vxlan2",
                        "vtep": "{{ vtep_e9081f8d67c8470d850ceb9c33bd0314 }}",
                        "port": 4789,
                        "vni": "{{ vni_e9081f8d67c8470d850ceb9c33bd0314 }}",
                        "tunlink": "wg0",
                        "rxcsum": False,
                        "txcsum": False,
                        "mtu": 1280,
                        "ttl": 64,
                    }
                ]
            },
            context={
                "vtep_e9081f8d67c8470d850ceb9c33bd0314": "10.0.0.2",
                "vni_e9081f8d67c8470d850ceb9c33bd0314": "2",
            },
        )
        expected = self._tabs("""package network

config interface 'vxlan2'
    option device 'vxlan2'
    option mtu '1280'
    option peeraddr '10.0.0.2'
    option port '4789'
    option proto 'vxlan'
    option rxcsum '0'
    option ttl '64'
    option tunlink 'wg0'
    option txcsum '0'
    option vid '2'
""")
        self.assertEqual(o.render(), expected)
