import json
import re
import six
import tarfile
from io import BytesIO

from jsonschema import validate
from jsonschema.exceptions import ValidationError as JsonSchemaValidationError
from jinja2 import Environment, PackageLoader

from . import renderers
from .schema import schema
from ...exceptions import ValidationError


class OpenWrt(object):
    """ OpenWrt Backend """
    schema = schema
    renderers = [
        renderers.SystemRenderer,
        renderers.NetworkRenderer,
        renderers.WirelessRenderer,
        renderers.DefaultRenderer
    ]

    def __init__(self, config):
        """
        :param config: python dict containing a valid NetJSON DeviceConfiguration
        :raises TypeError: raises an exception if config is not an instance of dict
        """
        if isinstance(config, six.string_types):
            try:
                config = json.loads(config)
            except ValueError:
                pass
        if not isinstance(config, dict):
            raise TypeError('Config argument must be an istance '
                            'of dict or a valid JSON string')
        # allow omitting NetJSON type
        if 'type' not in config:
            config.update({'type': 'DeviceConfiguration'})
        self.config = config
        self.env = Environment(loader=PackageLoader('netjsonconfig.backends.openwrt',
                                                    'templates'),
                               trim_blocks=True)
        try:
            self.__find_bridges()
        except (AttributeError, KeyError):
            # validation will take care of errors later
            pass

    def render(self):
        self.validate()
        output = ''
        for renderer_class in self.renderers:
            renderer = renderer_class(self)
            additional_output = renderer.render()
            # add an additional new line
            # to separate blocks
            if output and additional_output:
                output += '\n'
            output += additional_output
        return output

    def validate(self):
        try:
            validate(self.config, self.schema)
        except JsonSchemaValidationError as e:
            raise ValidationError(e)

    def json(self, *args, **kwargs):
        self.validate()
        return json.dumps(self.config, *args, **kwargs)

    @classmethod
    def get_packages(cls):
        return [r.get_package() for r in cls.renderers]

    def __find_bridges(self):
        """
        OpenWRT declare bridges in /etc/config/network
        but wireless interfaces are attached to ethernet ones
        with declarations that go in /etc/config/wireless
        this method populates a few auxiliary data structures
        that are used to generate the correct UCI bridge settings
        """
        wifi = {}
        bridges = {}
        net_bridges = {}
        for interface in self.config.get('interfaces', []):
            if interface.get('type') == 'wireless':
                wifi[interface['name']] = interface
            elif interface.get('type') == 'bridge':
                bridges[interface['name']] = interface['bridge_members']
        for bridge_members in bridges.values():
            # determine bridges that will go in /etc/config/network
            net_names = [name for name in bridge_members if name not in wifi.keys()]
            net_bridges[net_names[0]] = net_names
            # openwrt deals with wifi bridges differently
            for name in bridge_members:
                if name in wifi.keys():
                    wifi[name]['_attached'] = net_names
        self._net_bridges = net_bridges

    def generate(self, name='openwrt-config'):
        """
        Generates tar.gz restorable in OpenWRT with:
            sysupgrade -r <file>
        """
        uci = self.render()
        tar = tarfile.open('{0}.tar.gz'.format(name), 'w:gz')
        # create a list with all the packages (and remove empty entries)
        packages = re.split('package ', uci)
        if '' in packages:
            packages.remove('')
        # for each package create a file with its contents in /etc/config
        for package in packages:
            lines = package.split('\n')
            package_name = lines[0]
            content_string = '\n'.join(lines[2:])
            content_byte = BytesIO(content_string.encode('utf8'))
            info = tarfile.TarInfo(name='/etc/config/{0}'.format(package_name))
            info.size = len(content_string)
            tar.addfile(tarinfo=info, fileobj=content_byte)
        # close archive
        tar.close()
