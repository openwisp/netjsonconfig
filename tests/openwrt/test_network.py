import unittest
from netjsonconfig import OpenWrt

from .utils import _TabsMixin


class TestNetworkRenderer(unittest.TestCase, _TabsMixin):
    """
    tests for backends.openwrt.renderers.NetworkRenderer
    """
    maxDiff = None

    def test_loopback(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "lo",
                    "type": "loopback",
                    "addresses": [
                        {
                            "address": "127.0.0.1",
                            "mask": 8,
                            "proto": "static",
                            "family": "ipv4"
                        }
                    ]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'lo'
    option ifname 'lo'
    option ipaddr '127.0.0.1/8'
    option proto 'static'
""")
        self.assertEqual(o.render(), expected)

    def test_multiple_ip(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0.1",
                    "type": "ethernet",
                    "autostart": True,
                    "addresses": [
                        {
                            "address": "192.168.1.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        },
                        {
                            "address": "192.168.2.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        },
                        {
                            "address": "fd87::1",
                            "mask": 128,
                            "proto": "static",
                            "family": "ipv6"
                        }
                    ]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth0_1'
    option auto '1'
    option ifname 'eth0.1'
    option ipaddr '192.168.1.1/24'
    option proto 'static'

config interface 'eth0_1_2'
    option auto '1'
    option ifname 'eth0.1'
    option ipaddr '192.168.2.1/24'
    option proto 'static'

config interface 'eth0_1_3'
    option auto '1'
    option ifname 'eth0.1'
    option ip6addr 'fd87::1/128'
    option proto 'static'
""")
        self.assertEqual(o.render(), expected)

    def test_dhcp(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "proto": "dhcp",
                            "family": "ipv4"
                        }
                    ]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'dhcp'
""")
        self.assertEqual(o.render(), expected)

    def test_multiple_dhcp(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "proto": "dhcp",
                            "family": "ipv4"
                        },
                        {
                            "proto": "dhcp",
                            "family": "ipv6"
                        }
                    ]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'dhcp'

config interface 'eth0_2'
    option ifname 'eth0'
    option proto 'dhcpv6'
""")
        self.assertEqual(o.render(), expected)

    def test_ipv4_routes(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth1",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "address": "192.168.1.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        }
                    ]
                }
            ],
            "routes": [
                {
                    "device": "eth1",
                    "destination": "192.168.3.1/24",
                    "next": "192.168.2.1"
                },
                {
                    "device": "eth1",
                    "destination": "192.168.4.1/24",
                    "next": "192.168.2.2",
                    "cost": 2,
                    "source": "192.168.1.10",
                    "table": 2,
                    "onlink": True,
                    "mtu": 1450
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth1'
    option ifname 'eth1'
    option ipaddr '192.168.1.1/24'
    option proto 'static'

config route 'route1'
    option gateway '192.168.2.1'
    option interface 'eth1'
    option netmask '255.255.255.0'
    option target '192.168.3.1'

config route 'route2'
    option gateway '192.168.2.2'
    option interface 'eth1'
    option metric '2'
    option mtu '1450'
    option netmask '255.255.255.0'
    option onlink '1'
    option source '192.168.1.10'
    option table '2'
    option target '192.168.4.1'
""")
        self.assertEqual(o.render(), expected)

    def test_ipv6_routes(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth1",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "address": "fd87::1",
                            "mask": 128,
                            "proto": "static",
                            "family": "ipv6"
                        }
                    ]
                }
            ],
            "routes": [
                {
                    "device": "eth1",
                    "destination": "fd89::1/128",
                    "next": "fd88::1"
                },
                {
                    "device": "eth1",
                    "destination": "fd90::1/128",
                    "next": "fd88::2",
                    "cost": 3,
                    "source": "fd87::10"
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth1'
    option ifname 'eth1'
    option ip6addr 'fd87::1/128'
    option proto 'static'

config route6
    option gateway 'fd88::1'
    option interface 'eth1'
    option target 'fd89::1/128'

config route6
    option gateway 'fd88::2'
    option interface 'eth1'
    option metric '3'
    option source 'fd87::10'
    option target 'fd90::1/128'
""")
        self.assertEqual(o.render(), expected)

    def test_additional_proto(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "mobile0",
                    "addresses": [
                        {
                            "proto": "3g"
                        }
                    ]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'mobile0'
    option ifname 'mobile0'
    option proto '3g'
""")
        self.assertEqual(o.render(), expected)

    def test_interface_custom_attrs(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "mobile0",
                    "mtu": 1400,
                    "enabled": False,
                    "custom_attr": "yes",
                    "empty": "",
                    "addresses": [
                        {
                            "proto": "3g"
                        }
                    ]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'mobile0'
    option custom_attr 'yes'
    option enabled '0'
    option ifname 'mobile0'
    option mtu '1400'
    option proto '3g'
""")
        self.assertEqual(o.render(), expected)

    def test_eth_bridge(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "address": "192.168.1.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        },
                        # most probably a config that wouldn't work in practice
                        # but needed to ensure that only the first
                        # logical interface contains bridge information
                        {
                            "address": "10.0.0.1",
                            "gateway": "10.0.0.10",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        }
                    ]
                },
                {
                    "name": "eth1",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "proto": "dhcp"
                        }
                    ]
                },
                {
                    "name": "br-eth0",
                    "type": "bridge",
                    "bridge_members": [
                        "eth0",
                        "eth1"
                    ]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth0'
    option ifname 'eth0 eth1'
    option ipaddr '192.168.1.1/24'
    option proto 'static'
    option type 'bridge'

config interface 'eth0_2'
    option gateway '10.0.0.10'
    option ifname 'eth0'
    option ipaddr '10.0.0.1/24'
    option proto 'static'

config interface 'eth1'
    option ifname 'eth1'
    option proto 'dhcp'
""")
        self.assertEqual(o.render(), expected)

    def test_dns(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "address": "192.168.1.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        }
                    ]
                }
            ],
            "dns_servers": [
                "10.11.12.13",
                "8.8.8.8"
            ],
            "dns_search": [
                "netjson.org",
                "openwisp.org",
            ]
        })
        expected = self._tabs("""package network

config interface 'eth0'
    option dns '10.11.12.13 8.8.8.8'
    option dns_search 'netjson.org openwisp.org'
    option ifname 'eth0'
    option ipaddr '192.168.1.1/24'
    option proto 'static'
""")
        self.assertEqual(o.render(), expected)

    def test_rules(self):
        o = OpenWrt({
            "ip_rules": [
                {
                    "in": "eth0",
                    "out": "eth1",
                    "src": "192.168.1.0/24",
                    "dest": "192.168.2.0/24",
                    "tos": 2,
                    "mark": "0x0/0x1",
                    "invert": True,
                    "lookup": "0",
                    "action": "blackhole"
                },
                {
                    "src": "192.168.1.0/24",
                    "dest": "192.168.3.0/24",
                    "goto": 0
                },
                {
                    "in": "vpn",
                    "dest": "fdca:1234::/64",
                    "action": "prohibit"
                },
                {
                    "in": "vpn",
                    "src": "fdca:1235::/64",
                    "action": "prohibit"
                }
            ]
        })
        expected = self._tabs("""package network

config rule
    option action 'blackhole'
    option dest '192.168.2.0/24'
    option in 'eth0'
    option invert '1'
    option lookup '0'
    option mark '0x0/0x1'
    option out 'eth1'
    option src '192.168.1.0/24'
    option tos '2'

config rule
    option dest '192.168.3.0/24'
    option goto '0'
    option src '192.168.1.0/24'

config rule6
    option action 'prohibit'
    option dest 'fdca:1234::/64'
    option in 'vpn'

config rule6
    option action 'prohibit'
    option in 'vpn'
    option src 'fdca:1235::/64'
""")
        self.assertEqual(o.render(), expected)

    def test_switch(self):
        o = OpenWrt({
            "switch": [
                {
                    "name": "switch0",
                    "reset": True,
                    "enable_vlan": True,
                    "vlan": [
                        {
                            "device": "switch0",
                            "vlan": 1,
                            "ports": "0t 2 3 4 5"
                        },
                        {
                            "device": "switch0",
                            "vlan": 2,
                            "ports": "0t 1"
                        }
                    ]
                },
                {
                    "name": "switch1",
                    "reset": True,
                    "enable_vlan": True,
                    "vlan": [
                        {
                            "device": "switch1",
                            "vlan": 3,
                            "ports": "0t 6 7"
                        }
                    ]
                }
            ]
        })
        expected = self._tabs("""package network

config switch
    option enable_vlan '1'
    option name 'switch0'
    option reset '1'

config switch_vlan
    option device 'switch0'
    option ports '0t 2 3 4 5'
    option vlan '1'

config switch_vlan
    option device 'switch0'
    option ports '0t 1'
    option vlan '2'

config switch
    option enable_vlan '1'
    option name 'switch1'
    option reset '1'

config switch_vlan
    option device 'switch1'
    option ports '0t 6 7'
    option vlan '3'
""")
        self.assertEqual(o.render(), expected)
