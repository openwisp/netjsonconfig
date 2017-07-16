import re
from . import converters
from ..base.backend import BaseBackend
from .renderer import Commands, Hostapd, Hostname, Interfaces, Ntp, Resolv
from .schema import schema


class Raspbian(BaseBackend):
    """
    Raspbian Backend
    """
    schema = schema
    converters = [
        converters.General,
        converters.Interfaces,
        converters.Wireless,
        converters.DnsServers,
        converters.DnsSearch,
        converters.Ntp
    ]
    renderers = [
        Hostname,
        Hostapd,
        Interfaces,
        Resolv,
        Ntp,
        Commands
    ]

    def _generate_contents(self, tar):
        text = self.render(files=False)
        config_files_pattern = re.compile('^# config:\s', flags=re.MULTILINE)
        config_files = config_files_pattern.split(text)
        if '' in config_files:
            config_files.remove('')
        for config_file in config_files:
            lines = config_file.split('\n')
            file_name = lines[0]
            text_contents = '\n'.join(lines[2:])
            self._add_file(tar=tar,
                           name='{0}'.format(file_name),
                           contents=text_contents)
