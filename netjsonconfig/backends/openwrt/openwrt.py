from jsonschema import ValidationError as JsonSchemaError

from ...exceptions import ValidationError
from ..base.backend import BaseBackend
from ..vxlan.vxlan_wireguard import VxlanWireguard
from ..wireguard.wireguard import Wireguard
from ..zerotier.zerotier import ZeroTier
from . import converters
from .parser import OpenWrtParser, config_path, packages_pattern
from .renderer import OpenWrtRenderer
from .schema import schema


class OpenWrt(BaseBackend):
    """
    OpenWRT / LEDE Configuration Backend
    """

    schema = schema
    converters = [
        converters.General,
        converters.Ntp,
        converters.Led,
        converters.Interfaces,
        converters.Routes,
        converters.Rules,
        converters.Switch,
        converters.Radios,
        converters.Wireless,
        converters.OpenVpn,
        converters.WireguardPeers,
        converters.ZeroTier,
        converters.Default,
    ]
    parser = OpenWrtParser
    renderer = OpenWrtRenderer
    list_identifiers = ["name", "config_value", "id"]
    list_identifiers_interfaces = {
        # Default identifiers, for backward compatibility
        None: list_identifiers,
        # VLANs use a composite key: different VLANs config objects are
        # merged only when their type, base device and VLAN ID match.
        "8021q": ["type", "name", "vid"],
        "8021ad": ["type", "name", "vid"],
    }

    def __init__(
        self, config=None, native=None, templates=None, context=None, dsa=True
    ):
        """
        :param config: ``dict`` containing a valid **NetJSON** configuration dictionary
        :param native: ``str`` or file object representing a native configuration that will
                       be parsed and converted to a **NetJSON** configuration dictionary
        :param templates: ``list`` containing **NetJSON** configuration dictionaries that
                          will be used as a base for the main config
        :param context: ``dict`` containing configuration variables
        :param dsa: ``bool`` flag to switch between OpenWrt configuration syntax.
                    ``True`` generates configuration in OpenWrt >21 syntax.
                    ``False`` generates configuration in OpenWrt <= 19 syntax.
        :raises TypeError: raised if ``config`` is not of type ``dict`` or if
                           ``templates`` is not of type ``list``
        """
        self.dsa = dsa
        super().__init__(config, native, templates, context)

    def validate(self):
        self._validate_radios()
        super().validate()
        self._validate_bridge_vlan_filtering()

    def _get_merge_config_identifiers(self, merging):
        """Returns interface-aware identifiers when merging interface lists.

        Allows handling special cases like VLANs."""
        if "interfaces" in merging:
            return self.list_identifiers_interfaces
        return self.list_identifiers

    def _generate_contents(self, tar):
        """
        Adds configuration files to tarfile instance.

        :param tar: tarfile instance
        :returns: None
        """
        uci = self.render(files=False)
        # create a list with all the packages (and remove empty entries)
        packages = packages_pattern.split(uci)
        if "" in packages:
            packages.remove("")
        # create an UCI file for each configuration package used
        for package in packages:
            lines = package.split("\n")
            package_name = lines[0]
            text_contents = "\n".join(lines[2:])
            self._add_file(
                tar=tar,
                name="{0}{1}".format(config_path, package_name),
                contents=text_contents,
            )

    @classmethod
    def wireguard_auto_client(cls, **kwargs):
        data = Wireguard.auto_client(**kwargs)
        config = {
            "interfaces": [
                {
                    "name": data["interface_name"],
                    "type": "wireguard",
                    "private_key": data["client"]["private_key"],
                    "port": data["client"]["port"],
                    # Default values for Wireguard Interface
                    "mtu": 1420,
                    "nohostroute": False,
                    "fwmark": "",
                    "ip6prefix": [],
                    "addresses": [],
                    "network": "",
                }
            ],
            "wireguard_peers": [
                {
                    "interface": data["interface_name"],
                    "public_key": data["server"]["public_key"],
                    "allowed_ips": data["server"]["allowed_ips"],
                    "endpoint_host": data["server"]["endpoint_host"],
                    "endpoint_port": data["server"]["endpoint_port"],
                    # Default values for Wireguard Peers
                    "preshared_key": "",
                    "persistent_keepalive": 60,
                    "route_allowed_ips": True,
                }
            ],
        }
        if data["client"]["ip_address"]:
            config["interfaces"][0]["addresses"] = [
                {
                    "proto": "static",
                    "family": "ipv4",
                    "address": data["client"]["ip_address"],
                    "mask": 32,
                },
            ]
        return config

    @classmethod
    def vxlan_wireguard_auto_client(cls, **kwargs):
        config = cls.wireguard_auto_client(**kwargs)
        vxlan_config = VxlanWireguard.auto_client(**kwargs)
        vxlan_interface = {
            "name": vxlan_config["name"],
            "type": "vxlan",
            "vtep": vxlan_config["server_ip_address"],
            "port": 4789,
            "vni": vxlan_config["vni"],
            "tunlink": config["interfaces"][0]["name"],
            # Default values for VXLAN interface
            "rxcsum": True,
            "txcsum": True,
            "mtu": 1280,
            "ttl": 64,
            "mac": "",
            "disabled": False,
            "network": "",
        }
        config["interfaces"].append(vxlan_interface)
        return config

    @classmethod
    def zerotier_auto_client(cls, **kwargs):
        data = ZeroTier.auto_client(**kwargs)
        return {"zerotier": [data]}

    def _validate_radios(self):
        """
        Predict radio frequency from the ``hwmode`` or ``band`` property.

        If both properties are absent, the channel is used instead. A channel
        set to ``auto`` (0) does not provide enough information to predict the
        radio frequency.
        """
        for radio in self.config.get("radios", []):
            if radio["protocol"] not in ["802.11n", "802.11ax"]:
                continue
            if (
                radio.get("band") is None
                and radio.get("hwmode") is None
                and radio.get("channel") == 0
            ):
                raise JsonSchemaError(
                    '"channel" cannot be set to "auto" when'
                    ' "hwmode" or "band" property is not configured.'
                )

    def _validate_bridge_vlan_filtering(self):
        """
        When VLAN filtering is enabled on a bridge, a primary VLAN ID can be
        set only once per port.
        """
        for index, interface in enumerate(self.config.get("interfaces", [])):
            pvid_mapping = []
            if interface.get("type") != "bridge":
                continue
            for vlan in interface.get("vlan_filtering", []):
                for port in vlan.get("ports", []):
                    if port.get("primary_vid", False):
                        if port["ifname"] in pvid_mapping:
                            raise ValidationError(
                                JsonSchemaError(
                                    f'Invalid configuration triggered by "#/interfaces/{index}"'
                                    " says: Primary VID can be set only one VLAN for a port."
                                )
                            )
                        pvid_mapping.append(port["ifname"])
