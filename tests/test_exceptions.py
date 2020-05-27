import unittest

from jsonschema import Draft4Validator, ValidationError

from netjsonconfig import OpenWrt
from netjsonconfig.exceptions import _list_errors

schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'object',
    'additionalProperties': True,
    'definitions': {
        'spam_object': {
            'additionalProperties': True,
            'required': ['spam'],
            'properties': {'spam': {'type': 'string'}},
        },
        'eggs_object': {
            'additionalProperties': True,
            'required': ['eggs'],
            'properties': {'eggs': {'type': 'boolean'}},
        },
    },
    'properties': {
        'test_object': {
            'type': 'object',
            'oneOf': [
                {'$ref': '#/definitions/spam_object'},
                {'$ref': '#/definitions/eggs_object'},
            ],
        }
    },
}


validate = Draft4Validator(schema).validate


class TestJsonSchema(unittest.TestCase):
    """
    tests ValidationError helpers
    """

    def test_spam_object(self):
        test_i = {'test_object': {'spam': 'lots of'}}
        validate(test_i, schema)

    def test_eggs_object(self):
        test_i = {'test_object': {'eggs': True}}
        validate(test_i, schema)

    def test_burrito_object(self):
        test_i = {'test_object': {'burrito': 'yes'}}
        self.assertRaises(ValidationError, validate, test_i, schema)

    def test_burrito_error_message(self):
        test_i = {'test_object': {'burrito': 'yes'}}
        with self.assertRaises(ValidationError) as e:
            validate(test_i, schema)
        message_list = [
            "'spam' is a required property",
            "'eggs' is a required property",
        ]
        self.assertEqual([err.message for err in e.exception.context], message_list)

    def test_list_errors(self):
        test_i = {'test_object': {'burrito': 'yes'}}
        with self.assertRaises(ValidationError) as e:
            validate(test_i, schema)
        suberror_list = [
            ({'$ref': '#/definitions/spam_object'}, "'spam' is a required property"),
            ({'$ref': '#/definitions/eggs_object'}, "'eggs' is a required property"),
        ]
        self.assertEqual(_list_errors(e.exception), suberror_list)

    def test_error_str(self):
        o = OpenWrt({'interfaces': [{'wrong': True}]})
        try:
            o.validate()
        except Exception as e:
            self.assertIn('Against schema', str(e))
        else:
            self.fail('ValidationError not raised')
