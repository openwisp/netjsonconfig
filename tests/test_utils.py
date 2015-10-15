import unittest

from netjsonconfig.utils import merge_config


class TestUtils(unittest.TestCase):
    """
    tests for netjsonconfig.utils
    """
    def test_merge_config(self):
        template = {
            "dict": {
                "a": "a"
            },
            "list": [
                "element1"
            ]
        }
        config = {
            "dict": {
                "b": "b"
            },
            "list": [
                "element2"
            ]
        }
        result = merge_config(template, config)
        self.assertEqual(result, {
            "dict": {
                "a": "a",
                "b": "b"
            },
            "list": [
                "element1",
                "element2"
            ]
        })
