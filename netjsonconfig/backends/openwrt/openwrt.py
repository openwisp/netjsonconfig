import re

from . import renderers
from ..base import BaseBackend
from .schema import schema


class OpenWrt(BaseBackend):
    """ OpenWrt Backend """
    schema = schema
    env_path = 'netjsonconfig.backends.openwrt'
    renderers = [
        renderers.SystemRenderer,
        renderers.NetworkRenderer,
        renderers.WirelessRenderer,
        renderers.DefaultRenderer,
        renderers.OpenVpnRenderer
    ]
    PACKAGE_EXP = re.compile('package ')

    @classmethod
    def get_renderers(cls):
        return [r.get_name() for r in cls.renderers]

    def _generate_contents(self, tar):
        """
        Adds configuration files to tarfile instance.

        :param tar: tarfile instance
        :returns: None
        """
        uci = self.render(files=False)
        # create a list with all the packages (and remove empty entries)
        packages = self.PACKAGE_EXP.split(uci)
        if '' in packages:
            packages.remove('')
        # for each package create a file with its contents in /etc/config
        for package in packages:
            lines = package.split('\n')
            package_name = lines[0]
            text_contents = '\n'.join(lines[2:])
            self._add_file(tar=tar,
                           name='etc/config/{0}'.format(package_name),
                           contents=text_contents)
