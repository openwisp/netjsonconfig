class NetConfigGenException(Exception):
    """ root netconfig-gen exception """
    pass


class ValidationError(NetConfigGenException):
    """ error while validating schema """
    pass
