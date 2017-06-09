import unittest

from .dummy import NtpclientAirOS


class TestResolvConverter(unittest.TestCase):

    backend = NtpclientAirOS

    def test_ntp_key(self):
        o = self.backend({
            "general": {}
        })

        o.to_intermediate()

        expected = [
                {
                    'status': 'disabled',
                },
        ]


        self.assertEqual(o.intermediate_data['ntpclient'], expected)
