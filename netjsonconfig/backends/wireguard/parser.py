import re
import tarfile
import io
from ..base.parser import BaseParser

vpn_pattern = re.compile(r'^\[Interface\]', flags=re.MULTILINE)
config_pattern = re.compile(r'^([^\s=]+)\s*=\s*(.*)$', flags=re.MULTILINE)
config_suffix = '.conf'


class WireguardParser(BaseParser):
    def parse_text(self, config):
        """
        Parses a WireGuard configuration text into a structured dictionary.
        """
        return self._get_config(config)

    def parse_tar(self, tar):
        """
        Parses a tar archive containing WireGuard configuration files.
        """
        parsed_configs = {}
        with tarfile.open(fileobj=io.BytesIO(tar), mode='r:*') as archive:
            for member in archive.getmembers():
                if member.isfile() and member.name.endswith(config_suffix):
                    file = archive.extractfile(member)
                    if file:
                        content = file.read().decode()
                        parsed_configs[member.name] = self._get_config(content)
        return parsed_configs

    def _get_vpns(self, text):
        """
        Extracts VPN sections from WireGuard config text.
        """
        vpn_sections = []
        sections = vpn_pattern.split(text)
        for section in sections[1:]:  # Ignore first split as it's before [Interface]
            vpn_sections.append(self._get_config(section.strip()))
        return vpn_sections

    def _get_config(self, contents):
        """
        Parses WireGuard config content into a structured dictionary.
        """
        config_data = {}
        current_section = None

        for line in contents.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Skip empty lines and comments

            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1].lower()
                config_data[current_section] = {}
            else:
                match = config_pattern.match(line)
                if match and current_section:
                    key, value = match.groups()
                    config_data[current_section][key] = value.strip()

        return config_data

