import re
import tarfile

from ...utils import sorted_dict
from ..base.parser import BaseParser

vpn_pattern = re.compile(r"^# wireguard config:\s", flags=re.MULTILINE)
config_pattern = re.compile(r"^([^\s]*) ?(.*)$")
config_suffix = ".conf"
# Wireguard uses an INI-like syntax: "[Interface]" appears once while
# "[Peer]" can be repeated, therefore sections must be tracked while
# parsing instead of reading each line as a standalone directive.
section_pattern = re.compile(r"^\[(\w+)\]$")
option_pattern = re.compile(r"^([^=]+)=(.*)$")
# directives which hold comma separated lists and may be repeated,
# all their occurrences are combined in a single comma separated value
list_directives = ("Address", "DNS", "AllowedIPs")


class WireguardParser(BaseParser):
    def parse_text(self, config):
        return self._get_vpns(config)

    def parse_tar(self, tar):
        fileobj = tar.buffer if hasattr(tar, "buffer") else tar
        tar = tarfile.open(fileobj=fileobj)
        text = ""
        for member in tar.getmembers():
            if not member.name.endswith(config_suffix):
                continue
            text += "# wireguard config: {name}\n\n{contents}\n".format(
                **{
                    "name": member.name.replace(config_suffix, ""),
                    "contents": tar.extractfile(member).read().decode(),
                }
            )
        return self.parse_text(text)

    def _get_vpns(self, text):
        results = re.split(vpn_pattern, text)
        vpns = []
        for result in results:
            result = result.strip()
            if not result:
                continue
            vpns.append(self._get_config(result))
        return {"wireguard": vpns}

    def _get_config(self, contents):
        lines = contents.split("\n")
        name = lines[0].strip()
        config = {"name": name}
        peers = []
        # options are collected into the section which precedes them
        current = config
        for line in lines[1:]:
            # like wg and wg-quick, ignore everything from "#" to the end of line
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            section = re.match(section_pattern, line)
            if section:
                if section.group(1).lower() == "peer":
                    current = {}
                    peers.append(current)
                else:
                    current = config
                continue
            option = re.match(option_pattern, line)
            if not option:
                continue
            key = option.group(1).strip()
            value = option.group(2).strip()
            if key in list_directives and current.get(key):
                value = f"{current[key]}, {value}" if value else current[key]
            current[key] = value
        if peers:
            config["peers"] = [sorted_dict(peer) for peer in peers]
        return sorted_dict(config)
