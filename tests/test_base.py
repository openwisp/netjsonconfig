import unittest
from io import BytesIO

from netjsonconfig.backends.base.backend import BaseBackend
from netjsonconfig.backends.base.parser import BaseParser
from netjsonconfig.backends.base.renderer import BaseRenderer


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

    def test_parse_text_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            BaseParser('')

    def test_parse_tar_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            BaseParser(BytesIO())

    def test_base_backend_parse_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            BaseBackend(native='')
