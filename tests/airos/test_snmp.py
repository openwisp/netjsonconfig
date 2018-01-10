from .mock import ConverterTest, SnmpAirOs


class TestSnmpConverter(ConverterTest):
    """
    tests for backends.airos.renderers.SystemRenderer
    """
    backend = SnmpAirOs

    def test_defaults(self):

        o = self.backend({})
        o.to_intermediate()
        expected = [
            {
                'community': 'public',
                'contact': '',
                'location': '',
                'status': 'enabled',
            }
        ]

        self.assertEqualConfig(o.intermediate_data['snmp'], expected)

    def test_custom_info(self):

        o = self.backend({
            'general': {
                'mantainer': 'noone@somedomain.com',
                'location': 'somewhere in the woods',
            }
        })
        o.to_intermediate()
        expected = [
            {
                'community': 'public',
                'contact': 'noone@somedomain.com',
                'location': 'somewhere in the woods',
                'status': 'enabled',
            }
        ]

        self.assertEqualConfig(o.intermediate_data['snmp'], expected)
