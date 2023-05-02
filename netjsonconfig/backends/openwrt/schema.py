"""
OpenWrt specific JSON-Schema definition
"""
from ...schema import schema as default_schema
from ...utils import merge_config
from ..openvpn.schema import base_openvpn_schema
from ..wireguard.schema import base_wireguard_schema
from .timezones import timezones

default_radio_driver = "mac80211"

wireguard = base_wireguard_schema["properties"]["wireguard"]["items"]["properties"]
wireguard_peers = wireguard["peers"]["items"]["properties"]
interface_settings = default_schema["definitions"]["interface_settings"]["properties"]

# The following regex will match against a single valid port, or a port range e.g. 1234-5000
port_range_regex = "(^(?=\s*$))|(^(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[0-9]{1,4})$|^(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[0-9]{1,4})-(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[0-9]{1,4})$)"  # noqa

# Match against a MAC address
mac_address_regex = "(^(?=\s*$))|(^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$)"

# Match against a yyyy-mm-dd format date. Note that draft07 of the JSON schema standard
# include a "date" pattern which can replace this.
# https://json-schema.org/understanding-json-schema/reference/string.html
date_regex = "(^(?=\s*$))|(^([0-9]{4})-(0[1-9]|[12][0-9]|3[01])-([012][0-9]|[3][01])$)"

# Match against a time in the format hh:mm:ss
time_regex = "(^(?=\s*$))|(^([01][0-9]|2[0123])(:([012345][0-9])){2}$)"

# Match against a range of IPv4 addresses
ipv4_cidr_regex = (
    "(^(?=\s*$))|(^([0-9]{1,3}.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))?$)"
)

# Match against a negatable range of IPv4 addresses. This variant allows for an optional
# "!" in front of the CIDR.
ipv4_negatable_cidr_regex = (
    "(^(?=\s*$))|(^!?([0-9]{1,3}.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))?$)"
)

# Match against a range of IPv6 addresses
ipv6_cidr_regex = "(^(?=\s*$))|(^s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:)))(%.+)?s*(\/([0-9]|[1-9][0-9]|1[0-1][0-9]|12[0-8]))?$)"  # noqa

ipv4_and_ipv6_cidr_regex = "(^(?=\s*$))|((^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))?$)|(^s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:)))(%.+)?s*(\/([0-9]|[1-9][0-9]|1[0-1][0-9]|12[0-8]))?)$)"  # noqa

schema = merge_config(
    default_schema,
    {
        "definitions": {
            "base_interface_settings": {
                "properties": {
                    "network": {
                        "type": "string",
                        "description": "logical interface name in UCI (OpenWRT configuration format), "
                        "will be automatically generated if left blank",
                        "maxLength": 15,
                        "pattern": "^[a-zA-z0-9_\\.\\-]*$",
                        "propertyOrder": 7,
                    }
                }
            },
            "wireless_interface": {
                "properties": {
                    "wireless": {
                        "properties": {
                            "network": {
                                "type": "array",
                                "title": "Attached Networks",
                                "description": "override OpenWRT \"network\" config option of of wifi-iface "
                                "directive; will be automatically determined if left blank",
                                "uniqueItems": True,
                                "additionalItems": True,
                                "items": {
                                    "title": "network",
                                    "type": "string",
                                    "$ref": "#/definitions/base_interface_settings/properties/network",
                                },
                                "propertyOrder": 19,
                            }
                        }
                    }
                }
            },
            "ap_wireless_settings": {
                "allOf": [
                    {
                        "properties": {
                            "wmm": {
                                "type": "boolean",
                                "title": "WMM (802.11e)",
                                "description": "enables WMM (802.11e) support; "
                                "required for 802.11n support",
                                "default": True,
                                "format": "checkbox",
                                "propertyOrder": 8,
                            },
                            "isolate": {
                                "type": "boolean",
                                "title": "isolate clients",
                                "description": "isolate wireless clients from one another",
                                "default": False,
                                "format": "checkbox",
                                "propertyOrder": 9,
                            },
                            "ieee80211r": {
                                "type": "boolean",
                                "title": "roaming",
                                "description": "enables fast BSS transition (802.11r) support",
                                "default": False,
                                "format": "checkbox",
                                "propertyOrder": 9,
                            },
                            "reassociation_deadline": {
                                "type": "integer",
                                "title": "reassociation deadline",
                                "description": (
                                    "reassociation deadline in time units "
                                    "(TUs / 1.024 ms, 1000-65535)"
                                ),
                                "default": 1000,
                                "minimum": 1000,
                                "maximum": 65535,
                                "propertyOrder": 9,
                            },
                            "ft_psk_generate_local": {
                                "type": "boolean",
                                "title": "FT PSK generate local",
                                "description": "whether to generate FT response locally for PSK networks",
                                "default": False,
                                "format": "checkbox",
                                "propertyOrder": 9,
                            },
                            "ft_over_ds": {
                                "type": "boolean",
                                "title": "FT-over-DS",
                                "description": "whether to enable FT-over-DS",
                                "default": True,
                                "format": "checkbox",
                                "propertyOrder": 9,
                            },
                            "rsn_preauth": {
                                "type": "boolean",
                                "title": "WPA2-EAP pre-authentication",
                                "description": "allow preauthentication for WPA2-EAP networks",
                                "default": False,
                                "format": "checkbox",
                                "propertyOrder": 9,
                            },
                            "macfilter": {
                                "type": "string",
                                "title": "MAC Filter",
                                "description": "specifies the mac filter policy, \"disable\" to disable "
                                "the filter, \"allow\" to treat it as whitelist or "
                                "\"deny\" to treat it as blacklist",
                                "enum": ["disable", "allow", "deny"],
                                "default": "disable",
                                "propertyOrder": 15,
                            },
                            "maclist": {
                                "type": "array",
                                "title": "MAC List",
                                "description": "mac addresses that will be filtered according to the policy "
                                "specified in the \"macfilter\" option",
                                "propertyOrder": 16,
                                "items": {
                                    "type": "string",
                                    "title": "MAC address",
                                    "pattern": "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
                                    "minLength": 17,
                                    "maxLength": 17,
                                },
                            },
                        }
                    }
                ]
            },
            "bridge_interface": {
                "allOf": [
                    {
                        "properties": {
                            "igmp_snooping": {
                                "type": "boolean",
                                "title": "IGMP snooping",
                                "description": "sets the \"multicast_snooping\" kernel setting for a bridge",
                                "default": False,
                                "format": "checkbox",
                                "propertyOrder": 5,
                            },
                            "multicast_querier": {
                                "type": "boolean",
                                "title": "IGMP multicast querier",
                                "description": (
                                    "enables the bridge as a multicast querier"
                                ),
                                "default": False,
                                "format": "checkbox",
                                "propertyOrder": 5,
                            },
                            "query_interval": {
                                "type": "integer",
                                "title": "IGMP query interval",
                                "description": (
                                    "time interval in centiseconds between"
                                    " multicast general queries"
                                ),
                                "default": 12500,
                                "propertyOrder": 5,
                            },
                            "query_response_interval": {
                                "type": "integer",
                                "title": "IGMP query response interval",
                                "description": (
                                    "the max response time in centiseconds inserted into"
                                    " the periodic general queries"
                                ),
                                "default": 1000,
                                "propertyOrder": 5,
                            },
                            "last_member_interval": {
                                "type": "integer",
                                "title": "IGMP last member interval",
                                "description": (
                                    "the maximum response time in centiseconds inserted into"
                                    " group-specific queries sent in response to leave group messages."
                                ),
                                "default": 100,
                                "propertyOrder": 5,
                            },
                            "hash_max": {
                                "type": "integer",
                                "title": "IGMP hash max",
                                "description": "size of kernel multicast hash table",
                                "default": 512,
                                "propertyOrder": 5,
                            },
                            "robustness": {
                                "type": "integer",
                                "title": "IGMP Robustness",
                                "description": "sets Startup Query Count and Last Member Count",
                                "default": 2,
                                "propertyOrder": 5,
                            },
                            "forward_delay": {
                                "type": "integer",
                                "title": "STP forward delay",
                                "description": (
                                    "time in seconds to spend in listening"
                                    " and learning states"
                                ),
                                "default": 4,
                                "minimum": 2,
                                "maximum": 30,
                                "propertyOrder": 4,
                            },
                            "hello_time": {
                                "type": "integer",
                                "title": "STP hello time",
                                "description": "time interval in seconds for STP hello packets",
                                "default": 2,
                                "minimum": 1,
                                "maximum": 10,
                                "propertyOrder": 4,
                            },
                            "priority": {
                                "type": "integer",
                                "title": "STP priority",
                                "description": "STP bridge priority",
                                "default": 32767,
                                "minimum": 0,
                                "maximum": 65535,
                                "propertyOrder": 4,
                            },
                            "ageing_time": {
                                "type": "integer",
                                "title": "STP ageing time",
                                "description": (
                                    "expiration time in seconds for dynamic MAC"
                                    " entries in the filtering DB"
                                ),
                                "default": 300,
                                "minimum": 10,
                                "maximum": 1000000,
                                "propertyOrder": 4,
                            },
                            "max_age": {
                                "type": "integer",
                                "title": "STP max age",
                                "description": (
                                    "timeout in seconds until topology updates on link loss"
                                ),
                                "default": 20,
                                "minimum": 0,
                                "maximum": 40,
                                "propertyOrder": 4,
                            },
                        }
                    }
                ]
            },
            "dialup_interface": {
                "title": "Dialup interface",
                "required": ["proto", "username", "password"],
                "allOf": [
                    {
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["dialup"],
                                "default": "dialup",
                                "propertyOrder": 1,
                            },
                            "proto": {
                                "type": "string",
                                "title": "protocol",
                                "enum": [
                                    "3g",
                                    "6in4",
                                    "aiccu",
                                    "l2tp",
                                    "ncm",
                                    "ppp",
                                    "pppoa",
                                    "pppoe",
                                    "pptp",
                                    "qmi",
                                    "wwan",
                                ],
                                "default": "pppoe",
                                "propertyOrder": 1.1,
                            },
                            "username": {
                                "type": "string",
                                "description": "username for authentication in protocols like PPPoE",
                                "propertyOrder": 9,
                            },
                            "password": {
                                "type": "string",
                                "description": "password for authentication in protocols like PPPoE",
                                "propertyOrder": 10,
                            },
                        }
                    },
                    {"$ref": "#/definitions/base_interface_settings"},
                    {"$ref": "#/definitions/interface_settings"},
                ],
            },
            "modemmanager_interface": {
                "type": "object",
                "title": "Modem manager interface",
                "required": ["name", "device"],
                "allOf": [
                    {
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["modem-manager"],
                                "default": "dialup",
                                "propertyOrder": 1,
                            },
                            "apn": {
                                "type": "string",
                                "title": "APN",
                                "propertyOrder": 1.1,
                            },
                            "pin": {
                                "type": "string",
                                "title": "PIN code",
                                "propertyOrder": 1.2,
                            },
                            "device": {
                                "type": "string",
                                "description": "Leave blank to use the hardware default",
                                "propertyOrder": 1.3,
                            },
                            "username": {"type": "string", "propertyOrder": 1.4},
                            "password": {"type": "string", "propertyOrder": 1.5},
                            "metric": {
                                "type": "integer",
                                "default": 50,
                                "propertyOrder": 1.6,
                            },
                            "iptype": {
                                "type": "string",
                                "title": "IP type",
                                "default": "ipv4",
                                "enum": ["ipv4", "ipv6", "ipv4v6"],
                                "options": {
                                    "enum_titles": ["IPv4", "IPv6", "IPv4 and IPv6"]
                                },
                                "propertyOrder": 1.7,
                            },
                            "lowpower": {
                                "type": "boolean",
                                "title": "Low power mode",
                                "format": "checkbox",
                                "default": False,
                                "propertyOrder": 1.8,
                            },
                            "signalrate": {
                                "type": "integer",
                                "title": "Signal refresh rate",
                                "propertyOrder": 1.9,
                                "description": "singal refresh rate in seconds",
                            },
                        }
                    },
                    {"$ref": "#/definitions/base_interface_settings"},
                ],
            },
            "wireguard_interface": {
                "type": "object",
                "title": "Wireguard interface",
                "required": ["private_key"],
                "additionalProperties": True,
                "allOf": [
                    {
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["wireguard"],
                                "default": "wireguard",
                                "propertyOrder": 1,
                            },
                            "private_key": wireguard["private_key"],
                            "port": wireguard["port"],
                            "mtu": {
                                "type": "integer",
                                "default": 1420,
                                "propertyOrder": 1.1,
                            },
                            "nohostroute": {
                                "type": "boolean",
                                "format": "checkbox",
                                "default": False,
                                "title": "no host route",
                                "description": (
                                    "Do not add routes to ensure the tunnel "
                                    "endpoints are routed via non-tunnel device"
                                ),
                                "propertyOrder": 3,
                            },
                            "fwmark": {
                                "type": "string",
                                "title": "firewall mark",
                                "description": (
                                    "Firewall mark to apply to tunnel endpoint packets, "
                                    "will be automatically determined if left blank"
                                ),
                                "propertyOrder": 3.1,
                            },
                            "ip6prefix": {
                                "title": "IPv6 prefixes",
                                "description": "IPv6 prefixes to delegate to other interfaces",
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "title": "IPv6 prefix",
                                    "uniqueItems": True,
                                },
                                "propertyOrder": 9,
                            },
                            # unfortunately some duplication with the base IP address
                            # definition is needed to achieve functional usability and
                            # consistency with the rest of the schema because the
                            # wireguard OpenWRT package uses a different configuration
                            # format for addresses
                            "addresses": {
                                "type": "array",
                                "title": "addresses",
                                "uniqueItems": True,
                                "propertyOrder": 20,
                                "items": {
                                    "required": ["proto", "family", "address", "mask"],
                                    "title": "address",
                                    "oneOf": [
                                        {
                                            "type": "object",
                                            "title": "ipv4",
                                            "properties": {
                                                "proto": {
                                                    "title": "protocol",
                                                    "type": "string",
                                                    "propertyOrder": 1,
                                                    "enum": ["static"],
                                                },
                                                "family": {
                                                    "title": "family",
                                                    "type": "string",
                                                    "propertyOrder": 2,
                                                    "enum": ["ipv4"],
                                                },
                                                "address": {
                                                    "type": "string",
                                                    "title": "ipv4 address",
                                                    "minLength": 7,
                                                    "propertyOrder": 3,
                                                },
                                                "mask": {
                                                    "type": "number",
                                                    "minimum": 8,
                                                    "maxmium": 32,
                                                    "default": 32,
                                                },
                                            },
                                        },
                                        {
                                            "type": "object",
                                            "title": "ipv6",
                                            "properties": {
                                                "proto": {
                                                    "title": "protocol",
                                                    "type": "string",
                                                    "propertyOrder": 1,
                                                    "enum": ["static"],
                                                },
                                                "family": {
                                                    "title": "family",
                                                    "type": "string",
                                                    "propertyOrder": 2,
                                                    "enum": ["ipv6"],
                                                },
                                                "address": {
                                                    "type": "string",
                                                    "title": "ipv6 address",
                                                    "minLength": 3,
                                                    "format": "ipv6",
                                                    "propertyOrder": 3,
                                                },
                                                "mask": {
                                                    "type": "number",
                                                    "minimum": 4,
                                                    "maxmium": 128,
                                                    "default": 128,
                                                },
                                            },
                                        },
                                    ],
                                },
                            },
                        }
                    },
                    {"$ref": "#/definitions/base_interface_settings"},
                ],
            },
            "vxlan_interface": {
                "title": "VXLAN interface",
                "required": ["vtep", "port", "vni", "tunlink"],
                "allOf": [
                    {
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["vxlan"],
                                "default": "vxlan",
                                "propertyOrder": 1,
                            },
                            "vtep": {
                                "type": "string",
                                "title": "VTEP",
                                "description": "VXLAN Tunnel End Point",
                                "propertyOrder": 1.1,
                            },
                            "port": {
                                "type": "integer",
                                "propertyOrder": 1.2,
                                "default": 4789,
                                "minimum": 1,
                                "maximum": 65535,
                            },
                            "vni": {
                                "type": ["integer", "string"],
                                "title": "VNI",
                                "description": "VXLAN Network Identifier",
                                "propertyOrder": 1.3,
                                "minimum": 1,
                                "maximum": 16777216,
                            },
                            "tunlink": {
                                "type": "string",
                                "title": "TUN link",
                                "description": "Interface to which the VXLAN tunnel will be bound",
                                "propertyOrder": 1.4,
                            },
                            "rxcsum": {
                                "type": "boolean",
                                "title": "RX checksum validation",
                                "description": "Use checksum validation in RX (receiving) direction",
                                "default": True,
                                "format": "checkbox",
                                "propertyOrder": 1.5,
                            },
                            "txcsum": {
                                "type": "boolean",
                                "title": "TX checksum validation",
                                "description": "Use checksum validation in TX (transmission) direction",
                                "default": True,
                                "format": "checkbox",
                                "propertyOrder": 1.6,
                            },
                            "mtu": {"type": "integer", "default": 1280},
                            "ttl": {
                                "type": "integer",
                                "title": "TTL",
                                "description": "TTL of the encapsulation packets",
                                "default": 64,
                                "propertyOrder": 3,
                            },
                            "mac": interface_settings["mac"],
                        }
                    },
                    {"$ref": "#/definitions/base_interface_settings"},
                ],
            },
            "base_radio_settings": {
                "properties": {
                    "driver": {
                        "type": "string",
                        "enum": ["mac80211", "atheros", "ath5k", "ath9k", "broadcom"],
                        "default": default_radio_driver,
                        "propertyOrder": 2,
                    }
                }
            },
            "radio_hwmode_11g": {
                "properties": {
                    "hwmode": {
                        "type": "string",
                        "title": "hardware mode",
                        "readOnly": True,
                        "propertyOrder": 8,
                        "default": "11g",
                        "enum": ["11g"],
                    }
                }
            },
            "radio_hwmode_11a": {
                "properties": {
                    "hwmode": {
                        "type": "string",
                        "title": "hardware mode",
                        "readOnly": True,
                        "propertyOrder": 8,
                        "default": "11a",
                        "enum": ["11a"],
                    }
                }
            },
            "radio_80211gn_settings": {
                "allOf": [{"$ref": "#/definitions/radio_hwmode_11g"}]
            },
            "radio_80211an_settings": {
                "allOf": [{"$ref": "#/definitions/radio_hwmode_11a"}]
            },
            "radio_80211ac_5ghz_settings": {
                "allOf": [{"$ref": "#/definitions/radio_hwmode_11a"}]
            },
            "radio_80211ax_2ghz_settings": {
                "allOf": [{"$ref": "#/definitions/radio_hwmode_11g"}]
            },
            "radio_80211ax_5ghz_settings": {
                "allOf": [{"$ref": "#/definitions/radio_hwmode_11a"}]
            },
        },
        "properties": {
            "general": {
                "properties": {
                    "timezone": {"enum": list(timezones.keys()), "default": "UTC"}
                }
            },
            "interfaces": {
                "items": {
                    "oneOf": [
                        {"$ref": "#/definitions/dialup_interface"},
                        {"$ref": "#/definitions/modemmanager_interface"},
                        {"$ref": "#/definitions/vxlan_interface"},
                        {"$ref": "#/definitions/wireguard_interface"},
                    ]
                }
            },
            "routes": {
                "items": {
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": [
                                "unicast",
                                "local",
                                "broadcast",
                                "multicast",
                                "unreachable",
                                "prohibit",
                                "blackhole",
                                "anycast",
                            ],
                            "default": "unicast",
                            "propertyOrder": 0,
                        },
                        "mtu": {
                            "type": "string",
                            "title": "MTU",
                            "propertyOrder": 6,
                            "pattern": "^[0-9]*$",
                        },
                        "table": {
                            "type": "string",
                            "propertyOrder": 7,
                            "pattern": "^[0-9]*$",
                        },
                        "onlink": {
                            "type": "boolean",
                            "default": False,
                            "format": "checkbox",
                            "propertyOrder": 8,
                        },
                    }
                }
            },
            "ip_rules": {
                "type": "array",
                "title": "Policy routing",
                "uniqueItems": True,
                "additionalItems": True,
                "propertyOrder": 7,
                "items": {
                    "type": "object",
                    "title": "IP rule",
                    "additionalProperties": True,
                    "properties": {
                        "in": {
                            "type": "string",
                            "title": "incoming interface",
                            "propertyOrder": 1,
                        },
                        "out": {
                            "type": "string",
                            "title": "outgoing interface",
                            "propertyOrder": 2,
                        },
                        "src": {
                            "type": "string",
                            "title": "source subnet",
                            "description": "(CIDR notation)",
                            "propertyOrder": 3,
                            "format": "cidr",
                        },
                        "dest": {
                            "type": "string",
                            "title": "destination subnet",
                            "description": "(CIDR notation)",
                            "propertyOrder": 4,
                            "format": "cidr",
                        },
                        "tos": {
                            "type": "integer",
                            "title": "TOS",
                            "description": "TOS value to match in IP headers",
                            "propertyOrder": 5,
                        },
                        "mark": {
                            "type": "string",
                            "description": "TOS value to match in IP headers",
                            "propertyOrder": 6,
                        },
                        "lookup": {
                            "type": "string",
                            "description": "routing table ID or symbolic link alias",
                            "propertyOrder": 7,
                        },
                        "action": {
                            "type": "string",
                            "enum": ["prohibit", "unreachable", "blackhole", "throw"],
                            "propertyOrder": 8,
                        },
                        "goto": {"type": "integer", "propertyOrder": 9},
                        "invert": {
                            "type": "boolean",
                            "default": False,
                            "format": "checkbox",
                            "propertyOrder": 10,
                        },
                    },
                },
            },
            "ntp": {
                "type": "object",
                "title": "NTP Settings",
                "additionalProperties": True,
                "propertyOrder": 8,
                "properties": {
                    "enabled": {
                        "type": "boolean",
                        "title": "enable NTP client",
                        "default": True,
                        "format": "checkbox",
                        "propertyOrder": 1,
                    },
                    "enable_server": {
                        "type": "boolean",
                        "title": "enable NTP server",
                        "default": False,
                        "format": "checkbox",
                        "propertyOrder": 2,
                    },
                    "server": {
                        "title": "NTP Servers",
                        "description": "NTP server candidates",
                        "type": "array",
                        "uniqueItems": True,
                        "additionalItems": True,
                        "propertyOrder": 3,
                        "items": {
                            "title": "NTP server",
                            "type": "string",
                            "format": "hostname",
                        },
                        "default": [
                            "0.openwrt.pool.ntp.org",
                            "1.openwrt.pool.ntp.org",
                            "2.openwrt.pool.ntp.org",
                            "3.openwrt.pool.ntp.org",
                        ],
                    },
                },
            },
            "switch": {
                "type": "array",
                "uniqueItems": True,
                "additionalItems": True,
                "title": "Programmable Switch",
                "propertyOrder": 9,
                "items": {
                    "title": "Switch",
                    "type": "object",
                    "additionalProperties": True,
                    "required": ["name", "reset", "enable_vlan", "vlan"],
                    "properties": {
                        "name": {"type": "string", "propertyOrder": 1},
                        "reset": {
                            "type": "boolean",
                            "default": True,
                            "format": "checkbox",
                            "propertyOrder": 2,
                        },
                        "enable_vlan": {
                            "type": "boolean",
                            "title": "enable vlan",
                            "default": True,
                            "format": "checkbox",
                            "propertyOrder": 3,
                        },
                        "vlan": {
                            "type": "array",
                            "title": "VLANs",
                            "uniqueItems": True,
                            "additionalItems": True,
                            "propertyOrder": 4,
                            "items": {
                                "type": "object",
                                "title": "VLAN",
                                "additionalProperties": True,
                                "required": ["device", "vlan", "ports"],
                                "properties": {
                                    "device": {"type": "string", "propertyOrder": 1},
                                    "vlan": {"type": "integer", "propertyOrder": 2},
                                    "ports": {"type": "string", "propertyOrder": 3},
                                },
                            },
                        },
                    },
                },
            },
            "led": {
                "type": "array",
                "title": "LEDs",
                "uniqueItems": True,
                "additionalItems": True,
                "propertyOrder": 10,
                "items": {
                    "type": "object",
                    "title": "LED",
                    "additionalProperties": True,
                    "required": ["name", "sysfs", "trigger"],
                    "properties": {
                        "name": {"type": "string", "propertyOrder": 1},
                        "default": {
                            "type": "boolean",
                            "format": "checkbox",
                            "propertyOrder": 2,
                        },
                        "dev": {"type": "string", "propertyOrder": 3},
                        "sysfs": {"type": "string", "propertyOrder": 4},
                        "trigger": {"type": "string", "propertyOrder": 5},
                        "delayoff": {"type": "integer", "propertyOrder": 6},
                        "delayon": {"type": "integer", "propertyOrder": 7},
                        "interval": {"type": "integer", "propertyOrder": 8},
                        "message": {"type": "string", "propertyOrder": 9},
                        "mode": {"type": "string", "propertyOrder": 10},
                    },
                },
            },
            "wireguard_peers": {
                "type": "array",
                "title": "Wireguard Peers",
                "uniqueItems": True,
                "propertyOrder": 13,
                "items": {
                    "type": "object",
                    "title": "Wireguard peer",
                    "additionalProperties": True,
                    "required": ["interface", "public_key", "allowed_ips"],
                    "properties": {
                        "interface": {
                            "type": "string",
                            "title": "interface",
                            "description": "name of the wireguard interface",
                            "minLength": 2,
                            "maxLength": 15,
                            "pattern": "^[^\\s]*$",
                            "propertyOrder": 0,
                        },
                        "public_key": wireguard_peers["public_key"],
                        "allowed_ips": {
                            "type": "array",
                            "title": "allowed IPs",
                            "propertyOrder": 2,
                            "uniqueItems": True,
                            "items": {
                                "type": "string",
                                "title": "IP/prefix",
                                "minLength": 1,
                            },
                        },
                        "endpoint_host": wireguard_peers["endpoint_host"],
                        "endpoint_port": wireguard_peers["endpoint_port"],
                        "preshared_key": wireguard_peers["preshared_key"],
                        "persistent_keepalive": {
                            "type": "integer",
                            "title": "keep alive",
                            "description": (
                                "Number of second between keepalive "
                                "messages, 0 means disabled"
                            ),
                            "default": 0,
                            "propertyOrder": 6,
                        },
                        "route_allowed_ips": {
                            "type": "boolean",
                            "format": "checkbox",
                            "title": "route allowed IPs",
                            "description": (
                                "Automatically create a route for "
                                "each Allowed IPs for this peer"
                            ),
                            "default": False,
                            "propertyOrder": 7,
                        },
                    },
                },
            },
        },
    },
)

firewall_definitions = {
    "name": {
        "type": "string",
        "title": "Name",
        "description": "Name of redirect",
        "propertyOrder": 1,
    },
    "enabled": {
        "type": "boolean",
        "title": "Enable",
        "description": "Enable this configuration entity.",
        "default": True,
        "format": "checkbox",
        "propertyOrder": 2,
    },
    "zone_name": {
        "type": "string",
        "title": "Zone name",
        "description": "A unique zone name. Has a maximum" "length of 11 characters.",
        "maxLength": 11,
        "propertyOrder": 3,
    },
    "ipv4_cidr": {
        "type": "string",
        "pattern": ipv4_cidr_regex,
    },
    "ipv4_negatable_cidr": {
        "type": "string",
        "pattern": ipv4_negatable_cidr_regex,
    },
    "src": {
        "type": "string",
        "title": "Source zone",
        "description": "Specifies the traffic source zone. "
        "Must refer to one of the defined zone names. "
        "For typical port forwards this usually is wan.",
        "maxLength": 11,
        "propertyOrder": 4,
    },
    "src_ip": {
        "type": "array",
        "title": "Source address",
        "description": "Match incoming traffic from the specified source ip "
        "address.",
        "uniqueItems": True,
        "items": {
            "title": "Source adress",
            "type": "string",
            "pattern": ipv4_and_ipv6_cidr_regex,
        },
        "propertyOrder": 5,
    },
    "src_mac": {
        "type": "string",
        "title": "Source MAC address",
        "description": "Match incoming traffic from the specified MAC address.",
        "pattern": mac_address_regex,
        "propertyOrder": 6,
    },
    "src_port": {
        "type": "string",
        "title": "Source port",
        "description": "Match incoming traffic originating from the given source "
        "port or port range on the client host.",
        "pattern": port_range_regex,
        "propertyOrder": 7,
    },
    "proto": {
        "type": "array",
        "title": "Protocol",
        "description": "Match incoming traffic using the given protocol. "
        "Can be one of tcp, udp, tcpudp, udplite, icmp, esp, "
        "ah, sctp, or all or it can be a numeric value, "
        "representing one of these protocols or a different one. "
        "A protocol name from /etc/protocols is also allowed. "
        "The number 0 is equivalent to all",
        "default": ["tcp", "udp"],
        "propertyOrder": 8,
        "items": {"title": "Protocol type", "type": "string"},
    },
    "dest": {
        "type": "string",
        "title": "Destination zone",
        "description": "Specifies the traffic destination zone. Must refer to "
        "on of the defined zone names. For DNAT target on Attitude Adjustment, "
        'NAT reflection works only if this is equal to "lan".',
        "maxLength": 11,
        "propertyOrder": 9,
    },
    "dest_ip": {
        "type": "array",
        "title": "Destination address",
        "description": "For DNAT, redirect matches incoming traffic to the "
        "specified internal host. For SNAT, it matches traffic directed at "
        "the given address. For DNAT, if the dest_ip is not specified, the rule "
        "is translated in a iptables/REDIRECT rule, otherwise it is a "
        "iptables/DNAT rule.",
        "items": {
            "title": "dest_ip",
            "type": "string",
            "pattern": ipv4_and_ipv6_cidr_regex,
        },
        "propertyOrder": 10,
    },
    "dest_port": {
        "type": "string",
        "title": "Destination port",
        "description": "For DNAT, redirect matched incoming traffic to the given "
        "port on the internal host. For SNAT, match traffic directed at the "
        "given ports. Only a single port or range can be specified.",
        "pattern": port_range_regex,
        "propertyOrder": 11,
    },
    "ipset": {
        "type": "string",
        "title": "IP Set",
        "description": "Match traffic against the given ipset. The match can be "
        "inverted by prefixing the value with an exclamation mark.",
        "propertyOrder": 12,
    },
    "mark": {
        "type": "string",
        "title": "Match mark",
        "description": 'Match traffic against the given firewall mark, e.g. '
        '"0xFF" to match mark 255 or "0x0/0x1" to match any even mark value. '
        'The match can be inverted by prefixing the value with an exclamation '
        'mark, e.g. "!0x10" to match all but mark #16.',
        "propertyOrder": 13,
    },
    "start_date": {
        "type": "string",
        "title": "Start date",
        "description": "Only match traffic after the given date (inclusive).",
        "pattern": date_regex,
        # "format": "date", TODO: replace pattern with this
        # when adopt draft07
        "propertyOrder": 14,
    },
    "stop_date": {
        "type": "string",
        "title": "Stop date",
        "description": "Only match traffic before the given date (inclusive).",
        "pattern": date_regex,
        # "format": "date", TODO: replace pattern with this
        # when adopt draft07
        "propertyOrder": 15,
    },
    "start_time": {
        "type": "string",
        "title": "Start time",
        "description": "Only match traffic after the given time of day " "(inclusive).",
        "pattern": time_regex,
        "propertyOrder": 16,
    },
    "stop_time": {
        "type": "string",
        "title": "Stop time",
        "description": "Only match traffic before the given time of day "
        "(inclusive).",
        "pattern": time_regex,
        "propertyOrder": 17,
    },
    # Note: here we don't support negation of values like
    # the UCI syntax does, as it's not necessary.
    "weekdays": {
        "type": "array",
        "title": "Weekdays",
        "description": "Only match traffic during the given week days, "
        'e.g. ["sun", "mon", "thu", "fri"] to only match on Sundays, '
        "Mondays, Thursdays and Fridays.",
        "propertyOrder": 18,
        "items": {
            "type": "string",
            "title": "Weekday",
            "enum": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
        },
    },
    # Note: here we don't support negation of values like
    # the UCI syntax does, as it's not necessary.
    "monthdays": {
        "type": "array",
        "title": "Monthdays",
        "description": "Only match traffic during the given days of the "
        "month, e.g. [2, 5, 30] to only match on every 2nd, 5th and 30th "
        "day of the month.",
        "propertyOrder": 19,
        "items": {
            "type": "integer",
            "title": "day of month",
            "minimum": 1,
            "maximum": 31,
        },
    },
    "utc_time": {
        "type": "boolean",
        "title": "UTC time",
        "description": "Treat all given time values as UTC time instead of local "
        "time.",
        "default": False,
        "propertyOrder": 20,
    },
    "family": {
        "type": "string",
        "title": "Family",
        "description": "Protocol family (ipv4, ipv6 or any) to generate iptables "
        "rules for",
        "enum": ["ipv4", "ipv6", "any"],
        "default": "any",
        "propertyOrder": 22,
    },
    "limit": {
        "type": "string",
        "title": "Limit",
        "description": "Maximum average matching rate; specified as a number, "
        "with an optional /second, /minute, /hour or /day suffix. "
        "Examples: 3/second, 3/sec or 3/s.",
        "propertyOrder": 25,
    },
    "limit_burst": {
        "type": "integer",
        "title": "Limit burst",
        "description": "Maximum initial number of packets to match, allowing a "
        "short-term average above limit.",
        "default": 5,
        "propertyOrder": 26,
    },
    "firewall_policy": {
        "type": "string",
        "enum": ["ACCEPT", "REJECT", "DROP"],
        "options": {"enum_titles": ["Accept", "Reject", "Drop"]},
        "default": "REJECT",
    },
    "zone_policy": {
        "type": "string",
        "enum": ["ACCEPT", "REJECT", "DROP"],
        "options": {"enum_titles": ["Accept", "Reject", "Drop"]},
        "default": "REJECT",
    },
    "rule_policy": {
        "type": "string",
        "enum": ["ACCEPT", "REJECT", "DROP", "MARK", "NOTRACK"],
        "options": {"enum_titles": ["Accept", "Reject", "Drop", "Mark", "Notrack"]},
        "default": "REJECT",
    },
}

firewall_includes_properties = {
    "name": {"$ref": "#/definitions/name"},
    "enabled": {"$ref": "#/definitions/enabled"},
    "family": {"$ref": "#/definitions/family"},
    "type": {
        "type": "string",
        "title": "Type of the script",
        "description": 'Specifies the type of the include, can be "script" for traditional '
        'shell script includes or restore for plain files in iptables-restore format.',
        "enum": ["script", "restore"],
        "propertyOrder": 101,
    },
    "path": {
        "type": "string",
        "title": "Script to include",
        "description": "Specifies a shell script to execute on boot or firewall restarts",
        "default": "/etc/firewall.user",
        "propertyOrder": 102,
    },
    "reload": {
        "type": "boolean",
        "title": "Reload the included file when reloading firewall rules",
        "description": "This specifies whether or not the included file should be "
        "reloaded when the firewall rules are reloaded. This is only needed if "
        "the included file injects rules into internal OpenWRT chains.",
        "default": False,
        "propertyOrder": 103,
    },
}

firewall_redirect_properties = {
    "name": {"$ref": "#/definitions/name"},
    "enabled": {"$ref": "#/definitions/enabled"},
    "src": {"$ref": "#/definitions/src"},
    "src_ip": {"$ref": "#/definitions/src_ip"},
    "src_mac": {"$ref": "#/definitions/src_mac"},
    "src_port": {"$ref": "#/definitions/src_port"},
    "proto": {"$ref": "#/definitions/proto"},
    "dest": {"$ref": "#/definitions/dest"},
    "dest_ip": {"$ref": "#/definitions/dest_ip"},
    "dest_port": {"$ref": "#/definitions/dest_port"},
    "ipset": {"$ref": "#/definitions/ipset"},
    "mark": {"$ref": "#/definitions/mark"},
    "start_date": {"$ref": "#/definitions/start_date"},
    "stop_date": {"$ref": "#/definitions/stop_date"},
    "start_time": {"$ref": "#/definitions/start_time"},
    "stop_time": {"$ref": "#/definitions/stop_time"},
    "weekdays": {"$ref": "#/definitions/weekdays"},
    "monthdays": {"$ref": "#/definitions/monthdays"},
    "utc_time": {"$ref": "#/definitions/utc_time"},
    "family": {"$ref": "#/definitions/family"},
    "limit": {"$ref": "#/definitions/limit"},
    "limit_burst": {"$ref": "#/definitions/limit_burst"},
    "src_dip": {
        "type": "string",
        "title": "Source DIP",
        "description": "For DNAT, match incoming traffic directed at the "
        "given destination ip address. For SNAT rewrite the source address "
        "to the given address.",
        "format": "ipv4",
        "propertyOrder": 101,
    },
    "src_dport": {
        "type": "string",
        "title": "Source DPORT",
        "description": "For DNAT, match incoming traffic directed at the given "
        "destination port or port range on this host. For SNAT rewrite the "
        "source ports to the given value.",
        "pattern": port_range_regex,
        "propertyOrder": 102,
    },
    "reflection": {
        "type": "boolean",
        "title": "Reflection",
        "description": "Activate NAT reflection for this redirect. Applicable to "
        "DNAT targets.",
        "default": True,
        "propertyOrder": 103,
    },
    "reflection_src": {
        "type": "string",
        "title": "Reflection source",
        "description": "The source address to use for NAT-reflected packets if "
        "reflection is True. This can be internal or external, specifying which "
        "interface’s address to use. Applicable to DNAT targets.",
        "enum": ["internal", "external"],
        "default": "internal",
        "propertyOrder": 104,
    },
    "target": {
        "type": "string",
        "title": "Target",
        "description": "NAT target (DNAT or SNAT) to use when generating the rule.",
        "enum": ["DNAT", "SNAT"],
        "default": "DNAT",
        "propertyOrder": 105,
    },
}

firewall_rules_properties = {
    "name": {"$ref": "#/definitions/name"},
    "enabled": {"$ref": "#/definitions/enabled"},
    "src": {"$ref": "#/definitions/src"},
    "src_ip": {"$ref": "#/definitions/src_ip"},
    "src_mac": {"$ref": "#/definitions/src_mac"},
    "src_port": {"$ref": "#/definitions/src_port"},
    "proto": {"$ref": "#/definitions/proto"},
    "dest": {"$ref": "#/definitions/dest"},
    "dest_ip": {"$ref": "#/definitions/dest_ip"},
    "dest_port": {"$ref": "#/definitions/dest_port"},
    "ipset": {"$ref": "#/definitions/ipset"},
    "mark": {"$ref": "#/definitions/mark"},
    "start_date": {"$ref": "#/definitions/start_date"},
    "stop_date": {"$ref": "#/definitions/stop_date"},
    "start_time": {"$ref": "#/definitions/start_time"},
    "stop_time": {"$ref": "#/definitions/stop_time"},
    "weekdays": {"$ref": "#/definitions/weekdays"},
    "monthdays": {"$ref": "#/definitions/monthdays"},
    "utc_time": {"$ref": "#/definitions/utc_time"},
    "family": {"$ref": "#/definitions/family"},
    "limit": {"$ref": "#/definitions/limit"},
    "limit_burst": {"$ref": "#/definitions/limit_burst"},
    "icmp_type": {
        "title": "ICMP type",
        "description": "For protocol icmp select specific icmp types to match. "
        "Values can be either exact icmp type numbers or type names.",
        "type": "array",
        "uniqueItems": True,
        "additionalItems": True,
        "propertyOrder": 101,
        "items": {"title": "ICMP type", "type": "string"},
    },
    "target": {
        "allOf": [
            {"$ref": "#/definitions/rule_policy"},
            {
                "title": "Target",
                "description": "firewall action for matched traffic",
                "propertyOrder": 11,
            },
        ]
    },
}

firewall_forwardings_properties = {
    "name": {"$ref": "#/definitions/name"},
    "enabled": {"$ref": "#/definitions/enabled"},
    "src": {"$ref": "#/definitions/src"},
    "dest": {"$ref": "#/definitions/dest"},
    "family": {"$ref": "#/definitions/family"},
}

# Note: this is currently incomplete and needs other properties adding
# https://openwrt.org/docs/guide-user/firewall/firewall_configuration#zones
firewall_zones_properties = {
    "name": {"$ref": "#/definitions/zone_name"},
    "enabled": {"$ref": "#/definitions/enabled"},
    "network": {
        "type": "array",
        "title": "Network",
        "description": "List of interfaces attached to this zone.",
        "uniqueItems": True,
        "propertyOrder": 2,
        "items": {
            "title": "Network",
            "type": "string",
            "maxLength": 15,
            "pattern": "^[a-zA-z0-9_\\.\\-]*$",
        },
    },
    "masq": {
        "type": "boolean",
        "title": "Masquerading",
        "description": "Specifies whether outgoing zone traffic should be "
        "masqueraded.",
        "default": False,
        "format": "checkbox",
        "propertyOrder": 3,
    },
    "mtu_fix": {
        "type": "boolean",
        "title": "MSS clamping",
        "description": "Enable MSS clamping for outgoing zone traffic.",
        "default": False,
        "format": "checkbox",
        "propertyOrder": 4,
    },
    "input": {
        "allOf": [
            {"$ref": "#/definitions/zone_policy"},
            {
                "title": "Input policy",
                "description": "Default policy for incoming zone traffic.",
                "propertyOrder": 5,
            },
        ]
    },
    "output": {
        "allOf": [
            {"$ref": "#/definitions/zone_policy"},
            {
                "title": "Output policy",
                "description": "Default policy for outgoing zone traffic.",
                "propertyOrder": 6,
            },
        ]
    },
    "forward": {
        "allOf": [
            {"$ref": "#/definitions/zone_policy"},
            {
                "title": "Forward policy",
                "description": "Default policy for forwarded zone traffic.",
                "propertyOrder": 7,
            },
        ]
    },
    "masq_src": {
        "type": "array",
        "title": "Masqueraded source CIDR list",
        "description": "List of source IPv4 CIDRs that require masquerading.",
        "propertyOrder": 8,
        "items": {
            "allOf": [
                {"$ref": "#/definitions/ipv4_cidr"},
                {
                    "title": "Masqueraded source CIDR",
                    "description": "Source CIDR to enable masquerading for. "
                    'Negation is possible by prefixing the subnet with a "!". ',
                },
            ],
        },
    },
    "masq_dest": {
        "type": "array",
        "title": "Masqueraded destination CIDR list",
        "description": "List of destination IPv4 CIDRs that require masquerading.",
        "propertyOrder": 9,
        "items": {
            "allOf": [
                {"$ref": "#/definitions/ipv4_cidr"},
                {
                    "title": "Masquerade destination CIDR",
                    "description": "Destination CIDR to enable masquerading for. "
                    'Negation is possible by prefixing the subnet with a "!". ',
                },
            ],
        },
    },
    "masq_allow_invalid": {
        "type": "boolean",
        "title": "Allow invalid packets",
        "description": "Do not add DROP INVALID rules to the firewall if masquerading "
        "is used. The DROP rules are supposed to prevent NAT leakage.",
        "default": False,
        "format": "checkbox",
        "propertyOrder": 10,
    },
    "family": {"$ref": "#/definitions/family"},
    "log": {
        "type": "string",  # check if it's an integer
        "title": "Enable logging for the filter and/or mangle table",
        "description": "Bit field to enable logging in the filter and/or mangle tables, "
        "bit 0 = filter, bit 1 = mangle.",
        "min": "0",
        "max": "3",
        "default": "0",
        "propertyOrder": 10,
    },
    "log_limit": {
        "type": "string",
        "title": "Limit on the number of log messages",
        "description": "Limits the amount of log messages per interval. For example, "
        '"10/minute" will limit the logging to 10 messages per minute',
        "default": "10/minute",
        "propertyOrder": 11,
    },
    "device": {
        "type": "array",
        "title": "Raw devices to attach to this zone",
        "description": "A list of raw device names to associate with this zone. ",
        "items": {
            "type": "string",
            "title": "A device to attach to the zone.",
            "description": "A device to attach to the zone."
            'For example, "ppp+" to match any PPP interface to the zone.',
        },
        "propertyOrder": 12,
    },
}

firewall_defaults = {
    "input": {
        "title": "Default input policy",
        "description": "Default policy for the INPUT chain of the filter table",
        "propertyOrder": 1,
        "allOf": [
            {"$ref": "#/definitions/firewall_policy"},
        ],
    },
    "output": {
        "allOf": [
            {"$ref": "#/definitions/firewall_policy"},
            {
                "title": "Default output policy",
                "description": "Default policy for the OUTPUT chain of the filter table",
                "propertyOrder": 2,
            },
        ]
    },
    "forward": {
        "allOf": [
            {"$ref": "#/definitions/firewall_policy"},
            {
                "title": "Default forward policy",
                "description": "Defulat policy for the FORWARD chain of the filter table",
                "propertyOrder": 3,
            },
        ]
    },
    "drop_invalid": {
        "type": "boolean",
        "title": "Drop invalid packets",
        "description": "If True then any invalid packets will be dropped.",
        "default": False,
        "format": "checkbox",
        "propertyOrder": 4,
    },
    "synflood_protect": {
        "type": "boolean",
        "title": "Enable SYN flood protection",
        "description": "Enables SYN flood protection.",
        "default": False,
        "format": "checkbox",
        "propertyOrder": 5,
    },
    "synflood_rate": {
        "type": "integer",
        "title": "Rate limit (packets/second) for SYN packets above which the traffic is considered a flood.",
        "description": "Number of packets/second for SYN packets above which the traffic is considered a "
        "flood.",
        "default": 25,
        "propertyOrder": 6,
    },
    "synflood_burst": {
        "type": "integer",
        "title": "Burst limit (packets/second) for SYN packets",
        "description": "Set burst limit for SYN packets above which the traffic is considered a flood if it "
        "exceeds the allowed rate.",
        "default": 50,
        "propertyOrder": 7,
    },
    "tcp_syncookies": {
        "type": "boolean",
        "title": "Enable the use of TCP SYN cookies",
        "description": "If True, enables the use of SYN cookies.",
        "default": True,
        "format": "checkbox",
        "propertyOrder": 8,
    },
    "tcp_ecn": {
        "type": "boolean",
        "title": "Enable Explicit Congestion Notification",
        "description": "If True, enables Explicit Congestion Notification.",
        "default": False,
        "format": "checkbox",
        "propertyOrder": 9,
    },
    "tcp_window_scaling": {
        "type": "boolean",
        "title": "Enable TCP window scaling",
        "description": "If True, enables TCP window scaling.",
        "default": True,
        "format": "checkbox",
        "propertyOrder": 10,
    },
    "accept_redirects": {
        "type": "boolean",
        "title": "Accept redirects",
        "description": "If True, accept redirects.",
        "default": False,
        "format": "checkbox",
        "propertyOrder": 11,
    },
    "accept_source_route": {
        "type": "boolean",
        "title": "Accept source routes",
        "description": "If True, accept source routes.",
        "default": False,
        "format": "checkbox",
        "propertyOrder": 12,
    },
    "custom_chains": {
        "type": "boolean",
        "title": "Enable generation of custom rule chain hooks for user generated rules",
        "description": "If True, enable generation of custom rule chain hooks for user generated rules. "
        "User rules would be typically stored in firewall.user but some packages e.g. BCP38 also make use "
        "of these hooks.",
        "default": True,
        "format": "checkbox",
        "propertyOrder": 13,
    },
    "disable_ipv6": {
        "type": "boolean",
        "title": "Disable IPv6 firewall rules",
        "description": "If True, disable IPv6 firewall rules.",
        "default": False,
        "format": "checkbox",
        "propertyOrder": 14,
    },
    "flow_offloading": {
        "type": "boolean",
        "title": "Enable software flow offloading for connections.",
        "description": "If True, enable software flow offloading for connections.",
        "default": False,
        "format": "checkbox",
        "propertyOrder": 15,
    },
    "flow_offloading_hw": {
        "type": "boolean",
        "title": "Enable hardware flow offloading for connections",
        "description": "If True, enable hardware flow offloading for connections.",
        "default": False,
        "format": "checkbox",
        "propertyOrder": 16,
    },
    "auto_helper": {
        "type": "boolean",
        "title": "Enable Conntrack helpers",
        "description": "If True, enable Conntrack helpers ",
        "default": True,
        "format": "checkbox",
        "propertyOrder": 17,
    },
}

firewall_properties = {
    "defaults": {
        "type": "object",
        "title": "Firewall defaults",
        "description": "Defaults for the firewall",
        "propertyOrder": 4,
        "properties": firewall_defaults,
    },
    "forwardings": {
        "type": "array",
        "title": "Forwardings",
        "propertyOrder": 5,
        "items": {
            "type": "object",
            "title": "Forwarding",
            "additionalProperties": False,
            "required": [
                "src",
                "dest",
            ],  # need to check why openwrt has forwardings without src or dest
            "properties": firewall_forwardings_properties,
        },
    },
    "zones": {
        "type": "array",
        "title": "Zones",
        "propertyOrder": 6,
        "items": {
            "type": "object",
            "title": "Zones",
            "additionalProperties": True,
            "required": ["name"],
            "properties": firewall_zones_properties,
        },
    },
    "rules": {
        "type": "array",
        "title": "Rules",
        "propertyOrder": 7,
        "items": {
            "type": "object",
            "title": "Rules",
            "additionalProperties": True,
            "required": ["target"],
            "properties": firewall_rules_properties,
        },
    },
    "redirects": {
        "type": "array",
        "title": "Redirects",
        "propertyOrder": 8,
        "items": {
            "type": "object",
            "title": "Redirect",
            "additionalProperties": False,
            "properties": firewall_redirect_properties,
        },
    },
    "includes": {
        "type": "array",
        "title": "Includes",
        "propertyOrder": 9,
        "items": {
            "type": "object",
            "title": "Include",
            "additionalProperties": False,
            "required": ["path"],
            "properties": firewall_includes_properties,
        },
    },
}

firewall = {
    "definitions": firewall_definitions,
    "properties": {
        "firewall": {
            "type": "object",
            "title": "Firewall",
            "additionalProperties": True,
            "propertyOrder": 11,
            "properties": firewall_properties,
        },
    },
}

schema = merge_config(schema, firewall)

mwan3 = {
    "properties": {
        "mwan3": {
            "type": "object",
            "title": "Mwan3",
            "additionalProperties": True,
            "propertyOrder": 12,
            "properties": {
                "globals": {
                    "type": "object",
                    "title": "Globals",
                    "description": "Globals for mwan3",
                    "propertyOrder": 1,
                    "required": [
                        "mmx_mask",
                    ],
                    "properties": {
                        "mmx_mask": {
                            "type": "string",
                            "title": "Firewall mask",
                            "description": "Enter value in hex, starting with 0x",
                            "propertyOrder": 1,
                            "default": "0x3F00",
                        },
                        "logging": {
                            "type": "boolean",
                            "title": "Logging",
                            "description": "Global firewall logging. "
                            "This must be enabled for any rule specific logging to occur",
                            "propertyOrder": 2,
                            "default": False,
                        },
                        "loglevel": {
                            "type": "string",
                            "title": "Log Level",
                            "description": "Firewall loglevel",
                            "enum": [
                                "emerg",
                                "alert",
                                "crit",
                                "error",
                                "warning",
                                "notice",
                                "info",
                                "debug",
                            ],
                            "default": "notice",
                            "propertyOrder": 3,
                        },
                        "rt_table_lookup": {
                            "type": "number",
                            "title": "Routing table lookup",
                            "description": "Specify an additional routing table to be scanned  "
                            "for connected networks. In default config leave empty",
                            "propertyOrder": 4,
                        },
                    },
                },
                "interfaces": {
                    "type": "array",
                    "title": "Interfaces",
                    "propertyOrder": 2,
                    "items": {
                        "type": "object",
                        "title": "Interface",
                        "additionalProperties": True,
                        "required": [
                            "name",
                        ],
                        "properties": {
                            "name": {
                                "type": "string",
                                "title": "Interface name",
                                "description": "OpenWrt interface name",
                                "propertyOrder": 1,
                            },
                            "enabled": {
                                "type": "boolean",
                                "title": "Enabled",
                                "description": "Specifies whether mwan3 should run on this interface",
                                "default": True,
                                "format": "checkbox",
                                "propertyOrder": 2,
                            },
                            "track_method": {
                                "type": "string",
                                "title": "Tracking method",
                                "description": "Tracking method for mwan3track",
                                "enum": [
                                    "ping",
                                    # "arping", #not working on openwrt
                                    # "httping",
                                    # "nping-tcp",
                                    # "nping-udp",
                                    # "nping-icmp",
                                    # "nping-arp", 
                                ],
                                "default": "ping",
                                "propertyOrder": 3,
                            },
                            "track_ip": {
                                "title": "Tracking IPs",
                                "description": "List of IPs to ping to test the interface. If this list "
                                "is empty then the interface is always considered up",
                                "type": "array",
                                "uniqueItems": True,
                                "additionalItems": True,
                                "items": {
                                    "type": "string",
                                    "title": "ipv4 address",
                                    "minLength": 7,
                                    "maxLength": 15,
                                    "format": "ipv4",
                                },
                                "propertyOrder": 4,
                            },
                            "reliability": {
                                "type": "integer",
                                "title": "Reliability",
                                "description": "Number of track_ip hosts that must reply for the test to"
                                " be considered successful. Ensure there are at least this"
                                " many track_ip hosts defined or the interface will always"
                                " be considered down",
                                "default": 1,
                                "propertyOrder": 5,
                            },
                            "count": {
                                "type": "integer",
                                "title": "Count",
                                "description": "Number of checks to send to each host with each test",
                                "default": 1,
                                "propertyOrder": 6,
                            },
                            "timeout": {
                                "type": "integer",
                                "title": "Timeout",
                                "description": "Number of seconds to wait for an echo-reply after an "
                                "echo-request",
                                "default": 4,
                                "propertyOrder": 7,
                            },
                            "interval": {
                                "type": "integer",
                                "title": "Interval",
                                "description": "Number of seconds between each test",
                                "default": 10,
                                "propertyOrder": 8,
                            },
                            "failure_interval": {
                                "type": "integer",
                                "title": "Failure interval",
                                "description": "Number of seconds between each test during teardown on "
                                "failure detection",
                                "propertyOrder": 9,
                            },
                            "recovery_interval": {
                                "type": "integer",
                                "title": "Recovery interval",
                                "description": "Number of seconds between each test during tearup on "
                                "recovery detection",
                                "propertyOrder": 10,
                            },
                            "keep_failure_interval": {
                                "type": "boolean",
                                "title": "Keep failure interval",
                                "description": "In the event of an error, keep the number of seconds "
                                "between each test during teardown (failure detection)",
                                "default": False,
                                "format": "checkbox",
                                "propertyOrder": 11,
                            },
                            "check_quality": {
                                "type": "boolean",
                                "title": "Check link quality",
                                "description": "In addition to the interface being up, the check_quality "
                                "options can check the overall link quality "
                                "with packet loss and/or latency measurements",
                                "default": False,
                                "format": "checkbox",
                                "propertyOrder": 12,
                            },
                            "up": {
                                "type": "integer",
                                "title": "Up",
                                "description": "Number of successful tests to consider link as alive",
                                "default": 5,
                                "propertyOrder": 13,
                            },
                            "down": {
                                "type": "integer",
                                "title": "Down",
                                "description": "Number of failed tests to consider link as dead",
                                "default": 5,
                                "propertyOrder": 14,
                            },
                            "family": {
                                "type": "string",
                                "title": "Family",
                                "description": "The specific protocol family this interface handles",
                                "enum": [
                                    "ipv4",
                                    "ipv6",
                                ],
                                "default": "ipv4",
                                "propertyOrder": 15,
                            },
                            "max_ttl": {
                                "type": "integer",
                                "title": "Time to live",
                                "description": "Time to live (TTL) or hop limit. Only valid if tracking "
                                "method is ping.",
                                "default": 60,
                                "propertyOrder": 16,
                            },
                            "initial_state": {
                                "type": "string",
                                "title": "Initial state",
                                "description": "If the value is offline, then traffic goes via this "
                                "interface only if mwan3track checked the connection "
                                "first. If the value is online, then the mwan3track "
                                "test is not waited for. The interface is marked as "
                                "online at once.",
                                "enum": [
                                    "online",
                                    "offline",
                                ],
                                "default": "online",
                                "propertyOrder": 17,
                            },
                            "size": {
                                "type": "integer",
                                "title": "Size",
                                "description": "Size of ping packets to use in bytes. Only valid if "
                                "tracking method is ping.",
                                "default": 56,
                                "propertyOrder": 18,
                            },
                            "flush_conntrack": {
                                "title": "Flush connection tracking",
                                "description": "specifies upon which events the connections table should"
                                " be flushed",
                                "type": "array",
                                # commented because the front end gives a strange error
                                # "uniqueItems": True,
                                "additionalItems": True,
                                "items": {
                                    "type": "string",
                                    "enum": [
                                        "ifup",
                                        "ifdown",
                                        "connected",
                                        "disconnected",
                                    ],
                                },
                                "propertyOrder": 19,
                            },
                        },
                    },
                },
                "members": {
                    "type": "array",
                    "title": "Members",
                    "propertyOrder": 3,
                    "items": {
                        "type": "object",
                        "title": "Members",
                        "additionalProperties": True,
                        "required": ["name", "interface"],
                        "properties": {
                            "name": {
                                "type": "string",
                                "title": "Name",
                                "description": "The name of this member configuration "
                                ",which is then referenced in policies",
                                "propertyOrder": 1,
                            },
                            "interface": {
                                "type": "string",
                                "title": "Interface",
                                "description": "Member applies to this interface "
                                "(use the same interface name as used in the mwan3 "
                                "interface section, above)",
                                "propertyOrder": 2,
                            },
                            "metric": {
                                "type": "integer",
                                "title": "Metric",
                                "description": "Members within one policy with a lower "
                                "metric have precedence over higher metric members",
                                "default": 1,
                                "propertyOrder": 3,
                            },
                            "weight": {
                                "type": "integer",
                                "title": "Weight",
                                "description": "Members with same metric will distribute "
                                "load based on this weight value",
                                "default": 1,
                                "propertyOrder": 4,
                            },
                        },
                    },
                },
                "policies": {
                    "type": "array",
                    "title": "Policy",
                    "propertyOrder": 4,
                    "items": {
                        "type": "object",
                        "title": "Policy",
                        "additionalProperties": True,
                        "required": ["name", "use_member"],
                        "properties": {
                            "name": {
                                "type": "string",
                                "title": "Name",
                                "description": "The unique name of the policy. "
                                "Must be no more than 15 characters",
                                "propertyOrder": 1,
                            },
                            "use_member": {
                                "type": "array",
                                "title": "Members assigned",
                                "description": "One or more members assigned to this policy",
                                "items": {
                                    "title": "Member used",
                                    "type": "string",
                                },
                                "propertyOrder": 2,
                            },
                            "last_resort": {
                                "type": "string",
                                "title": "Last resort",
                                "description": "Determine the fallback routing "
                                "behaviour if all WAN members in the policy are down",
                                "enum": ["unreachable", "blackhole", "default"],
                                "default": "unreachable",
                                "propertyOrder": 3,
                            },
                        },
                    },
                },
                "rules": {
                    "type": "array",
                    "title": "Rules",
                    "propertyOrder": 5,
                    "items": {
                        "type": "object",
                        "title": "Rules",
                        "additionalProperties": True,
                        "required": ["name", "use_policy"],
                        "properties": {
                            "name": {
                                "type": "string",
                                "title": "Name",
                                "description": "The unique name of the rule. "
                                "Must be no more than 15 characters",
                                "propertyOrder": 1,
                            },
                            "use_policy": {
                                "type": "string",
                                "title": "Use policy",
                                "description": "Use this policy for traffic that matches or set to "
                                "default to use the default routing table to lookup",
                                "default": "default",
                                "propertyOrder": 2,
                            },
                            # check description
                            "src_ip": {
                                "$ref": "#/definitions/src_ip",
                                "propertyOrder": 3,
                            },
                            "src_port": {
                                "$ref": "#/definitions/src_port",
                                "propertyOrder": 4,
                            },
                            "proto": {
                                "$ref": "#/definitions/proto",
                                "propertyOrder": 5,
                            },
                            "dest_ip": {
                                "$ref": "#/definitions/dest_ip",
                                "propertyOrder": 6,
                            },
                            "dest_port": {
                                "$ref": "#/definitions/dest_port",
                                "propertyOrder": 7,
                            },
                            "ipset": {
                                "$ref": "#/definitions/ipset",
                                "propertyOrder": 8,
                            },
                            "sticky": {
                                "type": "boolean",
                                "title": "Sticky",
                                "description": "Allow traffic from the same source "
                                "IP address within the timeout limit to use"
                                " same wan interface as prior session",
                                "default": False,
                                "propertyOrder": 9,
                            },
                            "timeout": {
                                "type": "integer",
                                "title": "Sticky",
                                "description": "Stickiness timeout value in seconds",
                                "default": 60,
                                "propertyOrder": 10,
                            },
                            "family": {"$ref": "#/definitions/family"},
                            "logging": {
                                "type": "boolean",
                                "title": "Enable logging",
                                "description": "Enables firewall rule logging "
                                "(global mwan3 logging setting must also be enabled)",
                                "default": False,
                                "propertyOrder": 11,
                            },
                        },
                    },
                },
            },
        }
    },
}
schema = merge_config(schema, mwan3)

# add OpenVPN schema
schema = merge_config(schema, base_openvpn_schema)
# OpenVPN customizations for OpenWRT
schema = merge_config(
    schema,
    {
        "definitions": {
            "tunnel": {
                "properties": {
                    "disabled": {
                        "title": "disabled",
                        "description": "disable this VPN without deleting its configuration",
                        "type": "boolean",
                        "default": False,
                        "format": "checkbox",
                        "propertyOrder": 1,
                    }
                }
            }
        }
    },
)
