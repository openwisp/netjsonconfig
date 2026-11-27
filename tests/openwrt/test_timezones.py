import ast
import inspect
import unittest

from netjsonconfig.backends.openwrt import timezones


class TestTimezones(unittest.TestCase):
    def test_entries_are_tuples(self):
        # a set literal is unpacked in hash order, which differs per process
        tree = ast.parse(inspect.getsource(timezones))
        sets = [node.lineno for node in ast.walk(tree) if isinstance(node, ast.Set)]
        self.assertEqual(sets, [])
        self.assertIn("Asia/Qostanay", timezones.timezones)
        self.assertEqual(
            timezones.timezones["Europe/Kyiv"], "EET-2EEST,M3.5.0/3,M10.5.0/4"
        )
