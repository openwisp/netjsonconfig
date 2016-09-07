import gzip
import json
import tarfile
from copy import deepcopy
from io import BytesIO

import six
from jinja2 import Environment, PackageLoader
from jsonschema import FormatChecker, validate
from jsonschema.exceptions import ValidationError as JsonSchemaError

from ..exceptions import ValidationError
from ..schema import DEFAULT_FILE_MODE
from ..utils import evaluate_vars, merge_config, var_pattern


class BaseBackend(object):
    """
    Base Backend class
    """
    schema = None
    env_path = 'netjsonconfig.backends.base'
    FILE_SECTION_DELIMITER = '# ---------- files ---------- #'

    def __init__(self, config, templates=[], context={}):
        """
        :param config: ``dict`` containing valid **NetJSON DeviceConfiguration**
        :param templates: ``list`` containing **NetJSON** dictionaries that will be
                          used as a base for the main config, defaults to empty list
        :param context: ``dict`` containing configuration variables
        :raises TypeError: raised if ``config`` is not of type ``dict`` or if
                           ``templates`` is not of type ``list``
        """
        # perform deepcopy to avoid modifying the original config argument
        config = deepcopy(self._load(config))
        self.config = self._merge_config(config, templates)
        self.config = self._evaluate_vars(self.config, context)
        self.env = Environment(loader=PackageLoader(self.env_path, 'templates'),
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

    def _evaluate_vars(self, config, context):
        """ evaluates configuration variables """
        # return immediately if context is empty
        if not context:
            return config
        # return immediately if no variables are found
        netjson = self.json(validate=False)
        if var_pattern.search(netjson) is None:
            return config
        # only if variables are found perform evaluation
        return evaluate_vars(config, context)

    def _render_files(self):
        """
        Renders additional files specified in ``self.config['files']``
        """
        output = ''
        # render files
        files = self.config.get('files', [])
        # add delimiter
        if files:
            output += '\n{0}\n\n'.format(self.FILE_SECTION_DELIMITER)
        for f in files:
            mode = f.get('mode', DEFAULT_FILE_MODE)
            # add file to output
            file_output = '# path: {0}\n'\
                          '# mode: {1}\n\n'\
                          '{2}\n\n'.format(f['path'], mode, f['contents'])
            output += file_output
        return output

    def validate(self):
        try:
            validate(self.config, self.schema, format_checker=FormatChecker())
        except JsonSchemaError as e:
            raise ValidationError(e)

    def render(self, files=True):
        """
        Converts the configuration dictionary into the corresponding configuration format.

        :param files: whether to include "additional files" in the output or not;
                      defaults to ``True``
        :returns: string with output
        """
        self.validate()
        output = ''
        # render config
        for renderer_class in self.renderers:
            renderer = renderer_class(self)
            additional_output = renderer.render()
            # add an additional new line
            # to separate blocks
            if output and additional_output:
                output += '\n'
            output += additional_output
        if files:
            # render files
            files_output = self._render_files()
            if files_output:
                output += files_output.replace('\n\n\n', '\n\n')  # max 3 \n
        return output

    def json(self, validate=True, *args, **kwargs):
        """
        returns a string formatted as **NetJSON DeviceConfiguration**;
        performs validation before returning output;

        ``*args`` and ``*kwargs`` will be passed to ``json.dumps``;

        :returns: string
        """
        if validate:
            self.validate()
        # automatically adds NetJSON type
        config = deepcopy(self.config)
        config.update({'type': 'DeviceConfiguration'})
        return json.dumps(config, *args, **kwargs)

    def generate(self):
        """
        Returns a ``BytesIO`` instance representing an in-memory tar.gz archive
        containing the native router configuration.

        :returns: in-memory tar.gz archive, instance of ``BytesIO``
        """
        tar_bytes = BytesIO()
        tar = tarfile.open(fileobj=tar_bytes, mode='w')
        self._generate_contents(tar)
        self._process_files(tar)
        tar.close()
        tar_bytes.seek(0)  # set pointer to beginning of stream
        # `mtime` parameter of gzip file must be 0, otherwise any checksum operation
        # would return a different digest even when content is the same.
        # to achieve this we must use the python `gzip` library because the `tarfile`
        # library does not seem to offer the possibility to modify the gzip `mtime`.
        gzip_bytes = BytesIO()
        gz = gzip.GzipFile(fileobj=gzip_bytes, mode='wb', mtime=0)
        gz.write(tar_bytes.getvalue())
        gz.close()
        gzip_bytes.seek(0)  # set pointer to beginning of stream
        return gzip_bytes

    def _generate_contents(self, tar):
        raise NotImplementedError()

    def write(self, name, path='./'):
        """
        Like ``generate`` but writes to disk.

        :param name: file name, the tar.gz extension will be added automatically
        :param path: directory where the file will be written to, defaults to ``./``
        :returns: None
        """
        byte_object = self.generate()
        file_name = '{0}.tar.gz'.format(name)
        if not path.endswith('/'):
            path += '/'
        f = open('{0}{1}'.format(path, file_name), 'wb')
        f.write(byte_object.getvalue())
        f.close()

    def _process_files(self, tar):
        """
        Adds files specified in self.config['files'] to tarfile instance.

        :param tar: tarfile instance
        :returns: None
        """
        # insert additional files
        for file_item in self.config.get('files', []):
            path = file_item['path']
            # remove leading slashes from path
            if path.startswith('/'):
                path = path[1:]
            self._add_file(tar=tar,
                           name=path,
                           contents=file_item['contents'],
                           mode=file_item.get('mode', DEFAULT_FILE_MODE))

    def _add_file(self, tar, name, contents, mode=DEFAULT_FILE_MODE):
        """
        Adds a single file in tarfile instance.

        :param tar: tarfile instance
        :param name: string representing filename or path
        :param contents: string representing file contents
        :param mode: string representing file mode, defaults to 644
        :returns: None
        """
        byte_contents = BytesIO(contents.encode('utf8'))
        info = tarfile.TarInfo(name=name)
        info.size = len(contents)
        # mtime must be 0 or any checksum operation
        # will return a different digest even when content is the same
        info.mtime = 0
        info.type = tarfile.REGTYPE
        info.mode = int(mode, 8)  # permissions converted to decimal notation
        tar.addfile(tarinfo=info, fileobj=byte_contents)


class BaseRenderer(object):
    """
    Renderers are used to generate specific configuration blocks.
    """
    block_name = None

    def __init__(self, backend):
        self.config = backend.config
        self.env = backend.env
        self.backend = backend

    @classmethod
    def get_name(cls):
        return str(cls.__name__).replace('Renderer', '').lower()

    def cleanup(self, output):
        """
        Performs cleanup of output (indentation, new lines)
        """
        return output

    def render(self):
        """
        Renders config block with jinja2 templating engine
        """
        # get jinja2 template
        template_name = '{0}.jinja2'.format(self.get_name())
        template = self.env.get_template(template_name)
        # render template and cleanup
        context = self.get_context()
        output = template.render(**context)
        return self.cleanup(output)

    def get_context(self):
        """
        Builds context that is passed to jinja2 templates
        """
        # get list of private methods that start with "_get_"
        methods = [method for method in dir(self) if method.startswith('_get_')]
        context = {}
        # build context
        for method in methods:
            key = method.replace('_get_', '')
            context[key] = getattr(self, method)()
        # determine if all context values are empty
        context['is_empty'] = not any(context.values())
        return context
