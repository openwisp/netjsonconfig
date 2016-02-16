import unittest

from jinja2.exceptions import SecurityError

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestContext(unittest.TestCase, _TabsMixin):
    """
    tests for configuration variables feature
    """
    def test_config(self):
        config = {
            "general": {
                "hostname": "${name}",
                "description": "${desc}"
            }
        }
        context = {
            "name": "test-context-name",
            "desc": "test.context.desc"
        }
        o = OpenWrt(config, context=context)
        output = o.render()
        self.assertIn("option hostname 'test-context-name'", output)
        self.assertIn("option description 'test.context.desc'", output)

    def test_template(self):
        config = {"general": {"hostname": "${name}"}}
        template = {"general": {"description": "${desc}"}}
        context = {
            "name": "test-context-name",
            "desc": "test.context.desc"
        }
        o = OpenWrt(config, context=context, templates=[template])
        output = o.render()
        self.assertIn("option hostname 'test-context-name'", output)
        self.assertIn("option description 'test.context.desc'", output)

    def test_sandbox(self):
        danger = """${ self.__repr__.__globals__.get('sys').version }"""
        config = {"general": {"description": danger}}
        o = OpenWrt(config, context={"description": "sandbox"})
        with self.assertRaises(SecurityError):
            print(o.render())

    def test_security_binop(self):
        danger = """desc: ${10**10}"""
        config = {"general": {"description": danger}}
        o = OpenWrt(config, context={"description": "sandbox"})
        with self.assertRaises(SecurityError):
            print(o.render())

    def test_security_unop(self):
        danger = """desc: ${ -10 }"""
        config = {"general": {"description": danger}}
        o = OpenWrt(config, context={"description": "sandbox"})
        with self.assertRaises(SecurityError):
            print(o.render())

    def test_security_block(self):
        danger = """{=## if True ##=}true{=## endif ##=}"""
        config = {"general": {"description": danger}}
        o = OpenWrt(config, context={"description": "sandbox"})
        with self.assertRaises(SecurityError):
            print(o.render())

    def test_security_methods(self):
        danger = """${ "{.__getitem__.__globals__[sys].version}".format(self) }"""
        config = {"general": {"description": danger}}
        o = OpenWrt(config, context={"description": "sandbox"})
        with self.assertRaises(SecurityError):
            print(o.render())
