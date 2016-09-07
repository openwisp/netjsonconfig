import unittest

from netjsonconfig.backends.base import BaseBackend, BaseRenderer


class TestBase(unittest.TestCase):
    """
    tests for netjsonconfig.backends.base
    """
    def test_generate(self):
        b = BaseBackend({})
        with self.assertRaises(NotImplementedError):
            b.generate()

    def test_cleanup(self):
        b = BaseBackend({})
        r = BaseRenderer(b)
        self.assertEqual(r.cleanup(''), '')
