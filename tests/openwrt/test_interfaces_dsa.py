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

config device 'device_lo'
    option name 'lo'

config interface 'lo'
    option device 'lo'
    option ipaddr '127.0.0.1'
    option netmask '255.0.0.0'
    option proto 'static'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_loopback(self):
        native = self._tabs(
            """package network

config device 'device_lo'
    option name 'lo'

config interface 'lo'
    option device 'lo'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
"""
        )
        expected = {"interfaces": [{"name": "eth0", "type": "ethernet"}]}
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_parse_incorrect_ipaddr(self):
        native = self._tabs(
            """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option ipaddr '/'
"""
        )
        expected = {"interfaces": [{"name": "eth0", "type": "ethernet"}]}
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_parse_incorrect_ipaddr_netmask(self):
        native = self._tabs(
            """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option ipaddr '192.168.1.1'
    option proto 'static'
"""
        )
        o = OpenWrt(native=native)
        self.assertEqual(o.config, self._eth0_32)

    def test_parse_forgotten_ipv4_mask(self):
        native = self._tabs(
            """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option ipaddr '192.168.1.1/'
    option proto 'static'
"""
        )
        o = OpenWrt(native=native)
        self.assertEqual(o.config, self._eth0_32)

    def test_parse_missing_ipv4_mask_list(self):
        native = self._tabs(
            """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    list ipaddr '192.168.1.1'
    option proto 'static'
"""
        )
        o = OpenWrt(native=native)
        self.assertEqual(o.config, self._eth0_32)

    def test_parse_missing_ipv6_mask_list(self):
        native = self._tabs(
            """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option ip6addr '2aa1:4aaa:2aaa:1d::5/64'
    option proto 'static'
"""
        )
        o = OpenWrt(native=native)
        self.assertEqual(o.config, self._eth0_64)

    def test_parse_ipv4_list(self):
        native = self._tabs(
            """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
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

config device 'device_eth0_1'
    option name 'eth0.1'

config interface 'eth0_1'
    option auto '1'
    option device 'eth0.1'
    option gateway '192.168.1.1'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option proto 'dhcp'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_dhcp(self):
        native = self._tabs(
            """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option proto 'dhcp'

config interface 'eth0_2'
    option device 'eth0'
    option proto 'dhcpv6'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_multiple_dhcp(self):
        native = self._tabs(
            """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option proto 'dhcp'

config interface 'eth0_2'
    option device 'eth0'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    list ipaddr '192.168.1.1/24'
    list ipaddr '192.168.2.1/24'
    option proto 'static'

config interface 'eth0_2'
    option device 'eth0'
    option proto 'dhcp'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_multiple_ip_and_dhcp(self):
        native = self._tabs(
            """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    list ipaddr '192.168.1.1/24'
    list ipaddr '192.168.2.1/24'
    option proto 'static'

config interface 'eth0_2'
    option device 'eth0'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option enabled '0'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_interface_disabled(self):
        native = self._tabs(
            """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option enabled '0'
    option device 'eth0'
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

config device 'device_mobile0'
    option name 'mobile0'

config interface 'mobile0'
    option custom_attr 'yes'
    option device 'mobile0'
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
                "mac": "E8:94:F6:33:8C:00",
            },
        ]
    }
    _simple_bridge_uci = """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option proto 'none'

config device 'device_eth1'
    option name 'eth1'

config interface 'eth1'
    option device 'eth1'
    option proto 'none'

config device 'device_lan'
    option macaddr 'E8:94:F6:33:8C:00'
    option name 'br-lan'
    list ports 'eth0'
    list ports 'eth1'
    option type 'bridge'

config interface 'lan'
    option device 'br-lan'
    option proto 'none'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option proto 'none'

config device 'device_eth1'
    option name 'eth1'

config interface 'eth1'
    option device 'eth1'
    option proto 'none'

config device 'device_lan'
    option name 'br-lan'
    list ports 'eth0'
    list ports 'eth1'
    option stp '1'
    option type 'bridge'

config interface 'lan'
    option device 'br-lan'
    option gateway '10.0.0.10'
    list ipaddr '192.168.1.1/24'
    list ipaddr '10.0.0.1/24'
    option proto 'static'

config interface 'lan_2'
    option device 'br-lan'
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

config device 'device_lan'
    option bridge_empty '1'
    option name 'br-lan'
    option type 'bridge'

config interface 'lan'
    option device 'br-lan'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_empty_bridge(self):
        native = self._tabs(
            """package network

config device 'device_lan'
    option bridge_empty '1'
    option name 'br-lan'
    option type 'bridge'

config interface 'lan'
    option device 'br-lan'
    option proto 'none'
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

    _bridge_21_bridge_uci = """package network

config device 'device_eth0'
    option name 'eth0'

config device 'device_eth1'
    option name 'eth1'

config interface 'eth0'
    option device 'eth0'
    option proto 'none'

config interface 'eth1'
    option device 'eth1'
    option proto 'none'

config device 'device_lan'
    option type 'bridge'
    option name 'lan'
    list ports 'eth0'
    list ports 'eth1'
    option macaddr 'E8:94:F6:33:8C:00'

config interface 'lan'
    option device 'lan'
    option proto 'none'
"""

    def test_parse_bridge_21(self):
        o = OpenWrt(native=self._bridge_21_bridge_uci)
        self.assertEqual(o.config, self._simple_bridge_netjson)

    _l2_options_bridge_netjson = {
        "interfaces": [
            {"name": "eth0", "type": "ethernet"},
            {"name": "eth1", "type": "ethernet"},
            {
                "network": "lan",
                "name": "br-lan",
                "type": "bridge",
                "bridge_members": ["eth0", "eth1"],
                "mac": "E8:94:F6:33:8C:00",
                'rpfilter': 'strict',
                'txqueuelen': 1000,
                'neighreachabletime': 30000,
                'neighgcstaletime': 3000,
                'neighlocktime': 3000,
                'igmpversion': 2,
                'mldversion': 2,
                'promisc': True,
                'acceptlocal': True,
                'sendredirects': True,
                'multicast': True,
            },
        ]
    }
    _l2_options_bridge_uci = """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option proto 'none'

config device 'device_eth1'
    option name 'eth1'

config interface 'eth1'
    option device 'eth1'
    option proto 'none'

config device 'device_lan'
    option acceptlocal '1'
    option igmpversion '2'
    option macaddr 'E8:94:F6:33:8C:00'
    option mldversion '2'
    option multicast '1'
    option name 'br-lan'
    option neighgcstaletime '3000'
    option neighlocktime '3000'
    option neighreachabletime '30000'
    list ports 'eth0'
    list ports 'eth1'
    option promisc '1'
    option rpfilter 'strict'
    option sendredirects '1'
    option txqueuelen '1000'
    option type 'bridge'

config interface 'lan'
    option device 'br-lan'
    option proto 'none'
"""

    def test_render_l2_options_bridge(self):
        o = OpenWrt(self._l2_options_bridge_netjson)
        expected = self._tabs(self._l2_options_bridge_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_l2_options_bridge(self):
        o = OpenWrt(native=self._l2_options_bridge_uci)
        self.assertEqual(o.config, self._l2_options_bridge_netjson)

    _l2_options_interface_netjson = {
        "interfaces": [
            {
                "name": "wan",
                "type": "ethernet",
                "mac": "00:11:22:33:44:55",
                "addresses": [{"proto": "dhcp", "family": "ipv4"}],
            }
        ]
    }
    _l2_options_interface_uci = """package network

config device 'device_wan'
    option macaddr '00:11:22:33:44:55'
    option name 'wan'

config interface 'wan'
    option device 'wan'
    option proto 'dhcp'
"""

    def test_render_l2_options_interface(self):
        o = OpenWrt(self._l2_options_interface_netjson)
        expected = self._tabs(self._l2_options_interface_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_l2_options_interface(self):
        o = OpenWrt(native=self._l2_options_interface_uci)
        self.assertEqual(o.config, self._l2_options_interface_netjson)

    _vlan_filtering_bridge_netjson = {
        "interfaces": [
            {
                "type": "bridge",
                "bridge_members": ["lan1", "lan2", "lan3"],
                "name": "br-lan",
                "vlan_filtering": [
                    {
                        "vlan": 1,
                        "ports": [
                            {"ifname": "lan1", "tagging": "t", "primary_vid": True},
                            {"ifname": "lan2", "tagging": "t"},
                        ],
                    },
                    {
                        "vlan": 2,
                        "ports": [
                            {"ifname": "lan1", "tagging": "t", "primary_vid": False},
                            {"ifname": "lan3", "tagging": "u", "primary_vid": True},
                        ],
                    },
                ],
            }
        ]
    }

    _vlan_filtering_bridge_uci = """package network

config device 'device_br_lan'
    option name 'br-lan'
    list ports 'lan1'
    list ports 'lan2'
    list ports 'lan3'
    option type 'bridge'
    option vlan_filtering '1'

config bridge-vlan 'vlan_br_lan_1'
    option device 'br-lan'
    list ports 'lan1:t*'
    list ports 'lan2:t'
    option vlan '1'

config bridge-vlan 'vlan_br_lan_2'
    option device 'br-lan'
    list ports 'lan1:t'
    list ports 'lan3:u*'
    option vlan '2'

config interface 'vlan_br_lan_1'
    option device 'br-lan.1'
    option proto 'none'

config interface 'vlan_br_lan_2'
    option device 'br-lan.2'
    option proto 'none'

config interface 'br_lan'
    option device 'br-lan'
    option proto 'none'
"""

    def test_render_bridge_vlan_filtering(self):
        o = OpenWrt(self._vlan_filtering_bridge_netjson)
        self.assertEqual(self._tabs(self._vlan_filtering_bridge_uci), o.render())

        with self.subTest('Test setting PVID on same port on different VLANS'):
            netjson = deepcopy(self._vlan_filtering_bridge_netjson)
            netjson['interfaces'][0]['vlan_filtering'][1]['ports'][0][
                'primary_vid'
            ] = True
            with self.assertRaises(ValidationError) as error:
                OpenWrt(netjson).validate()
            self.assertEqual(
                error.exception.message,
                (
                    'Invalid configuration triggered by "#/interfaces/0"'
                    ' says: Primary VID can be set only one VLAN for a port.'
                ),
            )

    def test_parse_bridge_vlan_filtering(self):
        o = OpenWrt(native=self._vlan_filtering_bridge_uci)
        expected = deepcopy(self._vlan_filtering_bridge_netjson)
        expected['interfaces'][0]['vlan_filtering'][0]['ports'][1][
            'primary_vid'
        ] = False
        self.assertEqual(o.config, expected)

    _vlan_filtering_bridge_override_netjson = {
        "interfaces": [
            {
                "type": "bridge",
                "bridge_members": ["lan1", "lan2", "lan3"],
                "name": "br-lan",
                "vlan_filtering": [
                    {
                        "vlan": 1,
                        "ports": [
                            {"ifname": "lan1", "tagging": "t", "primary_vid": False},
                            {"ifname": "lan2", "tagging": "u", "primary_vid": False},
                        ],
                    }
                ],
            },
            {
                "type": "ethernet",
                "name": "br-lan.1",
                "mtu": 1500,
                "mac": "61:4A:A0:D7:3F:0E",
                "addresses": [
                    {
                        "proto": "static",
                        "family": "ipv4",
                        "address": "192.168.2.1",
                        "mask": 24,
                    }
                ],
            },
        ]
    }
    _vlan_filtering_bridge_override_uci = """package network

config device 'device_br_lan'
    option name 'br-lan'
    list ports 'lan1'
    list ports 'lan2'
    list ports 'lan3'
    option type 'bridge'
    option vlan_filtering '1'

config bridge-vlan 'vlan_br_lan_1'
    option device 'br-lan'
    list ports 'lan1:t'
    list ports 'lan2:u'
    option vlan '1'

config interface 'vlan_br_lan_1'
    option device 'br-lan.1'
    option proto 'none'

config interface 'br_lan'
    option device 'br-lan'
    option proto 'none'

config interface 'br_lan_1'
    option device 'br-lan.1'
    option ipaddr '192.168.2.1'
    option netmask '255.255.255.0'
    option proto 'static'
"""

    def test_render_bridge_vlan_filtering_override_interface(self):
        o = OpenWrt(self._vlan_filtering_bridge_override_netjson)
        self.assertEqual(
            self._tabs(self._vlan_filtering_bridge_override_uci), o.render()
        )

    def test_parse_bridge_vlan_filtering_override_interface(self):
        o = OpenWrt(native=self._vlan_filtering_bridge_override_uci)
        expected = deepcopy(self._vlan_filtering_bridge_override_netjson)
        del expected['interfaces'][1]['mtu']
        del expected['interfaces'][1]['mac']
        self.assertEqual(o.config, expected)

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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option dns '10.11.12.13 8.8.8.8'
    option dns_search 'netjson.org openwisp.org'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option dns '10.11.12.13 8.8.8.8'
    option dns_search 'netjson.org openwisp.org'
    option device 'eth0'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    list dns '10.11.12.13'
    list dns '8.8.8.8'
    list dns_search 'netjson.org'
    list dns_search 'openwisp.org'
    option device 'eth0'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option dns_search 'netjson.org openwisp.org'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option dns_search 'netjson.org openwisp.org'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_empty_interface(self):
        o = OpenWrt({"interfaces": [{"name": "eth0", "type": "ethernet"}]})
        expected = self._tabs(
            """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
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

config device 'device_lan'
    option name 'eth0'

config interface 'lan'
    option device 'eth0'
    option ipaddr '192.168.1.1'
    option netmask '255.255.255.0'
    option proto 'static'

config interface 'lan_2'
    option device 'eth0'
    option proto 'dhcp'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_network_attribute(self):
        native = self._tabs(
            """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'lan'
    option device 'eth0'
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

config device 'device_lan_1'
    option name 'eth0.1'

config interface 'lan_1'
    option device 'eth0.1'
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

config device 'device_lan_0'
    option name 'eth-0'

config interface 'lan_0'
    option device 'eth-0'
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

config device 'device_lan'
    option name 'br-lan'
    list ports 'eth0'
    list ports 'eth1'
    option type 'bridge'

config interface 'lan'
    option device 'br-lan'
    option proto 'none'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option proto 'dhcp'
    list reqopts '43'
    list reqopts '54'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_interface_list(self):
        native = self._tabs(
            """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    list dns '8.8.8.8'
    list dns '8.8.4.4'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    list dns_search 'openwisp.org'
    list dns_search 'netjson.org'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    _spanning_tree_bridge_netjson = {
        "interfaces": [
            {
                "name": "br-lan",
                "type": "bridge",
                "stp": True,
                "hello_time": 2,
                "forward_delay": 15,
                "max_age": 20,
                "priority": 32767,
                "bridge_members": ["eth0", "eth1"],
            }
        ]
    }
    _spanning_tree_bridge_uci = """package network

config device 'device_br_lan'
    option forward_delay '15'
    option hello_time '2'
    option max_age '20'
    option name 'br-lan'
    list ports 'eth0'
    list ports 'eth1'
    option priority '32767'
    option stp '1'
    option type 'bridge'

config interface 'br_lan'
    option device 'br-lan'
    option proto 'none'
"""

    def test_render_spanning_tree_bridge(self):
        o = OpenWrt(self._spanning_tree_bridge_netjson)
        expected = self._tabs(self._spanning_tree_bridge_uci)
        self.assertEqual(o.render(), expected)
        # try entering an invalid value
        o.config['interfaces'][0]['stp'] = 'wrong'
        with self.assertRaises(ValidationError):
            o.validate()

        stp_disabled_netjson = deepcopy(self._spanning_tree_bridge_netjson)
        stp_disabled_netjson['interfaces'][0]['stp'] = False
        self.assertNotIn('option stp \'1\'', OpenWrt(stp_disabled_netjson).render())

    def test_parse_spanning_tree_bridge(self):
        o = OpenWrt(native=self._spanning_tree_bridge_uci)
        self.assertEqual(o.config, self._spanning_tree_bridge_netjson)

        # try invalid option values
        bogus_uci = self._spanning_tree_bridge_uci.replace(
            "option forward_delay '15'", "option forward_delay 'wrong'"
        )
        o = OpenWrt(native=bogus_uci)
        self.assertNotIn('forward_delay', o.config['interfaces'][0])

    _igmp_bridge_netjson = {
        "interfaces": [
            {
                "name": "br-lan",
                "type": "bridge",
                "igmp_snooping": True,
                "multicast_querier": True,
                "query_interval": 12500,
                "query_response_interval": 1000,
                "last_member_interval": 100,
                "hash_max": 512,
                "robustness": 2,
                "bridge_members": ["eth0", "eth1"],
            }
        ]
    }
    _igmp_bridge_uci = """package network

config device 'device_br_lan'
    option hash_max '512'
    option igmp_snooping '1'
    option last_member_interval '100'
    option multicast_querier '1'
    option name 'br-lan'
    list ports 'eth0'
    list ports 'eth1'
    option query_interval '12500'
    option query_response_interval '1000'
    option robustness '2'
    option type 'bridge'

config interface 'br_lan'
    option device 'br-lan'
    option proto 'none'
"""

    def test_render_igmp_bridge(self):
        o = OpenWrt(self._igmp_bridge_netjson)
        expected = self._tabs(self._igmp_bridge_uci)
        self.assertEqual(o.render(), expected)

        # try entering an invalid value
        o.config['interfaces'][0]['igmp_snooping'] = 'wrong'
        with self.assertRaises(ValidationError):
            o.validate()

        igmp_snooping_disabled_netjson = deepcopy(self._igmp_bridge_netjson)
        igmp_snooping_disabled_netjson['interfaces'][0]['igmp_snooping'] = False
        self.assertIn(
            "option igmp_snooping '0'",
            OpenWrt(igmp_snooping_disabled_netjson).render(),
        )

    def test_parse_igmp_bridge(self):
        o = OpenWrt(native=self._igmp_bridge_uci)
        self.assertEqual(o.config, self._igmp_bridge_netjson)

        # try invalid option value
        bogus_uci = self._igmp_bridge_uci.replace(
            "option robustness '2'", "option robustness 'wrong'"
        )
        o = OpenWrt(native=bogus_uci)
        self.assertNotIn('robustness', o.config['interfaces'][0])

    def test_render_autostart_false(self):
        o = OpenWrt(
            {"interfaces": [{"name": "eth0", "type": "ethernet", "autostart": False}]}
        )
        expected = self._tabs(
            """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option auto '0'
    option device 'eth0'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_autostart_false(self):
        native = self._tabs(
            """package network

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option auto '0'
    option device 'eth0'
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

config device 'device_eth0'
    option macaddr 'E8:94:F6:33:8C:00'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    def test_parse_macaddr(self):
        native = self._tabs(
            """package network

config device 'device_eth0'
    option name 'eth0'
    option macaddr 'E8:94:F6:33:8C:00'

config interface 'eth0'
    option device 'eth0'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
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

config device 'device_eth0'
    option name 'eth0'

config interface 'eth0'
    option device 'eth0'
    option proto 'none'
"""
        )
        self.assertEqual(o.render(), expected)

    _vlan8021q_netjson = {
        "interfaces": [
            {
                "type": "8021q",
                "vid": 1,
                "name": "br-lan",
                "mac": "E8:6A:64:3E:4A:3A",
                "mtu": 1500,
                "ingress_qos_mapping": ["1:1"],
                "egress_qos_mapping": ["2:2"],
            }
        ]
    }

    _vlan8021q_uci = """package network

config device 'device_br_lan_1'
    list egress_qos_mapping '2:2'
    option ifname 'br-lan'
    list ingress_qos_mapping '1:1'
    option macaddr 'E8:6A:64:3E:4A:3A'
    option mtu '1500'
    option name 'br-lan.1'
    option type '8021q'
    option vid '1'

config interface 'vlan_br_lan_1'
    option device 'br-lan.1'
    option proto 'none'
"""

    def test_render_vlan8021q(self):
        o = OpenWrt(self._vlan8021q_netjson)
        expected = self._tabs(self._vlan8021q_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_vlan8021q(self):
        o = OpenWrt(native=self._tabs(self._vlan8021q_uci))
        expected = deepcopy(self._vlan8021q_netjson)
        expected['interfaces'][0]['network'] = 'vlan_br_lan_1'
        self.assertEqual(expected, o.config)

    _vlan8021ad_netjson = {
        "interfaces": [
            {
                "type": "8021ad",
                "vid": 6,
                "name": "eth0",
            }
        ]
    }

    _vlan8021ad_uci = """package network

config device 'device_eth0_6'
    option ifname 'eth0'
    option name 'eth0.6'
    option type '8021ad'
    option vid '6'

config interface 'vlan_eth0_6'
    option device 'eth0.6'
    option proto 'none'
"""

    def test_render_vlan8021ad(self):
        o = OpenWrt(self._vlan8021ad_netjson)
        expected = self._tabs(self._vlan8021ad_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_vlan8021ad(self):
        o = OpenWrt(native=self._tabs(self._vlan8021ad_uci))
        expected = deepcopy(self._vlan8021ad_netjson)
        expected['interfaces'][0]['network'] = 'vlan_eth0_6'
        self.assertEqual(expected, o.config)
