from .dummy import HttpdAirOS, ConverterTest


class TestHttpdConverter(ConverterTest):

    backend = HttpdAirOS

    def test_httpd_key(self):
        o = self.backend({
            "general": {}
        })

        o.to_intermediate()

        expected = [
                {
                    'https.port': 443,
                    'https.status': 'enabled',
                },
                {
                    'port': 80,
                    'session.timeout': 900,
                    'status': 'enabled',
                },
        ]

        self.assertEqualConfig(o.intermediate_data['httpd'], expected)
