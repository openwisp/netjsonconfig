import json

from .schema import schema
from ...exceptions import ValidationError

from jinja2 import Environment, PackageLoader


class OpenWrt(object):
    """ OpenWrt Backend """
    schema = schema

    def __init__(self, config):
        self.config = config
        self.env = Environment(loader=PackageLoader('netjsonconfig.backends.openwrt', 'templates'),
                               trim_blocks=True)

    def parse(self, config):
        raise NotImplementedError()

    def gen(self):
        output = self._gen('network')
        return output

    def validate(self):
        raise ValidationError()

    def json(self, *args, **kwargs):
        return json.dumps(self.config, *args, **kwargs)

    def _gen(self, block):
        method_name = '_gen_{0}'.format(block)
        method = getattr(self, method_name)
        output = method.__call__()
        return self._clean(output)

    def _clean(self, output):
        return output.replace('    ', '')\
                     .replace('option', '    option')\
                     .replace('list', '    list')

    def _gen_network(self):
        t = self.env.get_template('network.uci')
        return t.render(interfaces=self.config.get('interfaces'))
