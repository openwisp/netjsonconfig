from functools import reduce


def list_error_in_subschema(jsonschema_error):
    sub_errors = []
    for validator_value, error in zip(jsonschema_error.validator_value, jsonschema_error.context):
        sub_errors.append((validator_value, error.message))
        if error.context:
            sub_errors += list_error_in_subschema(error)
    return sub_errors


class NetJsonConfigException(Exception):
    """
    Root netjsonconfig exception
    """
    def __str__(self):
        suberrors = list_error_in_subschema(self.details)

        default_message = "%s %s\n" % (self.__class__.__name__, self.details,)
        suberror_fmt = '\nAgainst schema %s\n%s\n'
        suberror_message = reduce(lambda x, y: x + suberror_fmt % y, suberrors, '')

        return default_message + suberror_message


class ValidationError(NetJsonConfigException):
    """
    Error while validating schema
    """
    def __init__(self, e):
        """
        preserve jsonschema exception attributes
        in self.details
        """
        self.message = e.message
        self.details = e
