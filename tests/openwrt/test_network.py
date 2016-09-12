import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.exceptions import ValidationError
from netjsonconfig.utils import _TabsMixin


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
    option ipaddr '127.0.0.1'
    option netmask '255.0.0.0'
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
    option ipaddr '192.168.1.1'
    option netmask '255.255.255.0'
    option proto 'static'

config interface 'eth0_1_2'
    option auto '1'
    option ifname 'eth0.1'
    option ipaddr '192.168.2.1'
    option netmask '255.255.255.0'
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
                    "next": "192.168.2.1",
                    "cost": 0
                },
                {
                    "device": "eth1",
                    "destination": "192.168.4.1/24",
                    "next": "192.168.2.2",
                    "cost": 2,
                    "source": "192.168.1.10",
                    "table": "2",
                    "onlink": True,
                    "mtu": "1450",
                    "type": "unicast"
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth1'
    option ifname 'eth1'
    option ipaddr '192.168.1.1'
    option netmask '255.255.255.0'
    option proto 'static'

config route 'route1'
    option gateway '192.168.2.1'
    option interface 'eth1'
    option metric '0'
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
    option type 'unicast'
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
                    "next": "fd88::1",
                    "cost": 0
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

config route6 'route1'
    option gateway 'fd88::1'
    option interface 'eth1'
    option metric '0'
    option target 'fd89::1/128'

config route6 'route2'
    option gateway 'fd88::2'
    option interface 'eth1'
    option metric '3'
    option source 'fd87::10'
    option target 'fd90::1/128'
""")
        self.assertEqual(o.render(), expected)

    def test_custom_proto(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "ppp0",
                    "type": "other",
                    "proto": "ppp",
                    "device": "/dev/usb/modem1",
                    "username": "user1",
                    "password": "pwd0123",
                    "keepalive": 3,
                    "ipv6": True
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'ppp0'
    option device '/dev/usb/modem1'
    option ifname 'ppp0'
    option ipv6 '1'
    option keepalive '3'
    option password 'pwd0123'
    option proto 'ppp'
    option username 'user1'
""")
        self.assertEqual(o.render(), expected)

    def test_interface_disabled(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "disabled": True,
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth0'
    option enabled '0'
    option ifname 'eth0'
    option proto 'none'
""")
        self.assertEqual(o.render(), expected)

    def test_interface_custom_attrs(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "mobile0",
                    "type": "wireless",
                    "mtu": 1400,
                    "custom_attr": "yes",
                    "empty": "",
                    "proto": "3g",
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'mobile0'
    option custom_attr 'yes'
    option ifname 'mobile0'
    option mtu '1400'
    option proto '3g'
""")
        self.assertEqual(o.render(), expected)

    def test_simple_bridge(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet"
                },
                {
                    "name": "eth1",
                    "type": "ethernet"
                },
                {
                    "network": "lan",
                    "name": "br-lan",
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
    option ifname 'eth0'
    option proto 'none'

config interface 'eth1'
    option ifname 'eth1'
    option proto 'none'

config interface 'lan'
    option ifname 'eth0 eth1'
    option proto 'none'
    option type 'bridge'
""")
        self.assertEqual(o.render(), expected)

    def test_eth_bridge(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet"
                },
                {
                    "name": "eth1",
                    "type": "ethernet",
                },
                {
                    "name": "lan",
                    "type": "bridge",
                    "bridge_members": [
                        "eth0",
                        "eth1"
                    ],
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
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'none'

config interface 'eth1'
    option ifname 'eth1'
    option proto 'none'

config interface 'lan'
    option ifname 'eth0 eth1'
    option ipaddr '192.168.1.1'
    option netmask '255.255.255.0'
    option proto 'static'
    option type 'bridge'

config interface 'lan_2'
    option gateway '10.0.0.10'
    option ifname 'br-lan'
    option ipaddr '10.0.0.1'
    option netmask '255.255.255.0'
    option proto 'static'
""")
        self.assertEqual(o.render(), expected)

    def test_empty_bridge(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "network": "lan",
                    "name": "br-lan",
                    "type": "bridge",
                    "bridge_members": []
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'lan'
    option bridge_empty '1'
    option proto 'none'
    option type 'bridge'
""")
        self.assertEqual(o.render(), expected)

    def test_bridge_members_schema(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "lan",
                    "type": "bridge"
                }
            ]
        })
        with self.assertRaises(ValidationError):
            o.validate()
        o.config['interfaces'][0]['bridge_members'] = [3]
        with self.assertRaises(ValidationError):
            o.validate()
        # ensure fix works
        o.config['interfaces'][0]['bridge_members'] = ['eth0', 'wlan0']
        o.validate()

    def test_bridge_members_pattern(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "lan",
                    "type": "bridge",
                    "bridge_members": ["eth 0"]
                }
            ]
        })
        with self.assertRaises(ValidationError):
            o.validate()
        # ensure fix works
        o.config['interfaces'][0]['bridge_members'][0] = 'e-t_h@=0.1'
        o.validate()

    def test_bridge_members_unique(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "lan",
                    "type": "bridge",
                    "bridge_members": ["eth0", "eth0"]
                }
            ]
        })
        with self.assertRaises(ValidationError):
            o.validate()
        # ensure fix works
        o.config['interfaces'][0]['bridge_members'][0] = 'eth1'
        o.validate()

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
            "dns_servers": ["10.11.12.13", "8.8.8.8"],
            "dns_search": ["netjson.org", "openwisp.org"],
        })
        expected = self._tabs("""package network

config interface 'eth0'
    option dns '10.11.12.13 8.8.8.8'
    option dns_search 'netjson.org openwisp.org'
    option ifname 'eth0'
    option ipaddr '192.168.1.1'
    option netmask '255.255.255.0'
    option proto 'static'
""")
        self.assertEqual(o.render(), expected)

    def test_dns_dhcpv4_ignored(self):
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
            ],
            "dns_servers": ["10.11.12.13", "8.8.8.8"],
            "dns_search": ["netjson.org", "openwisp.org"],
        })
        expected = self._tabs("""package network

config interface 'eth0'
    option dns_search 'netjson.org openwisp.org'
    option ifname 'eth0'
    option proto 'dhcp'
""")
        self.assertEqual(o.render(), expected)

    def test_dns_dhcpv6_ignored(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "proto": "dhcp",
                            "family": "ipv6"
                        }
                    ]
                }
            ],
            "dns_servers": ["10.11.12.13", "8.8.8.8"],
            "dns_search": ["netjson.org", "openwisp.org"],
        })
        expected = self._tabs("""package network

config interface 'eth0'
    option dns_search 'netjson.org openwisp.org'
    option ifname 'eth0'
    option proto 'dhcpv6'
""")
        self.assertEqual(o.render(), expected)

    def test_dhcp_ignored_proto_none(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                }
            ],
            "dns_servers": ["10.11.12.13", "8.8.8.8"],
            "dns_search": ["netjson.org", "openwisp.org"],
        })
        expected = self._tabs("""package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'none'
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

config rule 'rule1'
    option action 'blackhole'
    option dest '192.168.2.0/24'
    option in 'eth0'
    option invert '1'
    option lookup '0'
    option mark '0x0/0x1'
    option out 'eth1'
    option src '192.168.1.0/24'
    option tos '2'

config rule 'rule2'
    option dest '192.168.3.0/24'
    option goto '0'
    option src '192.168.1.0/24'

config rule6 'rule3'
    option action 'prohibit'
    option dest 'fdca:1234::/64'
    option in 'vpn'

config rule6 'rule4'
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

config switch 'switch0'
    option enable_vlan '1'
    option name 'switch0'
    option reset '1'

config switch_vlan 'switch0_vlan1'
    option device 'switch0'
    option ports '0t 2 3 4 5'
    option vlan '1'

config switch_vlan 'switch0_vlan2'
    option device 'switch0'
    option ports '0t 1'
    option vlan '2'

config switch 'switch1'
    option enable_vlan '1'
    option name 'switch1'
    option reset '1'

config switch_vlan 'switch1_vlan1'
    option device 'switch1'
    option ports '0t 6 7'
    option vlan '3'
""")
        self.assertEqual(o.render(), expected)

    def test_empty_interface(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet"
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'none'
""")
        self.assertEqual(o.render(), expected)

    def test_ifname_length(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "ifname0123456789",
                    "type": "ethernet"
                }
            ]
        })
        with self.assertRaises(ValidationError):
            o.validate()
        # ensure fix works
        o.config['interfaces'][0]['name'] = 'ifname0'
        o.validate()

    def test_ifname_pattern(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth 0",
                    "type": "ethernet"
                }
            ]
        })
        with self.assertRaises(ValidationError):
            o.validate()
        # ensure fix works
        o.config['interfaces'][0]['name'] = 'e-t_h@=0.1'
        o.validate()

    def test_network_maxlength(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "network": "lan0123456789012345",
                    "type": "ethernet"
                }
            ]
        })
        with self.assertRaises(ValidationError):
            o.validate()
        # ensure fix works
        o.config['interfaces'][0]['network'] = 'lan'
        o.validate()

    def test_network_pattern(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "network": "lan 0",
                    "type": "ethernet"
                }
            ]
        })
        with self.assertRaises(ValidationError):
            o.validate()
        o.config['interfaces'][0]['network'] = 'lan/0'
        with self.assertRaises(ValidationError):
            o.validate()
        # ensure fix works
        o.config['interfaces'][0]['network'] = 'lan'
        o.validate()

    def test_network_attribute(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "network": "lan",
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
                        }
                    ]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'lan'
    option ifname 'eth0'
    option ipaddr '192.168.1.1'
    option netmask '255.255.255.0'
    option proto 'static'

config interface 'lan_2'
    option ifname 'eth0'
    option ipaddr '192.168.2.1'
    option netmask '255.255.255.0'
    option proto 'static'
""")
        self.assertEqual(o.render(), expected)

    def test_network_dot_conversion(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0.1",
                    "type": "ethernet",
                    "network": "lan.1",
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'lan_1'
    option ifname 'eth0.1'
    option proto 'none'
""")
        self.assertEqual(o.render(), expected)

    def test_network_dash_conversion(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth-0",
                    "type": "ethernet",
                    "network": "lan-0",
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'lan_0'
    option ifname 'eth-0'
    option proto 'none'
""")
        self.assertEqual(o.render(), expected)

    def test_ula_prefix(self):
        o = OpenWrt({
            "general": {"ula_prefix": "fd8e:f40a:6701::/48"}
        })
        expected = self._tabs("""package network

config globals 'globals'
    option ula_prefix 'fd8e:f40a:6701::/48'
""")
        self.assertEqual(o.render(), expected)

    def test_empty_dns(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet"
                }
            ],
            "dns_servers": [],
            "dns_search": []
        })
        expected = self._tabs("""package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'none'
""")
        self.assertEqual(o.render(), expected)

    def test_mac_address_format(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "mac": "00:11:22:33:44:55"
                }
            ]
        })
        o.validate()
        # too short
        o.config['interfaces'][0]['mac'] = '00:11:22:33:44'
        with self.assertRaises(ValidationError):
            o.validate()
        # valid
        o.config['interfaces'][0]['mac'] = '00-11-22-33-44-55'
        o.validate()
        # should not be valid
        o.config['interfaces'][0]['mac'] = '00:11:22:33:44:ZY'
        with self.assertRaises(ValidationError):
            o.validate()
        # empty is valid (will be ignored)
        o.config['interfaces'][0]['mac'] = ''
        o.validate()

    def test_default_addresses(self):
        """
        the following configuration dictionary caused empty output up to 0.4.0
        """
        o = OpenWrt({
            "interfaces": [
                {
                    "type": "bridge",
                    "network": "lan",
                    "addresses": [],
                    "name": "br-lan",
                    "bridge_members": [
                        "eth0",
                        "eth1"
                    ]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'lan'
    option ifname 'eth0 eth1'
    option proto 'none'
    option type 'bridge'
""")
        self.assertEqual(o.render(), expected)

    def test_interface_list_option(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "ip6class": ["wan6", "backbone"]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth0'
    option ifname 'eth0'
    list ip6class 'wan6'
    list ip6class 'backbone'
    option proto 'none'
""")
        self.assertEqual(o.render(), expected)

    def test_address_list_option(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "proto": "dhcp",
                            "family": "ipv4",
                            "reqopts": ["43", "54"]
                        }
                    ]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'dhcp'
    list reqopts '43'
    list reqopts '54'
""")
        self.assertEqual(o.render(), expected)

    def test_dns_override(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "dns": ["8.8.8.8", "8.8.4.4"]
                }
            ],
            "dns_servers": ["192.168.3.1", "192.168.3.2"]
        })
        expected = self._tabs("""package network

config interface 'eth0'
    list dns '8.8.8.8'
    list dns '8.8.4.4'
    option ifname 'eth0'
    option proto 'none'
""")
        self.assertEqual(o.render(), expected)

    def test_dns_search_override(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "dns_search": ["openwisp.org", "netjson.org"]
                }
            ],
            "dns_search": ["domain.com"]
        })
        expected = self._tabs("""package network

config interface 'eth0'
    list dns_search 'openwisp.org'
    list dns_search 'netjson.org'
    option ifname 'eth0'
    option proto 'none'
""")
        self.assertEqual(o.render(), expected)

    def test_spanning_tree(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "br-lan",
                    "type": "bridge",
                    "stp": True,
                    "bridge_members": ["eth0", "eth1"]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'br_lan'
    option ifname 'eth0 eth1'
    option proto 'none'
    option stp '1'
    option type 'bridge'
""")
        self.assertEqual(o.render(), expected)
        # try entering an invalid value
        o.config['interfaces'][0]['stp'] = 'wrong'
        with self.assertRaises(ValidationError):
            o.validate()

    def test_igmp(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "br-lan",
                    "type": "bridge",
                    "igmp_snooping": True,
                    "bridge_members": ["eth0", "eth1"]
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'br_lan'
    option ifname 'eth0 eth1'
    option igmp_snooping '1'
    option proto 'none'
    option type 'bridge'
""")
        self.assertEqual(o.render(), expected)
        # try entering an invalid value
        o.config['interfaces'][0]['igmp_snooping'] = 'wrong'
        with self.assertRaises(ValidationError):
            o.validate()

    def test_autostart(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "autostart": False
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth0'
    option auto '0'
    option ifname 'eth0'
    option proto 'none'
""")
        self.assertEqual(o.render(), expected)

    def test_macaddr_override(self):
        o = OpenWrt({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "mac": "E8:94:F6:33:8C:00"
                }
            ]
        })
        expected = self._tabs("""package network

config interface 'eth0'
    option ifname 'eth0'
    option macaddr 'E8:94:F6:33:8C:00'
    option proto 'none'
""")
        self.assertEqual(o.render(), expected)
