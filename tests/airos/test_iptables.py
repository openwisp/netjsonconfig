from .mock import ConverterTest, IptablesAirOs


class IptablesConverter(ConverterTest):
    backend = IptablesAirOs

    def test_bridge(self):
        o = self.backend({
            'netmode': 'bridge',
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'disabled',
            },
            {
                'sys.portfw.status': 'disabled',
                'sys.status': 'enabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['iptables'], expected)

    def test_router(self):
        o = self.backend({
            'netmode': 'router',
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                'sys.portfw.status': 'disabled',
                'sys.fw.status': 'disabled',
                'sys.mgmt.1.devname': 'br0',
                'sys.mgmt.1.status': 'enabled',
                'sys.mgmt.status': 'enabled',
                'sys.status': 'enabled',
            },
        ]
        self.assertEqualConfig(o.intermediate_data['iptables'], expected)
