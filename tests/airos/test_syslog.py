from .mock import ConverterTest, SyslogAirOs


class TestSyslogConverter(ConverterTest):
    backend = SyslogAirOs

    def test_active(self):
        o = self.backend({})
        o.to_intermediate()
        expected = [
            {
                'remote.port': 514,
                'remote.status': 'disabled',
                'status': 'enabled',
            }
        ]
        self.assertEqualConfig(o.intermediate_data['syslog'], expected)
