from .mock import ConverterTest, NetmodeAirOs


class TestNetmodeConverter(ConverterTest):

    backend = NetmodeAirOs

    def test_netconf_key(self):
        o = self.backend({
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'bridge',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netmode'], expected)

    def test_bridge(self):
        o = self.backend({
            'netmode': 'bridge',
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'bridge',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netmode'], expected)

    def test_router(self):
        o = self.backend({
            'netmode': 'router',
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'router',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['netmode'], expected)
