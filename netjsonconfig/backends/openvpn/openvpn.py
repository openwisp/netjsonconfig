import re

from ..base import BaseBackend
from .renderers import OpenVpnRenderer
from .schema import schema


class OpenVpn(BaseBackend):
    """
    OpenVPN 2.3 backend
    """
    schema = schema
    env_path = 'netjsonconfig.backends.openvpn'
    renderers = [OpenVpnRenderer]
    VPN_REGEXP = re.compile('# openvpn config: ')

    def _generate_contents(self, tar):
        """
        Adds configuration files to tarfile instance.

        :param tar: tarfile instance
        :returns: None
        """
        text = self.render(files=False)
        # create a list with all the packages (and remove empty entries)
        vpn_instances = self.VPN_REGEXP.split(text)
        if '' in vpn_instances:
            vpn_instances.remove('')
        # for each package create a file with its contents in /etc/config
        for vpn in vpn_instances:
            lines = vpn.split('\n')
            vpn_name = lines[0]
            text_contents = '\n'.join(lines[2:])
            # do not end with double new line
            if text_contents.endswith('\n\n'):
                text_contents = text_contents[0:-1]
            self._add_file(tar=tar,
                           name='{0}.conf'.format(vpn_name),
                           contents=text_contents)
