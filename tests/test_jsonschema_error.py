import unittest

from jsonschema import ValidationError, validate

from netjsonconfig.exceptions import list_error_in_subschema

schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'additionalProperties': True,
        'definitions': {
            'spam_object': {
                'additionalProperties': True,
                'required': [
                    'spam',
                ],
                'properties': {
                    'spam': {
                        'type': 'string',
                    },
                },
            },
            'eggs_object': {
                'additionalProperties': True,
                'required': [
                    'eggs',
                ],
                'properties': {
                    'eggs': {
                        'type': 'boolean',
                    },
                },
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


class TestJsonSchema(unittest.TestCase):
    """
    tests ValidationError helpers
    """

    def test_spam_object(self):
        test_i = {
                'test_object': {
                    'spam': 'lots of',
                },
        }

        validate(test_i, schema)

    def test_eggs_object(self):
        test_i = {
                'test_object': {
                    'eggs': True,
                },
        }

        validate(test_i, schema)

    def test_burrito_object(self):
        test_i = {
                'test_object': {
                    'burrito': 'yes',
                },
        }

        self.assertRaises(ValidationError, validate, test_i, schema)

    def test_burrito_error_message(self):
        test_i = {
                'test_object': {
                    'burrito': 'yes',
                },
        }

        with self.assertRaises(ValidationError) as error_container:
            validate(test_i, schema)

        message_list = [
                "'spam' is a required property",
                "'eggs' is a required property",
        ]

        self.assertEqual([e.message for e in error_container.exception.context], message_list)

    def test_list_error_in_subschema(self):
        test_i = {
                'test_object': {
                    'burrito': 'yes',
                },
        }

        with self.assertRaises(ValidationError) as error_container:
            validate(test_i, schema)

        suberror_list = [
                ({'$ref': '#/definitions/spam_object'}, "'spam' is a required property"),

                ({'$ref': '#/definitions/eggs_object'}, "'eggs' is a required property"),
        ]

        self.assertEqual(list_error_in_subschema(error_container.exception), suberror_list)
