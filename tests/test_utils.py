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

    def test_merge_originals_unchanged(self):
        template = {
            "str": "original",
            "dict": {"a": "a"},
            "list": ["element1"]
        }
        config = {
            "str": "changed",
            "dict": {"b": "b"},
            "list": ["element2"]
        }
        result = merge_config(template, config)
        # ensure original structures not changed
        self.assertEqual(template, {
            "str": "original",
            "dict": {"a": "a"},
            "list": ["element1"]
        })
        self.assertEqual(config, {
            "str": "changed",
            "dict": {"b": "b"},
            "list": ["element2"]
        })

    def test_merge_list_of_dicts_unchanged(self):
        template = {
            "list": [
                {"a": "original"},
                {"b": "original"}
            ]
        }
        config = {
            "list": [
                {"c": "original"}
            ]
        }
        result = merge_config(template, config)
        template['list'][0]['a'] = 'changed'
        config['list'][0]['c'] = 'changed'
        result['list'][1]['b'] = 'changed'
        # ensure originals changed
        # but not result of merge
        self.assertEqual(template, {
            "list": [
                {"a": "changed"},
                {"b": "original"}
            ]
        })
        self.assertEqual(config, {
            "list": [
                {"c": "changed"}
            ]
        })
        self.assertEqual(result, {
            "list": [
                {"a": "original"},
                {"b": "changed"},
                {"c": "original"}
            ]
        })
