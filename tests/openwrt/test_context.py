import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.backends.openwrt.timezones import timezones
from netjsonconfig.utils import _TabsMixin


class TestContext(unittest.TestCase, _TabsMixin):
    """
    tests for configuration variables feature
    """

    maxDiff = None

    def test_config(self):
        config = {"general": {"hostname": "{{ name }}", "description": "{{ desc }}"}}
        context = {"name": "test-context-name", "desc": "test.context.desc"}
        o = OpenWrt(config, context=context)
        output = o.render()
        self.assertIn("option hostname 'test-context-name'", output)
        self.assertIn("option description 'test.context.desc'", output)

    def test_template(self):
        config = {"general": {"hostname": "{{ name }}"}}
        template = {"general": {"description": "{{ desc }}"}}
        context = {"name": "test-context-name", "desc": "test.context.desc"}
        o = OpenWrt(config, context=context, templates=[template])
        output = o.render()
        self.assertIn("option hostname 'test-context-name'", output)
        self.assertIn("option description 'test.context.desc'", output)

    def test_evaluation_order(self):
        config = {"general": {"timezone": "{{ tz }}"}}
        context = {"tz": "Europe/Amsterdam"}
        o = OpenWrt(config, context=context)
        line = "option timezone '{Europe/Amsterdam}'".format(**timezones)
        output = o.render()
        self.assertIn(line, output)

    def test_no_variables_found(self):
        config = {"general": {"description": "{{ desc }}"}}
        o = OpenWrt(config, context={"a": "b"})
        output = o.render()
        self.assertIn("option description '{{ desc }}'", output)

    def test_context_bug(self):
        """
        see https://github.com/openwisp/netjsonconfig/issues/55
        """
        config = {"general": {"hostname": "test-context"}}
        template = {
            "files": [
                {
                    "path": "/etc/vpnserver1",
                    "mode": "0644",
                    "contents": "{{ name }}\n{{ vpnserver1 }}\n",
                }
            ]
        }
        context = {"name": "test-context", "vpnserver1": "vpn.testdomain.com"}
        o = OpenWrt(config, context=context, templates=[template])
        self.assertIn("vpn.testdomain.com", o.render())
