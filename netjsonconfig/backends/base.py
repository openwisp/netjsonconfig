class BaseRenderer(object):
    """
    Renderers are used to generate specific configuration blocks.
    """
    block_name = None

    def __init__(self, config, env):
        self.config = config
        self.env = env

    def cleanup(self, output):
        """
        Performs cleanup of output (indentation, new lines)
        """
        return output.replace('    ', '')\
                     .replace('option', '    option')\
                     .replace('list', '    list')[0:-1]

    def render(self):
        """
        Renders block
        """
        template_name = '{0}.uci'.format(self.block_name)
        template = self.env.get_template(template_name)
        context = self.get_context()
        output = template.render(**context)
        return self.cleanup(output)
