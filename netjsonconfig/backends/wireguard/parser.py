import re
import tarfile

from ...exceptions import ParseError
from ...utils import sorted_dict
from ..base.backend import BaseBackend
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
# wg and wg-quick match directive names case-insensitively,
# known names are normalized to the spelling used by the converter
known_directives = {
    name.lower(): name
    for name in (
        "PrivateKey",
        "ListenPort",
        "FwMark",
        "Address",
        "DNS",
        "MTU",
        "Table",
        "PreUp",
        "PostUp",
        "PreDown",
        "PostDown",
        "SaveConfig",
        "PublicKey",
        "PresharedKey",
        "AllowedIPs",
        "Endpoint",
        "PersistentKeepalive",
    )
}


class WireguardParser(BaseParser):
    def parse_text(self, config):
        return self._get_vpns(config)

    def parse_tar(self, tar):
        fileobj = tar.buffer if hasattr(tar, "buffer") else tar
        tar = tarfile.open(fileobj=fileobj)
        text = ""
        for member in tar.getmembers():
            # tunnels are generated in the root of the archive,
            # additional files (eg: "etc/app.conf") are not tunnels
            if "/" in member.name or not member.name.endswith(config_suffix):
                continue
            text += "# wireguard config: {name}\n\n{contents}\n".format(
                **{
                    "name": member.name.replace(config_suffix, ""),
                    "contents": tar.extractfile(member).read().decode(),
                }
            )
        return self.parse_text(text)

    def _get_vpns(self, text):
        # additional files rendered after the delimiter are not
        # WireGuard configuration and must not be parsed as such
        text = text.split(BaseBackend.FILE_SECTION_DELIMITER, 1)[0]
        results = re.split(vpn_pattern, text)
        # the tunnel name is only known from the "# wireguard config:"
        # marker, it cannot be inferred from a bare "[Interface]" block
        if results[0].strip():
            raise ParseError(
                "Each WireGuard configuration must start with "
                '"# wireguard config: <name>"'
            )
        vpns = []
        for result in results[1:]:
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
            key = known_directives.get(key.lower(), key)
            value = option.group(2).strip()
            if key in list_directives and current.get(key):
                value = f"{current[key]}, {value}" if value else current[key]
            current[key] = value
        if peers:
            config["peers"] = [sorted_dict(peer) for peer in peers]
        return sorted_dict(config)
