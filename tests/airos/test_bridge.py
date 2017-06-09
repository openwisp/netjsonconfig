import unittest

from netjsonconfig.backends.airos.converters import *

from .dummy import BridgeAirOS


class TestBridgeConverter(unittest.TestCase):
    """
    tests for backends.airos.renderers.SystemRenderer
    """
    backend = BridgeAirOS

    def test_active_bridge(self):

        o = self.backend({
            "interfaces": [
                {
                    "type": "ethernet",
                    "name": "eth0",
                    "disabled": False,
                },
                {
                    "type": "ethernet",
                    "name": "eth1",
                    "disabled": False,
                },
                {
                    "type": "bridge",
                    "name": "br0",
                    "bridge_members": [
                        "eth0",
                        "eth1",
                    ],
                    "disabled": False,
                }
            ]
        })

        o.to_intermediate()

        expected = [
                    {
                        '1.comment': '',
                        '1.devname': 'br0',
                        '1.port.1.devname': 'eth0',
                        '1.port.1.status': 'enabled',
                        '1.port.2.devname': 'eth1',
                        '1.port.2.status': 'enabled',
                        '1.status': 'enabled',
                        '1.stp.status': 'enabled'
                    },
                    {
                        'status': 'enabled',
                    }
                ]

        self.assertEqual(o.intermediate_data['bridge'], expected)

    def test_disabled_bridge(self):
        o = self.backend({
            "interfaces": [
                {
                    "type": "ethernet",
                    "name": "eth0",
                    "disabled": False,
                },
                {
                    "type": "ethernet",
                    "name": "eth1",
                    "disabled": False,
                },
                {
                    "type": "bridge",
                    "name": "br0",
                    "bridge_members": [
                        "eth0",
                        "eth1",
                    ],
                    "disabled": True,
                }
            ]
        })

        o.to_intermediate()

        expected = [
                    {
                        '1.comment': '',
                        '1.devname': 'br0',
                        '1.port.1.devname': 'eth0',
                        '1.port.1.status': 'enabled',
                        '1.port.2.devname': 'eth1',
                        '1.port.2.status': 'enabled',
                        '1.status': 'disabled',
                        '1.stp.status': 'enabled'
                    },
                    {
                        'status': 'enabled',
                    }
                ]

        self.assertEqual(o.intermediate_data['bridge'], expected)

    def test_many_bridges(self):
        o = self.backend({
            "interfaces": [
                {
                    "type": "ethernet",
                    "name": "eth0",
                    "disabled": False,
                },
                {
                    "type": "ethernet",
                    "name": "eth1",
                    "disabled": False,
                },
                {
                    "type": "bridge",
                    "name": "br0",
                    "bridge_members": [
                        "eth0",
                        "eth1",
                    ],
                    "disabled": True,
                },
                {
                    "type": "ethernet",
                    "name": "eth2",
                    "disabled": False,
                },
                {
                    "type": "ethernet",
                    "name": "eth3",
                    "disabled": False,
                },
                {
                    "type": "bridge",
                    "name": "br1",
                    "bridge_members": [
                        "eth2",
                        "eth3",
                    ],
                    "disabled": False,
                }
            ]
        })

        o.to_intermediate()

        expected = [
                    {
                        '1.comment': '',
                        '1.devname': 'br0',
                        '1.port.1.devname': 'eth0',
                        '1.port.1.status': 'enabled',
                        '1.port.2.devname': 'eth1',
                        '1.port.2.status': 'enabled',
                        '1.status': 'disabled',
                        '1.stp.status': 'enabled'
                    },
                    {
                        '2.comment': '',
                        '2.devname': 'br1',
                        '2.port.1.devname': 'eth2',
                        '2.port.1.status': 'enabled',
                        '2.port.2.devname': 'eth3',
                        '2.port.2.status': 'enabled',
                        '2.status': 'enabled',
                        '2.stp.status': 'enabled'
                    },
                    {
                        'status': 'enabled',
                    }
                ]

        self.assertEqual(o.intermediate_data['bridge'], expected)

    def test_no_vlan(self):
        o = self.backend({
            "interfaces": [
                {
                    "type": "ethernet",
                    "name": "eth0",
                    "disabled": False,
                },
                {
                    "type": "ethernet",
                    "name": "eth1",
                    "disabled": False,
                },
            ]
        })

        o.to_intermediate()

        expected = [
                    {
                        'status': 'enabled',
                    }
                ]

        self.assertEqual(o.intermediate_data['bridge'], expected)
