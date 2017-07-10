from .dummy import VlanAirOS, ConverterTest


class TestVlanConverter(ConverterTest):
    """
    tests for backends.airos.renderers.SystemRenderer
    """
    backend = VlanAirOS

    def test_active_vlan(self):

        o = self.backend({
            "interfaces": [
                {
                    "type": "ethernet",
                    "name": "eth0.1",
                    "disabled": False,
                }
            ]
        })

        o.to_intermediate()

        expected = [
                    {
                        '1.comment': '',
                        '1.devname': 'eth0',
                        '1.id': '1',
                        '1.status' : 'enabled',
                    },
                    {
                        'status' : 'enabled',
                    }
                ]

        self.assertEqualConfig(o.intermediate_data['vlan'], expected)

    def test_disabled_vlan(self):

        o = self.backend({
            "interfaces": [
                {
                    "type": "ethernet",
                    "name": "eth0.1",
                    "disabled": True,
                }
            ]
        })

        expected = [
                    {
                        '1.comment': '',
                        '1.devname': 'eth0',
                        '1.id': '1',
                        '1.status': 'disabled',
                    },
                    {
                        'status' : 'enabled',
                    }
                ]

        o.to_intermediate()

        self.assertEqualConfig(o.intermediate_data['vlan'], expected)

    def test_many_vlan(self):

        o = self.backend({
            "interfaces": [
                {
                    "type": "ethernet",
                    "name": "eth0.1",
                    "disabled": False,
                },
                {
                    "type": "ethernet",
                    "name": "eth0.2",
                    "disabled": False,
                }
            ]
        })

        expected = [
                    {
                        '1.comment': '',
                        '1.devname': 'eth0',
                        '1.id': '1',
                        '1.status': 'enabled',
                    },
                    {
                        '2.comment': '',
                        '2.devname': 'eth0',
                        '2.id': '2',
                        '2.status': 'enabled',
                    },
                    {
                        'status' : 'enabled',
                    }
                ]

        o.to_intermediate()

        self.assertEqualConfig(o.intermediate_data['vlan'], expected)

    def test_mixed_vlan(self):

        o = self.backend({
            "interfaces": [
                {
                    "type": "ethernet",
                    "name": "eth0.1",
                    "disabled": True,
                },
                {
                    "type": "ethernet",
                    "name": "eth0.2",
                    "disabled": False,
                }
            ]
        })

        expected = [
                    {
                        '1.comment': '',
                        '1.devname': 'eth0',
                        '1.id': '1',
                        '1.status': 'disabled',
                    },
                    {
                        '2.comment': '',
                        '2.devname': 'eth0',
                        '2.id': '2',
                        '2.status': 'enabled',
                    },
                    {
                        'status' : 'enabled',
                    }
                ]

        o.to_intermediate()

        self.assertEqualConfig(o.intermediate_data['vlan'], expected)

    def test_no_vlan(self):

        o = self.backend({
            "interfaces": [
                {
                    "type": "ethernet",
                    "name": "eth0",
                    "disabled": True,
                },
            ]
        })

        expected = [
                    {
                        'status' : 'enabled',
                    },
                ]

        o.to_intermediate()

        self.assertEqualConfig(o.intermediate_data['vlan'], expected)

    def test_one_vlan(self):

        o = self.backend({
            "interfaces": [
                {
                    "type": "ethernet",
                    "name": "eth0",
                    "disabled": False,
                },
                {
                    "type": "ethernet",
                    "name": "eth0.1",
                    "disabled": False,
                },

            ]
        })

        expected = [
                    {
                        '1.comment': '',
                        '1.devname': 'eth0',
                        '1.id': '1',
                        '1.status': 'enabled',
                    },
                    {
                        'status' : 'enabled',
                    },
                ]

        o.to_intermediate()

        self.assertEqualConfig(o.intermediate_data['vlan'], expected)
