import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError as JsonSchemaValidationError

from .schema import schema
from .renderers import SystemRenderer, NetworkRenderer, WirelessRenderer
from ...exceptions import ValidationError

from jinja2 import Environment, PackageLoader


class OpenWrt(object):
    """ OpenWrt Backend """
    schema = schema
    renderers = [
        SystemRenderer,
        NetworkRenderer,
        WirelessRenderer
    ]

    def __init__(self, config):
        self.config = config
        self.env = Environment(loader=PackageLoader('netjsonconfig.backends.openwrt', 'templates'),
                               trim_blocks=True)

    def render(self):
        self.validate()
        output = ''
        for renderer_class in self.renderers:
            renderer = renderer_class(self.config, self.env)
            output += renderer.render()
        return output

    def validate(self):
        try:
            validate(self.config, self.schema)
        except JsonSchemaValidationError as e:
            raise ValidationError(e)

    def json(self, *args, **kwargs):
        self.validate()
        return json.dumps(self.config, *args, **kwargs)
