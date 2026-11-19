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

    def test_russian_timezones_without_dst(self):
        # Russia abolished DST in 2011 and moved to permanent standard time in 2014
        tz = timezones.timezones
        self.assertEqual(tz["Europe/Moscow"], "MSK-3")
        self.assertEqual(tz["Asia/Vladivostok"], "<+10>-10")
        self.assertEqual(tz["Asia/Krasnoyarsk"], "<+07>-7")
        self.assertEqual(tz["Europe/Volgograd"], "MSK-3")
        for name in ("Asia/Magadan", "Asia/Novosibirsk", "Europe/Samara"):
            self.assertNotIn(",M3.5.0", tz[name])

    def test_new_timezones(self):
        self.assertIn("America/Ciudad Juarez", timezones.timezones)
        self.assertIn("America/Coyhaique", timezones.timezones)
