class NetJsonConfigException(Exception):
    """ root netjsonconfig exception """
    pass


class ValidationError(NetJsonConfigException):
    """ error while validating schema """
    pass
