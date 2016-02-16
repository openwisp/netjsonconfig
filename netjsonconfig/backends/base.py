from jinja2.exceptions import SecurityError
from jinja2.sandbox import SandboxedEnvironment


class ConfigSandbox(SandboxedEnvironment):
    intercepted_binops = frozenset(SandboxedEnvironment.default_binop_table.keys())
    intercepted_unops = frozenset(SandboxedEnvironment.default_unop_table.keys())

    def __init__(self, *args, **kwargs):
        super(ConfigSandbox, self).__init__(*args, **kwargs)
        self.globals = {}
        self.tests = {}
        self.filters = {}
        self.block_start_string = '{=##'
        self.block_end_string = '##=}'
        self.variable_start_string = '${'
        self.variable_end_string = '}'

    def call_binop(self, context, operator, left, right):
        raise SecurityError('binary operator {0} not allowed'.format(operator))

    def call_unop(self, context, operator, left):
        raise SecurityError('unary operator {0} not allowed'.format(operator))


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
    def get_package(cls):
        return str(cls.__name__).replace('Renderer', '').lower()

    def cleanup(self, output):
        """
        Performs cleanup of output (indentation, new lines)
        """
        # correct indentation
        output = output.replace('    ', '')\
                       .replace('option', '\toption')\
                       .replace('list', '\tlist')
        # convert True to 1 and False to 0
        output = output.replace('True', '1')\
                       .replace('False', '0')
        # max 2 consecutive \n delimiters
        output = output.replace('\n\n\n', '\n\n')
        # if output is present
        # ensure it always ends with 1 new line
        if output.endswith('\n\n'):
            return output[0:-1]
        return output

    def render(self):
        """
        Renders config block with jinja2 templating engine
        """
        # get jinja2 template
        template_name = '{0}.uci'.format(self.get_package())
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
