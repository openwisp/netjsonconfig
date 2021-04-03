from ..base.backend import BaseBackend
from . import converters
from .parser import config_suffix, vpn_pattern
from .renderer import WireguardRenderer
from .schema import schema


class Wireguard(BaseBackend):
    schema = schema
    converters = [converters.Wireguard]
    renderer = WireguardRenderer

    def _generate_contents(self, tar):
        """
        Adds configuration files to tarfile instance.

        :param tar: tarfile instance
        :returns: None
        """
        text = self.render(files=False)
        # create a list with all the packages (and remove empty entries)
        vpn_instances = vpn_pattern.split(text)
        if '' in vpn_instances:
            vpn_instances.remove('')
        # create a file for each VPN
        for vpn in vpn_instances:
            lines = vpn.split('\n')
            vpn_name = lines[0]
            text_contents = '\n'.join(lines[2:])
            # do not end with double new line
            if text_contents.endswith('\n\n'):
                text_contents = text_contents[0:-1]
            self._add_file(
                tar=tar,
                name='{0}{1}'.format(vpn_name, config_suffix),
                contents=text_contents,
            )
