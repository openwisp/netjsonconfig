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
from ...utils import merge_config
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

    def __init__(self, config, templates=[]):
        """
        :param config: dict containing a valid NetJSON DeviceConfiguration
        :param templates: list containing zero or more config blocks that will be used
                          as a base for the main config, defaults to empty list
        :raises TypeError: raised if config is not dict or templates is not a list
        """
        config = self._load(config)
        # allow omitting NetJSON type
        if 'type' not in config:
            config.update({'type': 'DeviceConfiguration'})
        self.config = self._merge_config(config, templates)
        self.env = Environment(loader=PackageLoader('netjsonconfig.backends.openwrt',
                                                    'templates'),
                               trim_blocks=True)
        try:
            self.__find_bridges()
        except (AttributeError, KeyError):
            # validation will take care of errors later
            pass

    def _load(self, config):
        """ loads config from string or dict """
        if isinstance(config, six.string_types):
            try:
                config = json.loads(config)
            except ValueError:
                pass
        if not isinstance(config, dict):
            raise TypeError('config block must be an istance '
                            'of dict or a valid NetJSON string')
        return config

    def _merge_config(self, config, templates):
        """ merges config with templates """
        # type check
        if not isinstance(templates, list):
            raise TypeError('templates argument must be an instance of list')
        # merge any present template with main configuration
        base_config = {}
        for template in templates:
            template = self._load(template)
            base_config = merge_config(base_config, template)
        if base_config:
            return merge_config(base_config, config)
        return config

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
            text_contents = '\n'.join(lines[2:])
            byte_contents = BytesIO(text_contents.encode('utf8'))
            info = tarfile.TarInfo(name='/etc/config/{0}'.format(package_name))
            info.size = len(text_contents)
            tar.addfile(tarinfo=info, fileobj=byte_contents)
        # insert additional files
        for file_item in self.config.get('files', []):
            byte_contents = BytesIO(file_item['contents'].encode('utf8'))
            info = tarfile.TarInfo(name=file_item['path'])
            info.size = len(file_item['contents'])
            tar.addfile(tarinfo=info, fileobj=byte_contents)
        # close archive
        tar.close()
