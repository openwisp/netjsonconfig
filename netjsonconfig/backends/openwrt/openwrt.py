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
                     .replace('list', '    list')[0:-1]

    def _gen_network(self):
        t = self.env.get_template('network.uci')
        interfaces = self._prepare_interfaces()
        # import pdb; pdb.set_trace()
        return t.render(interfaces=interfaces)

    def _prepare_interfaces(self):
        interfaces = self.config.get('interfaces')
        uci_interfaces = []
        for interface in interfaces:
            counter = 1
            uci_name = interface['name'].replace('.', '_')
            for address in interface.get('addresses', []):
                address_key = None
                address_value = None
                if counter > 1:
                    name = '{name}_{counter}'.format(name=uci_name, counter=counter)
                else:
                    name = uci_name
                if address['family'] == 'ipv4':
                    address_key = 'ipaddr'
                elif address['family'] == 'ipv6':
                    address_key = 'ip6addr'
                if address.get('address') and address.get('mask'):
                    address_value = '{address}/{mask}'.format(**address)
                uci_interfaces.append({
                    'uci_name': name,
                    'name': interface['name'],
                    'proto': address.get('proto', 'static'),
                    'address_key': address_key,
                    'address_value': address_value
                })
                counter += 1
        return uci_interfaces
