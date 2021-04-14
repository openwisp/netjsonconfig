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
                                "default": True,
                                "format": "checkbox",
                                "propertyOrder": 4,
                            }
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
            "radio_80211ac_2ghz_settings": {
                "allOf": [{"$ref": "#/definitions/radio_hwmode_11g"}]
            },
            "radio_80211ac_5ghz_settings": {
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
