from unittest import skip

from .mock import ConverterTest, NetconfAirOs


class TestNetconfConverter(ConverterTest):

    backend = NetconfAirOs

    def test_netconf_key(self):
        o = self.backend({
            'interfaces': []
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netconf'], expected)

    def test_active_interface(self):
        o = self.backend({
            'interfaces': [{
                'name': 'eth0',
                'type': 'ethernet',
                }]
        })

        o.to_intermediate()

        expected = [
            {
                '1.autoip.status': 'disabled',
                '1.autoneg': 'enabled',
                '1.devname': 'eth0',
                '1.flowcontrol.tx.status': 'enabled',
                '1.flowcontrol.rx.status': 'enabled',
                '1.mtu': 1500,
                '1.status': 'enabled',
                '1.up': 'enabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netconf'], expected)

    def test_inactive_interface(self):
        o = self.backend({
            'interfaces': [
                {
                    'name': 'eth0',
                    'type': 'ethernet',
                    'disabled': True,
                }
            ]
        })
        o.to_intermediate()
        expected = [
            {
                '1.autoip.status': 'disabled',
                '1.autoneg': 'enabled',
                '1.devname': 'eth0',
                '1.flowcontrol.tx.status': 'enabled',
                '1.flowcontrol.rx.status': 'enabled',
                '1.mtu': 1500,
                '1.status': 'enabled',
                '1.up': 'disabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netconf'], expected)

    def test_vlan(self):
        o = self.backend({
            'interfaces': [
                {
                    'name': 'eth0.1',
                    'type': 'ethernet',
                }
            ],
        })
        o.to_intermediate()
        expected = [
            {
                '1.devname': 'eth0.1',
                '1.mtu': 1500,
                '1.status': 'enabled',
                '1.up': 'enabled',
                '1.autoip.status': 'disabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netconf'], expected)

    def test_management_vlan(self):
        o = self.backend({
            'interfaces': [
                {
                    'name': 'eth0.1',
                    'type': 'ethernet',
                    'addresses': [
                        {
                            'address': '192.168.1.20',
                            'family': 'ipv4',
                            'management': True,
                            'mask': 24,
                            'proto': 'static',
                        }
                    ]
                }
            ],
        })
        o.to_intermediate()
        expected = [
            {
                '1.devname': 'eth0.1',
                '1.ip': '192.168.1.20',
                '1.netmask': '255.255.255.0',
                '1.mtu': 1500,
                '1.role': 'mlan',
                '1.status': 'enabled',
                '1.up': 'enabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netconf'], expected)

    def test_access_point(self):
        o = self.backend({
            'interfaces': [
                {
                    'name': 'wlan0',
                    'type': 'wireless',
                    'wireless': {
                        'radio': 'ath0',
                        'mode': 'access_point',
                        'ssid': 'ap-ssid-example',
                    }
                }
            ],
        })
        o.to_intermediate()
        expected = [
            {
                '1.devname': 'ath0',
                '1.mtu': 1500,
                '1.status': 'enabled',
                '1.up': 'enabled',
                '1.autoip.status': 'disabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netconf'], expected)

    def test_station(self):
        o = self.backend({
            'interfaces': [
                {
                    'name': 'wlan0',
                    'type': 'wireless',
                    'wireless': {
                        'radio': 'ath0',
                        'mode': 'station',
                        'bssid': '00:11:22:33:44:55',
                        'ssid': 'ap-ssid-example',
                    }
                }
            ],
        })
        o.to_intermediate()
        expected = [
            {
                '1.devname': 'ath0',
                '1.status': 'enabled',
                '1.up': 'enabled',
                '1.mtu': 1500,
                '1.autoip.status': 'disabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netconf'], expected)

    @skip("Airos does not support ``adhoc`` mode")
    def test_adhoc(self):
        o = self.backend({
            'interfaces': [
                {
                    'name': 'wlan0',
                    'type': 'wireless',
                    'wireless': {
                        'radio': 'ath0',
                        'mode': 'adhoc',
                        'ssid': 'ap-ssid-example',
                    }
                }
            ],
        })
        o.to_intermediate()
        expected = [
            {
                '1.devname': 'ath0',
                '1.status': 'enabled',
                '1.up': 'enabled',
                '1.mtu': 1500,
                '1.autoip.status': 'disabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netconf'], expected)

    @skip("Airos does not support wds")
    def test_wds(self):
        o = self.backend({
            'interfaces': [
                {
                    'name': 'wlan0',
                    'type': 'wireless',
                    'wireless': {
                        'radio': 'ath0',
                        'mode': 'wds',
                        'ssid': 'ap-ssid-example',
                    }
                }
            ],
        })
        o.to_intermediate()
        expected = [
            {
                '1.devname': 'ath0',
                '1.mtu': 1500,
                '1.up': 'enabled',
                '1.status': 'enabled',
                '1.autoip.status': 'disabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netconf'], expected)

    @skip("Airos does not support ``monitor`` mode")
    def test_monitor(self):
        o = self.backend({
            'interfaces': [
                {
                    'name': 'wlan0',
                    'type': 'wireless',
                    'wireless': {
                        'radio': 'ath0',
                        'mode': 'monitor',
                        'ssid': 'ap-ssid-example',
                    }
                }
            ],
        })
        o.to_intermediate()
        expected = [
            {
                '1.devname': 'ath0',
                '1.status': 'enabled',
                '1.up': 'enabled',
                '1.autoip.status': 'enabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netconf'], expected)

    @skip("AirOS does not support 802.11s")
    def test_80211s(self):
        o = self.backend({
            'interfaces': [
                {
                    'name': 'wlan0',
                    'type': 'wireless',
                    'wireless': {
                        'radio': 'ath0',
                        'mode': 'access_point',
                        'protocol': '802.11s',
                        'ssid': 'ap-ssid-example',
                    }
                }
            ],
        })
        o.to_intermediate()
        expected = [
            {
                '1.devname': 'ath0',
                '1.status': 'enabled',
                '1.up': 'enabled',
                '1.autoip.status': 'disabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netconf'], expected)

    def test_bridge(self):
        o = self.backend({
            'interfaces': [
                {
                    'name': 'br0',
                    'type': 'bridge',
                    'bridge_members': [
                        'eth0',
                        'eth1',
                    ],
                }
            ],
        })
        o.to_intermediate()
        expected = [
            {
                '1.devname': 'br0',
                '1.status': 'enabled',
                '1.up': 'enabled',
                '1.mtu': 1500,
                '1.autoip.status': 'disabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netconf'], expected)

    @skip("Airos does not support virtual interfaces")
    def test_virtual(self):
        o = self.backend({
            'interfaces': [
                {
                    'name': 'veth0',
                    'type': 'virtual',
                }
            ],
        })
        o.to_intermediate()
        expected = [
            {
                '1.devname': 'veth0',
                '1.status': 'enabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netconf'], expected)

    @skip("Airos does not support ``loopback`` interface")
    def test_loopback(self):
        o = self.backend({
            'interfaces': [
                {
                    'name': 'lopp0',
                    'type': 'loopback',
                }
            ],
        })
        o.to_intermediate()
        expected = [
            {
                '1.devname': 'loop0',
                '1.status': 'enabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netconf'], expected)

    @skip("Airos does not support ``other`` interfaces")
    def test_other(self):
        o = self.backend({
            'interfaces': [
                {
                    'name': 'fancyname0',
                    'type': 'other',
                }
            ],
        })
        o.to_intermediate()
        expected = [
            {
                '1.devname': 'fancyname0',
                '1.status': 'enabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netconf'], expected)

    def test_dhcp(self):
        o = self.backend({
            'interfaces': [
                {
                    'name': 'eth0',
                    'type': 'ethernet',
                    'addresses': [
                        {
                            'proto': 'dhcp',
                            'family': 'ipv4',
                        },
                    ]
                },
            ],
        })
        o.to_intermediate()
        expected = [
            {
                '1.autoip.status': 'enabled',
                '1.autoneg': 'enabled',
                '1.devname': 'eth0',
                '1.flowcontrol.rx.status': 'enabled',
                '1.flowcontrol.tx.status': 'enabled',
                '1.mtu': 1500,
                '1.status': 'enabled',
                '1.up': 'enabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['netconf'], expected)

    def test_more_interfaces(self):
        o = self.backend({
            'interfaces': [
                {
                    'name': 'eth0',
                    'type': 'ethernet',
                },
                {
                    'name': 'wlan0',
                    'type': 'wireless',
                    'wireless': {
                        'radio': 'ath0',
                        'mode': 'station',
                        'bssid': '00:11:22:33:44:55',
                        'ssid': 'ap-ssid-example',
                    }
                },
                {
                    'name': 'br0',
                    'type': 'bridge',
                    'bridge_members': [
                        'eth0',
                        'wlan0',
                    ],
                },
                {
                    'name': 'veth0',
                    'type': 'virtual',
                },
                {
                    'name': 'loop0',
                    'type': 'loopback',
                }
            ],
        })
        o.to_intermediate()
        expected = [
            {
                '1.autoip.status': 'disabled',
                '1.autoneg': 'enabled',
                '1.devname': 'eth0',
                '1.flowcontrol.rx.status': 'enabled',
                '1.flowcontrol.tx.status': 'enabled',
                '1.mtu': 1500,
                '1.status': 'enabled',
                '1.up': 'enabled',
            },
            {
                '2.autoip.status': 'disabled',
                '2.devname': 'ath0',
                '2.mtu': 1500,
                '2.status': 'enabled',
                '2.up': 'enabled',
            },
            {
                '3.autoip.status': 'disabled',
                '3.devname': 'br0',
                '3.mtu': 1500,
                '3.status': 'enabled',
                '3.up': 'enabled',
            },
            {
                '4.autoip.status': 'disabled',
                '4.devname': 'veth0',
                '4.mtu': 1500,
                '4.status': 'enabled',
                '4.up': 'enabled',
            },
            {
                '5.autoip.status': 'disabled',
                '5.devname': 'loop0',
                '5.mtu': 1500,
                '5.status': 'enabled',
                '5.up': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netconf'], expected)
