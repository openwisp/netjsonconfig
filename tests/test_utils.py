import unittest

from netjsonconfig.utils import merge_config


class TestUtils(unittest.TestCase):
    """
    tests for netjsonconfig.utils
    """
    def test_merge_config(self):
        template = {"a": "a", "c": "template"}
        config = {"b": "b", "c": "config"}
        result = merge_config(template, config)
        self.assertEqual(result, {
            "a": "a",
            "b": "b",
            "c": "config"
        })

    def test_merge_config_dict(self):
        template = {
            "dict": {"a": "a"},
        }
        config = {
            "dict": {"b": "b"},
            "key": "val"
        }
        result = merge_config(template, config)
        self.assertEqual(result, {
            "dict": {
                "a": "a",
                "b": "b"
            },
            "key": "val"
        })

    def test_merge_config_list(self):
        template = {
            "list": ["element1"]
        }
        config = {
            "list": ["element2"]
        }
        result = merge_config(template, config)
        self.assertEqual(result, {
            "list": [
                "element1",
                "element2"
            ]
        })
