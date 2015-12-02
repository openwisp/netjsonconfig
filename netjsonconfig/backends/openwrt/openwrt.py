import json
import re
import six
import time
import tarfile
from io import BytesIO
from copy import deepcopy

from jsonschema import validate
from jsonschema.exceptions import ValidationError as JsonSchemaError
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
        # perform deepcopy to avoid modifying the original config argument
        config = deepcopy(self._load(config))
        # allow omitting NetJSON type
        if 'type' not in config:
            config.update({'type': 'DeviceConfiguration'})
        self.config = self._merge_config(config, templates)
        self.env = Environment(loader=PackageLoader('netjsonconfig.backends.openwrt',
                                                    'templates'),
                               trim_blocks=True)

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
        except JsonSchemaError as e:
            raise ValidationError(e)

    def json(self, *args, **kwargs):
        self.validate()
        return json.dumps(self.config, *args, **kwargs)

    @classmethod
    def get_packages(cls):
        return [r.get_package() for r in cls.renderers]

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
        timestamp = time.time()
        for package in packages:
            lines = package.split('\n')
            package_name = lines[0]
            text_contents = '\n'.join(lines[2:])
            self._add_file(tar=tar,
                           name='etc/config/{0}'.format(package_name),
                           contents=text_contents,
                           timestamp=timestamp)
        self._add_files(tar, timestamp)
        # close archive
        tar.close()

    def _add_files(self, tar, timestamp):
        """
        adds files specified in self.config['files']
        in specified tar object
        """
        # insert additional files
        for file_item in self.config.get('files', []):
            contents = file_item['contents']
            path = file_item['path']
            # join lines if contents is a list
            if isinstance(contents, list):
                contents = '\n'.join(contents)
            # remove leading slashes from path
            if path.startswith('/'):
                path = path[1:]
            self._add_file(tar=tar,
                           name=path,
                           contents=contents,
                           timestamp=timestamp,
                           mode=file_item.get('mode', '644'))

    def _add_file(self, tar, name, contents, timestamp, mode='644'):
        """
        adds a single file in tar object
        """
        byte_contents = BytesIO(contents.encode('utf8'))
        info = tarfile.TarInfo(name=name)
        info.size = len(contents)
        info.mtime = timestamp
        info.type = tarfile.REGTYPE
        info.mode = int(mode, 8)  # permissions converted to decimal notation
        tar.addfile(tarinfo=info, fileobj=byte_contents)
