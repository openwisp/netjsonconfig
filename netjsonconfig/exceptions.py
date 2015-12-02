class NetJsonConfigException(Exception):
    """ root netjsonconfig exception """
    pass


class ValidationError(NetJsonConfigException):
    """ error while validating schema """

    def __init__(self, e):
        """
        preserve jsonschema exception attributes
        in self.details
        """
        self.message = e.message
        self.details = e
