import json
from ..exceptions import ValidationError


class OpenWrt(object):
    """ OpenWrt Backend """
    data = None
    schema = None

    def __init__(self):
        pass

    def parse(self, config):
        raise NotImplementedError()

    def gen(self):
        raise NotImplementedError()

    def validate(self):
        raise ValidationError()

    def json(self, *args, **kwargs):
        return json.dumps(self.data, *args, **kwargs)
