from .mock import ConverterTest, NtpclientAirOs


class TestResolvConverter(ConverterTest):

    backend = NtpclientAirOs

    def test_ntp_key(self):
        o = self.backend({
            "ntp_servers": [],
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'disabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['ntpclient'], expected)

    def test_no_ntp_server(self):
        o = self.backend({
            "ntp_servers": [],
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'disabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['ntpclient'], expected)

    def test_single_ntp_server(self):
        o = self.backend({
            "ntp_servers": [
                '0.openwrt.pool.ntp.org',
            ],
        })
        o.to_intermediate()
        expected = [
            {
                '1.server': '0.openwrt.pool.ntp.org',
                '1.status': 'enabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['ntpclient'], expected)

    def test_multiple_ntp_server(self):
        o = self.backend({
            "ntp_servers": [
                '0.openwrt.pool.ntp.org',
                '1.openwrt.pool.ntp.org',
            ],
        })
        o.to_intermediate()
        expected = [
            {
                '1.server': '0.openwrt.pool.ntp.org',
                '1.status': 'enabled',
            },
            {
                '2.server': '1.openwrt.pool.ntp.org',
                '2.status': 'enabled',
            },
            {
                'status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['ntpclient'], expected)
