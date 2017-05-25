class NetJsonConfigException(Exception):
    """
    Root netjsonconfig exception
    """
    def __str__(self):
        return "%s %s %s" % (self.__class__.__name__, self.message, self.details)


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
