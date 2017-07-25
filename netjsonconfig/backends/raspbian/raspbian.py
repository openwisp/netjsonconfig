import re

from . import converters
from ..base.backend import BaseBackend
from .renderer import Scripts, Hostapd, Hostname, Interfaces, Ntp, Resolv
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
        Scripts
    ]

    def _generate_contents(self, tar):
        text = self.render(files=False)
        files_pattern = re.compile('^# config:\s|^# script:\s', flags=re.MULTILINE)
        files = files_pattern.split(text)
        if '' in files:
            files.remove('')
        for file in files:
            lines = file.split('\n')
            file_name = lines[0]
            text_contents = '\n'.join(lines[2:])
            self._add_file(tar=tar,
                           name='{0}'.format(file_name),
                           contents=text_contents)
