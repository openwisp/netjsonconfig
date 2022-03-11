import unittest
from unittest.mock import patch

from netjsonconfig.backends.wireguard.parser import WireguardParser


class TestBaseParser(unittest.TestCase):
    """
    Tests for netjsonconfig.backends.wireguard.parser.BaseParser
    """

    def test_parse_text(self):
        # Creating an instance of WireguardParser will raise
        # NotImplementedError since it will requires "parse_text"
        with self.assertRaises(NotImplementedError):
            WireguardParser(config="")

    @patch.object(WireguardParser, 'parse_text', return_value=None)
    def test_parse_tar(self, mocked):
        parser = WireguardParser(config="")
        with self.assertRaises(NotImplementedError):
            parser.parse_tar(tar=None)

    @patch.object(WireguardParser, 'parse_text', return_value=None)
    def test_get_vpns(self, mocked):
        parser = WireguardParser(config="")
        with self.assertRaises(NotImplementedError):
            parser._get_vpns(text=None)

    @patch.object(WireguardParser, 'parse_text', return_value=None)
    def test_get_config(self, mocked):
        parser = WireguardParser(config="")
        with self.assertRaises(NotImplementedError):
            parser._get_config(contents=None)
