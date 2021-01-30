import unittest
from copy import deepcopy

from netjsonconfig import OpenWrt
from netjsonconfig.exceptions import ValidationError
from netjsonconfig.utils import _TabsMixin


class TestInterfaces(unittest.TestCase, _TabsMixin):
    maxDiff = None

    def test_render_loopback(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "lo",
                        "type": "loopback",
                        "addresses": [
                            {
                                "address": "127.0.0.1",
                                "mask": 8,
                                "proto": "static",
                                "family": "ipv4",
                            }
                        ],
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'lo'
    option ifname 'lo'
    option ipaddr '127.0.0.1'
    option netmask '255.0.0.0'
    option proto 'static'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_loopback(self):
        native = self._tabs(
            """package network

config interface 'lo'
    option ifname 'lo'
    option ipaddr '127.0.0.1'
    option netmask '255.0.0.0'
    option proto 'static'
"""
        )
        expected = {
            "interfaces": [
                {
                    "name": "lo",
                    "type": "loopback",
                    "addresses": [
                        {
                            "address": "127.0.0.1",
                            "mask": 8,
                            "proto": "static",
                            "family": "ipv4",
                        }
                    ],
                }
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_parse_ipv4_cidr(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option ipaddr '192.168.1.2/24'
    option proto 'static'
    option gateway '192.168.1.1'
"""
        )
        expected = {
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "address": "192.168.1.2",
                            "gateway": "192.168.1.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4",
                        }
                    ],
                }
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_parse_mising_proto(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
"""
        )
        expected = {"interfaces": [{"name": "eth0", "type": "ethernet"}]}
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_parse_incorrect_ipaddr(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option ipaddr '/'
"""
        )
        expected = {"interfaces": [{"name": "eth0", "type": "ethernet"}]}
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_parse_incorrect_ipaddr_netmask(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option ipaddr '/'
    option netmask '255.255.255.0'
"""
        )
        expected = {"interfaces": [{"name": "eth0", "type": "ethernet"}]}
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    _eth0_32 = {
        "interfaces": [
            {
                "name": "eth0",
                "type": "ethernet",
                "addresses": [
                    {
                        "address": "192.168.1.1",
                        "mask": 32,
                        "proto": "static",
                        "family": "ipv4",
                    }
                ],
            }
        ]
    }
    _eth0_64 = {
        "interfaces": [
            {
                "name": "eth0",
                "type": "ethernet",
                "addresses": [
                    {
                        "address": "2aa1:4aaa:2aaa:1d::5",
                        "mask": 64,
                        "proto": "static",
                        "family": "ipv6",
                    }
                ],
            }
        ]
    }

    def test_parse_missing_ipv4_mask(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option ipaddr '192.168.1.1'
    option proto 'static'
"""
        )
        o = OpenWrt(native=native)
        self.assertEqual(o.config, self._eth0_32)

    def test_parse_forgotten_ipv4_mask(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option ipaddr '192.168.1.1/'
    option proto 'static'
"""
        )
        o = OpenWrt(native=native)
        self.assertEqual(o.config, self._eth0_32)

    def test_parse_missing_ipv4_mask_list(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    list ipaddr '192.168.1.1'
    option proto 'static'
"""
        )
        o = OpenWrt(native=native)
        self.assertEqual(o.config, self._eth0_32)

    def test_parse_missing_ipv6_mask_list(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option ip6addr '2aa1:4aaa:2aaa:1d::5/64'
    option proto 'static'
"""
        )
        o = OpenWrt(native=native)
        self.assertEqual(o.config, self._eth0_64)

    def test_parse_ipv4_list(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    list ipaddr '192.168.1.1/'
    list ipaddr '192.168.2.1/24'
    list ipaddr '/'
    option proto 'static'
"""
        )
        expected = {
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "address": "192.168.1.1",
                            "mask": 32,
                            "proto": "static",
                            "family": "ipv4",
                        },
                        {
                            "address": "192.168.2.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4",
                        },
                    ],
                }
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    _multi_ip_netjson = {
        "interfaces": [
            {
                "name": "eth0.1",
                "type": "ethernet",
                "autostart": True,
                "addresses": [
                    {
                        "address": "192.168.1.2",
                        "gateway": "192.168.1.1",
                        "mask": 24,
                        "proto": "static",
                        "family": "ipv4",
                    },
                    {
                        "address": "192.168.2.3",
                        "mask": 24,
                        "proto": "static",
                        "family": "ipv4",
                    },
                    {
                        "address": "fd87::2",
                        "gateway": "fd87::1",
                        "mask": 64,
                        "proto": "static",
                        "family": "ipv6",
                    },
                    {
                        "address": "fd87::3",
                        "mask": 64,
                        "proto": "static",
                        "family": "ipv6",
                    },
                ],
            }
        ]
    }

    _multi_ip_uci = """package network

config interface 'eth0_1'
    option auto '1'
    option gateway '192.168.1.1'
    option ifname 'eth0.1'
    list ip6addr 'fd87::2/64'
    list ip6addr 'fd87::3/64'
    option ip6gw 'fd87::1'
    list ipaddr '192.168.1.2/24'
    list ipaddr '192.168.2.3/24'
    option proto 'static'
"""

    def test_render_multiple_ip(self):
        o = OpenWrt(self._multi_ip_netjson)
        expected = self._tabs(self._multi_ip_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_multiple_ip(self):
        o = OpenWrt(native=self._multi_ip_uci)
        self.assertEqual(o.config, self._multi_ip_netjson)

    def test_render_single_ipv6(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "addresses": [
                            {
                                "address": "fd87::2",
                                "mask": 64,
                                "proto": "static",
                                "family": "ipv6",
                            }
                        ],
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option ip6addr 'fd87::2/64'
    option proto 'static'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_render_dhcp(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "addresses": [{"proto": "dhcp", "family": "ipv4"}],
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'dhcp'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_dhcp(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'dhcp'
"""
        )
        expected = {
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [{"proto": "dhcp", "family": "ipv4"}],
                }
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_parse_dhcpv6(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'dhcpv6'
"""
        )
        expected = {
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [{"proto": "dhcp", "family": "ipv6"}],
                }
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_render_multiple_dhcp(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "addresses": [
                            {"proto": "dhcp", "family": "ipv4"},
                            {"proto": "dhcp", "family": "ipv6"},
                        ],
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'dhcp'

config interface 'eth0_2'
    option ifname 'eth0'
    option proto 'dhcpv6'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_multiple_dhcp(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'dhcp'

config interface 'eth0_2'
    option ifname 'eth0'
    option proto 'dhcpv6'
"""
        )
        expected = {
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [{"proto": "dhcp", "family": "ipv4"}],
                },
                {
                    "name": "eth0",
                    "network": "eth0_2",
                    "type": "ethernet",
                    "addresses": [{"proto": "dhcp", "family": "ipv6"}],
                },
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_render_multiple_ip_and_dhcp(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "addresses": [
                            {"proto": "dhcp", "family": "ipv4"},
                            {
                                "address": "192.168.1.1",
                                "mask": 24,
                                "proto": "static",
                                "family": "ipv4",
                            },
                            {
                                "address": "192.168.2.1",
                                "mask": 24,
                                "proto": "static",
                                "family": "ipv4",
                            },
                        ],
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    list ipaddr '192.168.1.1/24'
    list ipaddr '192.168.2.1/24'
    option proto 'static'

config interface 'eth0_2'
    option ifname 'eth0'
    option proto 'dhcp'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_multiple_ip_and_dhcp(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    list ipaddr '192.168.1.1/24'
    list ipaddr '192.168.2.1/24'
    option proto 'static'

config interface 'eth0_2'
    option ifname 'eth0'
    option proto 'dhcp'
"""
        )
        expected = {
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "address": "192.168.1.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4",
                        },
                        {
                            "address": "192.168.2.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4",
                        },
                    ],
                },
                {
                    "name": "eth0",
                    "network": "eth0_2",
                    "type": "ethernet",
                    "addresses": [{"proto": "dhcp", "family": "ipv4"}],
                },
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_render_custom_proto(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "ppp0",
                        "type": "other",
                        "proto": "ppp",
                        "device": "/dev/usb/modem1",
                        "username": "user1",
                        "password": "pwd0123",
                        "keepalive": 3,
                        "ipv6": True,
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'ppp0'
    option device '/dev/usb/modem1'
    option ifname 'ppp0'
    option ipv6 '1'
    option keepalive '3'
    option password 'pwd0123'
    option proto 'ppp'
    option username 'user1'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_custom_proto(self):
        native = self._tabs(
            """package network

config interface 'custom_if0'
    option device '/dev/usb/modem1'
    option ifname 'custom_if0'
    option ipv6 '1'
    option keepalive '3'
    option proto 'custom'
"""
        )
        expected = {
            "interfaces": [
                {
                    "name": "custom_if0",
                    "type": "other",
                    "proto": "custom",
                    "device": "/dev/usb/modem1",
                    "keepalive": '3',
                    "ipv6": '1',
                }
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_render_interface_disabled(self):
        o = OpenWrt(
            {"interfaces": [{"name": "eth0", "type": "ethernet", "disabled": True}]}
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    option enabled '0'
    option ifname 'eth0'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_interface_disabled(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option enabled '0'
    option ifname 'eth0'
    option proto 'none'
"""
        )
        expected = {
            "interfaces": [{"name": "eth0", "type": "ethernet", "disabled": True}]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_render_interface_custom_attrs(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "mobile0",
                        "type": "other",
                        "mtu": 1400,
                        "custom_attr": "yes",
                        "empty": "",
                        "proto": "3g",
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'mobile0'
    option custom_attr 'yes'
    option ifname 'mobile0'
    option mtu '1400'
    option proto '3g'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_interface_custom_attrs(self):
        native = self._tabs(
            """package network

config interface 'mobile0'
    option custom_attr 'yes'
    option ifname 'mobile0'
    option mtu '1400'
    option proto 'exotic'
"""
        )
        expected = {
            "interfaces": [
                {
                    "name": "mobile0",
                    "type": "other",
                    "mtu": 1400,
                    "custom_attr": "yes",
                    "proto": "exotic",
                }
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    _simple_bridge_netjson = {
        "interfaces": [
            {"name": "eth0", "type": "ethernet"},
            {"name": "eth1", "type": "ethernet"},
            {
                "network": "lan",
                "name": "br-lan",
                "type": "bridge",
                "bridge_members": ["eth0", "eth1"],
            },
        ]
    }
    _simple_bridge_uci = """package network

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
"""

    def test_render_simple_bridge(self):
        o = OpenWrt(self._simple_bridge_netjson)
        expected = self._tabs(self._simple_bridge_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_simple_bridge(self):
        native = self._tabs(self._simple_bridge_uci)
        o = OpenWrt(native=native)
        self.assertEqual(o.config, self._simple_bridge_netjson)

    _complex_bridge_netjson = {
        "interfaces": [
            {"name": "eth0", "type": "ethernet"},
            {"name": "eth1", "type": "ethernet"},
            {
                "name": "lan",
                "network": "lan",
                "type": "bridge",
                "stp": True,
                "bridge_members": ["eth0", "eth1"],
                "addresses": [
                    {
                        "address": "192.168.1.1",
                        "mask": 24,
                        "proto": "static",
                        "family": "ipv4",
                    },
                    {
                        "address": "10.0.0.1",
                        "gateway": "10.0.0.10",
                        "mask": 24,
                        "proto": "static",
                        "family": "ipv4",
                    },
                    {"proto": "dhcp", "family": "ipv4"},
                ],
            },
        ]
    }

    _complex_bridge_uci = """package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'none'

config interface 'eth1'
    option ifname 'eth1'
    option proto 'none'

config interface 'lan'
    option gateway '10.0.0.10'
    option ifname 'eth0 eth1'
    list ipaddr '192.168.1.1/24'
    list ipaddr '10.0.0.1/24'
    option proto 'static'
    option stp '1'
    option type 'bridge'

config interface 'lan_2'
    option ifname 'br-lan'
    option proto 'dhcp'
"""

    def test_render_complex_bridge(self):
        o = OpenWrt(self._complex_bridge_netjson)
        self.assertEqual(o.render(), self._tabs(self._complex_bridge_uci))

    def test_parse_complex_bridge(self):
        o = OpenWrt(native=self._tabs(self._complex_bridge_uci))
        # performed test is slightly asymmetric in order to
        # increase code coverage using less lines of code
        netjson = deepcopy(self._complex_bridge_netjson)
        netjson['interfaces'][2]['name'] = 'br-lan'
        del netjson['interfaces'][2]['addresses'][2]
        netjson['interfaces'].append(
            {
                "name": "br-lan",
                "network": "lan_2",
                "type": "ethernet",
                "addresses": [{"proto": "dhcp", "family": "ipv4"}],
            }
        )
        self.assertEqual(o.config, netjson)

    def test_render_empty_bridge(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "network": "lan",
                        "name": "br-lan",
                        "type": "bridge",
                        "bridge_members": [],
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'lan'
    option bridge_empty '1'
    option proto 'none'
    option type 'bridge'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_empty_bridge(self):
        native = self._tabs(
            """package network

config interface 'lan'
    option bridge_empty '1'
    option proto 'none'
    option type 'bridge'
"""
        )
        expected = {
            "interfaces": [
                {
                    "network": "lan",
                    "name": "br-lan",
                    "type": "bridge",
                    "bridge_members": [],
                }
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_bridge_members_schema(self):
        o = OpenWrt({"interfaces": [{"name": "lan", "type": "bridge"}]})
        with self.assertRaises(ValidationError):
            o.validate()
        o.config['interfaces'][0]['bridge_members'] = [3]
        with self.assertRaises(ValidationError):
            o.validate()
        # ensure fix works
        o.config['interfaces'][0]['bridge_members'] = ['eth0', 'wlan0']
        o.validate()

    def test_bridge_members_pattern(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {"name": "lan", "type": "bridge", "bridge_members": ["eth 0"]}
                ]
            }
        )
        with self.assertRaises(ValidationError):
            o.validate()
        # ensure fix works
        o.config['interfaces'][0]['bridge_members'][0] = 'e-t_h@=0.1'
        o.validate()

    def test_bridge_members_unique(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "lan",
                        "type": "bridge",
                        "bridge_members": ["eth0", "eth0"],
                    }
                ]
            }
        )
        with self.assertRaises(ValidationError):
            o.validate()
        # ensure fix works
        o.config['interfaces'][0]['bridge_members'][0] = 'eth1'
        o.validate()

    def test_render_dns(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "addresses": [
                            {
                                "address": "192.168.1.1",
                                "mask": 24,
                                "proto": "static",
                                "family": "ipv4",
                            }
                        ],
                    }
                ],
                "dns_servers": ["10.11.12.13", "8.8.8.8"],
                "dns_search": ["netjson.org", "openwisp.org"],
            }
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    option dns '10.11.12.13 8.8.8.8'
    option dns_search 'netjson.org openwisp.org'
    option ifname 'eth0'
    option ipaddr '192.168.1.1'
    option netmask '255.255.255.0'
    option proto 'static'
"""
        )
        self.assertEqual(o.render(), expected)

    _dns_netjson = {
        "interfaces": [
            {
                "name": "eth0",
                "type": "ethernet",
                "addresses": [
                    {
                        "address": "192.168.1.1",
                        "mask": 24,
                        "proto": "static",
                        "family": "ipv4",
                    }
                ],
            }
        ],
        "dns_servers": ["10.11.12.13", "8.8.8.8"],
        "dns_search": ["netjson.org", "openwisp.org"],
    }

    def test_parse_dns(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option dns '10.11.12.13 8.8.8.8'
    option dns_search 'netjson.org openwisp.org'
    option ifname 'eth0'
    option ipaddr '192.168.1.1'
    option netmask '255.255.255.0'
    option proto 'static'
"""
        )
        o = OpenWrt(native=native)
        self.assertEqual(o.config, self._dns_netjson)

    def test_parse_dns_list(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    list dns '10.11.12.13'
    list dns '8.8.8.8'
    list dns_search 'netjson.org'
    list dns_search 'openwisp.org'
    option ifname 'eth0'
    option ipaddr '192.168.1.1'
    option netmask '255.255.255.0'
    option proto 'static'
"""
        )
        o = OpenWrt(native=native)
        self.assertEqual(o.config, self._dns_netjson)

    def test_dns_dhcpv4_ignored(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "addresses": [{"proto": "dhcp", "family": "ipv4"}],
                    }
                ],
                "dns_servers": ["10.11.12.13", "8.8.8.8"],
                "dns_search": ["netjson.org", "openwisp.org"],
            }
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    option dns_search 'netjson.org openwisp.org'
    option ifname 'eth0'
    option proto 'dhcp'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_dns_dhcpv6_ignored(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "addresses": [{"proto": "dhcp", "family": "ipv6"}],
                    }
                ],
                "dns_servers": ["10.11.12.13", "8.8.8.8"],
                "dns_search": ["netjson.org", "openwisp.org"],
            }
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    option dns_search 'netjson.org openwisp.org'
    option ifname 'eth0'
    option proto 'dhcpv6'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_dhcp_ignored_proto_none(self):
        o = OpenWrt(
            {
                "interfaces": [{"name": "eth0", "type": "ethernet"}],
                "dns_servers": ["10.11.12.13", "8.8.8.8"],
                "dns_search": ["netjson.org", "openwisp.org"],
            }
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_empty_interface(self):
        o = OpenWrt({"interfaces": [{"name": "eth0", "type": "ethernet"}]})
        expected = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_ifname_length(self):
        o = OpenWrt({"interfaces": [{"name": "ifname0123456789", "type": "ethernet"}]})
        with self.assertRaises(ValidationError):
            o.validate()
        # ensure fix works
        o.config['interfaces'][0]['name'] = 'ifname0'
        o.validate()

    def test_ifname_pattern(self):
        o = OpenWrt({"interfaces": [{"name": "eth 0", "type": "ethernet"}]})
        with self.assertRaises(ValidationError):
            o.validate()
        # ensure fix works
        o.config['interfaces'][0]['name'] = 'e-t_h@=0.1'
        o.validate()

    def test_network_maxlength(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "eth0",
                        "network": "lan0123456789012345",
                        "type": "ethernet",
                    }
                ]
            }
        )
        with self.assertRaises(ValidationError):
            o.validate()
        # ensure fix works
        o.config['interfaces'][0]['network'] = 'lan'
        o.validate()

    def test_network_pattern(self):
        o = OpenWrt(
            {"interfaces": [{"name": "eth0", "network": "lan 0", "type": "ethernet"}]}
        )
        with self.assertRaises(ValidationError):
            o.validate()
        o.config['interfaces'][0]['network'] = 'lan/0'
        with self.assertRaises(ValidationError):
            o.validate()
        # ensure fix works
        o.config['interfaces'][0]['network'] = 'lan'
        o.validate()

    def test_render_network_attribute(self):
        o = OpenWrt(
            {
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
                                "family": "ipv4",
                            },
                            {"proto": "dhcp", "family": "ipv4"},
                        ],
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'lan'
    option ifname 'eth0'
    option ipaddr '192.168.1.1'
    option netmask '255.255.255.0'
    option proto 'static'

config interface 'lan_2'
    option ifname 'eth0'
    option proto 'dhcp'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_network_attribute(self):
        native = self._tabs(
            """package network

config interface 'lan'
    option ifname 'eth0'
    option proto 'static'
"""
        )
        expected = {
            "interfaces": [{"name": "eth0", "network": "lan", "type": "ethernet"}]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_network_dot_conversion(self):
        o = OpenWrt(
            {"interfaces": [{"name": "eth0.1", "type": "ethernet", "network": "lan.1"}]}
        )
        expected = self._tabs(
            """package network

config interface 'lan_1'
    option ifname 'eth0.1'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_network_dash_conversion(self):
        o = OpenWrt(
            {"interfaces": [{"name": "eth-0", "type": "ethernet", "network": "lan-0"}]}
        )
        expected = self._tabs(
            """package network

config interface 'lan_0'
    option ifname 'eth-0'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_mac_address_format(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {"name": "eth0", "type": "ethernet", "mac": "00:11:22:33:44:55"}
                ]
            }
        )
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
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "type": "bridge",
                        "network": "lan",
                        "addresses": [],
                        "name": "br-lan",
                        "bridge_members": ["eth0", "eth1"],
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'lan'
    option ifname 'eth0 eth1'
    option proto 'none'
    option type 'bridge'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_render_interface_list_option(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "ip6class": ["wan6", "backbone"],
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    list ip6class 'wan6'
    list ip6class 'backbone'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_render_address_list_option(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "addresses": [
                            {"proto": "dhcp", "family": "ipv4", "reqopts": ["43", "54"]}
                        ],
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'dhcp'
    list reqopts '43'
    list reqopts '54'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_interface_list(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    list ip6class 'wan6'
    list ip6class 'backbone'
    option proto 'none'
"""
        )
        expected = {
            "interfaces": [
                {"name": "eth0", "type": "ethernet", "ip6class": ["wan6", "backbone"]}
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_dns_override(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {"name": "eth0", "type": "ethernet", "dns": ["8.8.8.8", "8.8.4.4"]}
                ],
                "dns_servers": ["192.168.3.1", "192.168.3.2"],
            }
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    list dns '8.8.8.8'
    list dns '8.8.4.4'
    option ifname 'eth0'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_dns_search_override(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "dns_search": ["openwisp.org", "netjson.org"],
                    }
                ],
                "dns_search": ["domain.com"],
            }
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    list dns_search 'openwisp.org'
    list dns_search 'netjson.org'
    option ifname 'eth0'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_spanning_tree(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "br-lan",
                        "type": "bridge",
                        "stp": True,
                        "bridge_members": ["eth0", "eth1"],
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'br_lan'
    option ifname 'eth0 eth1'
    option proto 'none'
    option stp '1'
    option type 'bridge'
"""
        )
        self.assertEqual(o.render(), expected)
        # try entering an invalid value
        o.config['interfaces'][0]['stp'] = 'wrong'
        with self.assertRaises(ValidationError):
            o.validate()

    def test_igmp(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {
                        "name": "br-lan",
                        "type": "bridge",
                        "igmp_snooping": True,
                        "bridge_members": ["eth0", "eth1"],
                    }
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'br_lan'
    option ifname 'eth0 eth1'
    option igmp_snooping '1'
    option proto 'none'
    option type 'bridge'
"""
        )
        self.assertEqual(o.render(), expected)
        # try entering an invalid value
        o.config['interfaces'][0]['igmp_snooping'] = 'wrong'
        with self.assertRaises(ValidationError):
            o.validate()

    def test_render_autostart_false(self):
        o = OpenWrt(
            {"interfaces": [{"name": "eth0", "type": "ethernet", "autostart": False}]}
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    option auto '0'
    option ifname 'eth0'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_autostart_false(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option auto '0'
    option ifname 'eth0'
    option proto 'none'
"""
        )
        expected = {
            "interfaces": [{"name": "eth0", "type": "ethernet", "autostart": False}]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_render_macaddr(self):
        o = OpenWrt(
            {
                "interfaces": [
                    {"name": "eth0", "type": "ethernet", "mac": "E8:94:F6:33:8C:00"}
                ]
            }
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option macaddr 'E8:94:F6:33:8C:00'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_macaddr(self):
        native = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option macaddr 'E8:94:F6:33:8C:00'
    option proto 'none'
"""
        )
        expected = {
            "interfaces": [
                {"name": "eth0", "type": "ethernet", "mac": "E8:94:F6:33:8C:00"}
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_interface_disabled_bug(self):
        """
        see https://github.com/openwisp/netjsonconfig/issues/57
        """
        o = OpenWrt(
            {"interfaces": [{"type": "ethernet", "name": "eth0", "disabled": False}]}
        )
        self.assertNotIn("disabled '0'", o.render())
        self.assertIn("enabled '1'", o.render())

    def test_empty_network(self):
        o = OpenWrt(
            {"interfaces": [{"name": "eth0", "type": "ethernet", "network": ""}]}
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_empty_dns(self):
        o = OpenWrt(
            {
                "interfaces": [{"name": "eth0", "type": "ethernet"}],
                "dns_servers": [],
                "dns_search": [],
            }
        )
        expected = self._tabs(
            """package network

config interface 'eth0'
    option ifname 'eth0'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)
