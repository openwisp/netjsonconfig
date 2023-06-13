import re
import tarfile
from json import loads

from ..base.parser import BaseParser

vpn_pattern = re.compile('^// zerotier controller config:\s', flags=re.MULTILINE)
config_pattern = re.compile('^([^\s]*) ?(.*)$')
config_suffix = '.json'


class ZeroTierParser(BaseParser):
    def parse_text(self, config):
        return {'zerotier': self._get_vpn_config(config)}

    def parse_tar(self, tar):
        fileobj = tar.buffer if hasattr(tar, 'buffer') else tar
        tar = tarfile.open(fileobj=fileobj)
        text = ''
        for member in tar.getmembers():
            if not member.name.endswith(config_suffix):
                continue
            text += '// zerotier controller config: {name}\n\n{contents}\n'.format(
                **{
                    'name': member.name,
                    'contents': tar.extractfile(member).read().decode(),
                }
            )
        return self.parse_text(text)

    def _get_vpn_config(self, text):
        vpn_configs = []
        vpn_instances = vpn_pattern.split(text)
        if '' in vpn_instances:
            vpn_instances.remove('')
        for vpn in vpn_instances:
            lines = vpn.split('\n')
            text_contents = '\n'.join(lines[2:])
            vpn_configs.append(loads(text_contents))
        return vpn_configs
