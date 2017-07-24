from .mock import ConverterTest, NtpclientAirOs


class TestResolvConverter(ConverterTest):

    backend = NtpclientAirOs

    def test_ntp_key(self):
        o = self.backend({
            'ntp': {}
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                '1.server': '0.pool.ntp.org',
                '1.status': 'enabled',
            },
            {
                '2.server': '1.pool.ntp.org',
                '2.status': 'enabled',
            },
            {
                '3.server': '2.pool.ntp.org',
                '3.status': 'enabled',
            },
            {
                '4.server': '3.pool.ntp.org',
                '4.status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['ntpclient'], expected)

    def test_no_ntp_server(self):
        o = self.backend({
            'ntp': {
                'enabled': False,
            }
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'disabled',
            },
            {
                '1.server': '0.pool.ntp.org',
                '1.status': 'enabled',
            },
            {
                '2.server': '1.pool.ntp.org',
                '2.status': 'enabled',
            },
            {
                '3.server': '2.pool.ntp.org',
                '3.status': 'enabled',
            },
            {
                '4.server': '3.pool.ntp.org',
                '4.status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['ntpclient'], expected)

    def test_single_ntp_server(self):
        o = self.backend({
            'ntp': {
                'enabled': True,
                'server': [
                    '0.openwrt.pool.ntp.org',
                ]
            },
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                '1.server': '0.openwrt.pool.ntp.org',
                '1.status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['ntpclient'], expected)

    def test_multiple_ntp_server(self):
        o = self.backend({
            'ntp': {
                'server': [
                    '0.openwrt.pool.ntp.org',
                    '1.openwrt.pool.ntp.org',
                ],
            }
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                '1.server': '0.openwrt.pool.ntp.org',
                '1.status': 'enabled',
            },
            {
                '2.server': '1.openwrt.pool.ntp.org',
                '2.status': 'enabled',
            },
        ]

        self.assertEqualConfig(o.intermediate_data['ntpclient'], expected)
