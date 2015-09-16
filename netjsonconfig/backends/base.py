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
        output = output.replace('    ', '')\
                       .replace('option', '    option')\
                       .replace('list', '    list')
        # if output is present
        # ensure it always ends with 1 new line
        if output and not output.endswith('\n'):
            output += '\n'
        if output.endswith('\n\n'):
            return output[0:-1]
        return output

    def render(self):
        """
        Renders block
        """
        template_name = '{0}.uci'.format(self.block_name)
        template = self.env.get_template(template_name)
        context = self.get_context()
        output = template.render(**context)
        return self.cleanup(output)
