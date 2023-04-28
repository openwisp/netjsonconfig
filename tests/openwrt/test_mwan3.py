import textwrap
import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.exceptions import ValidationError
from netjsonconfig.utils import _TabsMixin


class TestMwan3(unittest.TestCase, _TabsMixin):
    maxDiff = None

    _interfaces_1_netjson = {
        "mwan3": {
            "interfaces": [
                {
                    "name": "Test",
                    "enabled": True,
                    "initial_state": "online",
                    "family": "ipv4",
                    "track_method": "ping",
                    "reliability": 1,
                    "count": 1,
                    "size": 56,
                    "max_ttl": 60,
                    "check_quality": False,
                    "timeout": 4,
                    "interval": 10,
                    "failure_interval": 0,
                    "recovery_interval": 0,
                    "down": 5,
                    "keep_failure_interval": False,
                    "up": 5,
                    "track_ip": ["8.8.8.8"],
                    "flush_conntrack": ["ifup"],
                }
            ]
        }
    }

    _interfaces_1_uci = textwrap.dedent(
        """\
        package mwan3

        config globals 'globals'

        config interface 'Test'
            option name 'Test'
            option enabled '1'
            option initial_state 'online'
            option family 'ipv4'
            option track_method 'ping'
            option reliability '1'
            option count '1'
            option size '56'
            option max_ttl '60'
            option check_quality '0'
            option timeout '4'
            option interval '10'
            option failure_interval '0'
            option recovery_interval '0'
            option down '5'
            option keep_failure_interval '0'
            option up '5'
            list track_ip '8.8.8.8'
            list flush_conntrack 'ifup'
       """
    )

    def test_render_interfaces_1(self):
        o = OpenWrt(self._interfaces_1_netjson)
        expected = self._tabs(self._interfaces_1_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_interfaces_1(self):
        o = OpenWrt(native=self._interfaces_1_uci)
        self.assertEqual(o.config, self._interfaces_1_netjson)
