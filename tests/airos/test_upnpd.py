from .mock import ConverterTest, UpnpdAirOs


class TestUpnpdConverter(ConverterTest):
    """
    tests for backends.airos.renderers.SystemRenderer
    """
    backend = UpnpdAirOs

    def test_bridge(self):

        o = self.backend({
            'netmode': 'bridge',
        })
        o.to_intermediate()
        with self.assertRaises(KeyError):
            o.intermediate_data['upnpd']

    def test_router(self):
        o = self.backend({
            'netmode': 'router',
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'disabled',
            }
        ]
        self.assertEqualConfig(o.intermediate_data['upnpd'], expected)
