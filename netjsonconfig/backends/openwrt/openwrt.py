import json

from .schema import schema
from .renderers import NetworkRenderer, SystemRenderer
from ...exceptions import ValidationError

from jinja2 import Environment, PackageLoader


class OpenWrt(object):
    """ OpenWrt Backend """
    schema = schema
    renderers = [
        SystemRenderer,
        NetworkRenderer
    ]

    def __init__(self, config):
        self.config = config
        self.env = Environment(loader=PackageLoader('netjsonconfig.backends.openwrt', 'templates'),
                               trim_blocks=True)

    def render(self):
        output = ''
        for renderer_class in self.renderers:
            renderer = renderer_class(self.config, self.env)
            output += renderer.render()
        return output

    def validate(self):
        raise ValidationError()

    def json(self, *args, **kwargs):
        return json.dumps(self.config, *args, **kwargs)
