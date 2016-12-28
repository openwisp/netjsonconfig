import unittest

from netjsonconfig.utils import evaluate_vars, merge_config


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
        merge_config(template, config)
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

    def test_evaluate_vars(self):
        self.assertEqual(evaluate_vars('{{ tz }}', {'tz': 'UTC'}), 'UTC')
        self.assertEqual(evaluate_vars('tz: {{ tz }}', {'tz': 'UTC'}), 'tz: UTC')

    def test_evaluate_vars_missing(self):
        self.assertEqual(evaluate_vars('{{ tz }}'), '{{ tz }}')
        self.assertEqual(evaluate_vars('tz: {{ tz }}'), 'tz: {{ tz }}')

    def test_evaluate_vars_dict(self):
        val = evaluate_vars({'timezone': '{{ tz }}'}, {'tz': 'UTC'})
        self.assertEqual(val, {'timezone': 'UTC'})

    def test_evaluate_vars_nested_dict(self):
        val = evaluate_vars({'general': {'timezone': '{{ tz }}'}}, {'tz': 'UTC'})
        self.assertEqual(val, {'general': {'timezone': 'UTC'}})

    def test_evaluate_vars_list(self):
        val = evaluate_vars(['{{ a }}', '{{ b }}'], {'a': '1', 'b': '2'})
        self.assertEqual(val, ['1', '2'])

    def test_evaluate_vars_list_in_dict(self):
        val = evaluate_vars({'l': ['{{ a }}', '{{ b }}']}, {'a': '1', 'b': '2'})
        self.assertEqual(val, {'l': ['1', '2']})

    def test_evaluate_vars_nowhitespace(self):
        self.assertEqual(evaluate_vars('{{tz}}', {'tz': 'UTC'}), 'UTC')

    def test_evaluate_vars_doublewhitespace(self):
        self.assertEqual(evaluate_vars('{{  tz  }}', {'tz': 'UTC'}), 'UTC')

    def test_evaluate_vars_strangewhitespace(self):
        self.assertEqual(evaluate_vars('{{  tz}}', {'tz': 'UTC'}), 'UTC')

    def test_evaluate_vars_multiple_newline(self):
        """
        see https://github.com/openwisp/netjsonconfig/issues/55
        """
        output = evaluate_vars('{{ a }}\n{{ b }}\n', {'a': 'a', 'b': 'b'})
        self.assertEqual(output, 'a\nb\n')

    def test_evaluate_vars_multiple_space(self):
        output = evaluate_vars('{{ a }} {{ b }}', {'a': 'a', 'b': 'b'})
        self.assertEqual(output, 'a b')

    def test_evaluate_vars_comma(self):
        output = evaluate_vars('{{ a }},{{ b }}', {'a': 'a', 'b': 'b'})
        self.assertEqual(output, 'a,b')

    def test_evaluate_vars_multiple_immersed(self):
        output = evaluate_vars('content{{a}}content{{ b }}content', {'a': 'A', 'b': 'B'})
        self.assertEqual(output, 'contentAcontentBcontent')

    def test_evaluate_vars_immersed(self):
        output = evaluate_vars('content{{a}}content', {'a': 'A'})
        self.assertEqual(output, 'contentAcontent')

    def test_evaluate_vars_one_char(self):
        self.assertEqual(evaluate_vars('{{ a }}', {'a': 'letter-A'}), 'letter-A')
