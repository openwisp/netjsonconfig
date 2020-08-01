"""
OpenWrt specific JSON-Schema definition
"""
from ...schema import schema as default_schema
from ...utils import merge_config
from ..openvpn.schema import base_openvpn_schema
from .timezones import timezones

default_radio_driver = "mac80211"

# The following regex will match against a single valid port, or a port range e.g. 1234-5000
port_range_regex = "^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])(-([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5]))?$"  # noqa

# Match against a MAC address
mac_address_regex = "^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$"

# Match against a yyyy-mm-dd format date. Note that draft07 of the JSON schema standard
# include a "date" pattern which can replace this.
# https://json-schema.org/understanding-json-schema/reference/string.html
date_regex = "^([0-9]{4})-(0[1-9]|[12][0-9]|3[01])-([012][0-9]|[3][01])$"

# Match against a time in the format hh:mm:ss
time_regex = "^([01][0-9]|2[0123])(:([012345][0-9])){2}$"

schema = merge_config(
    default_schema,
    {
        "definitions": {
            "interface_settings": {
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
                                "description": 'override OpenWRT "network" config option of of wifi-iface '
                                "directive; will be automatically determined if left blank",
                                "uniqueItems": True,
                                "additionalItems": True,
                                "items": {
                                    "title": "network",
                                    "type": "string",
                                    "$ref": "#/definitions/interface_settings/properties/network",
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
                                "description": 'specifies the mac filter policy, "disable" to disable '
                                'the filter, "allow" to treat it as whitelist or '
                                '"deny" to treat it as blacklist',
                                "enum": ["disable", "allow", "deny"],
                                "default": "disable",
                                "propertyOrder": 15,
                            },
                            "maclist": {
                                "type": "array",
                                "title": "MAC List",
                                "description": "mac addresses that will be filtered according to the policy "
                                'specified in the "macfilter" option',
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
                                "description": 'sets the "multicast_snooping" kernel setting for a bridge',
                                "default": True,
                                "format": "checkbox",
                                "propertyOrder": 4,
                            }
                        }
                    }
                ]
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
                "default": "DROP",
            },
            "rule_policy": {
                "type": "string",
                "enum": ["ACCEPT", "REJECT", "DROP", "MARK", "NOTRACK"],
                "options": {
                    "enum_titles": ["Accept", "Reject", "Drop", "Mark", "Notrack"]
                },
                "default": "DROP",
            },
            "base_radio_settings": {
                "properties": {
                    "driver": {
                        "type": "string",
                        "enum": ["mac80211", "madwifi", "ath5k", "ath9k", "broadcom"],
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
            "firewall": {
                "type": "object",
                "title": "Firewall",
                "additionalProperties": True,
                "propertyOrder": 11,
                "properties": {
                    "syn_flood": {
                        "type": "boolean",
                        "title": "enable SYN flood protection",
                        "default": False,
                        "format": "checkbox",
                        "propertyOrder": 1,
                    },
                    "input": {
                        "allOf": [
                            {"$ref": "#/definitions/firewall_policy"},
                            {
                                "title": "input",
                                "description": "policy for the INPUT chain of the filter table",
                                "propertyOrder": 2,
                            },
                        ]
                    },
                    "output": {
                        "allOf": [
                            {"$ref": "#/definitions/firewall_policy"},
                            {
                                "title": "output",
                                "description": "policy for the OUTPUT chain of the filter table",
                                "propertyOrder": 3,
                            },
                        ]
                    },
                    "forward": {
                        "allOf": [
                            {"$ref": "#/definitions/firewall_policy"},
                            {
                                "title": "forward",
                                "description": "policy for the FORWARD chain of the filter table",
                                "propertyOrder": 4,
                            },
                        ]
                    },
                    "forwardings": {
                        "type": "array",
                        "title": "Forwardings",
                        "propertyOrder": 5,
                        "items": {
                            "type": "object",
                            "title": "Forwarding",
                            "additionalProperties": False,
                            "required": ["src", "dest"],
                            "properties": {
                                "src": {
                                    "type": "string",
                                    "title": "src",
                                    "description": "specifies the traffic source zone and must "
                                    "refer to one of the defined zone names",
                                    "propertyOrder": 1,
                                },
                                "dest": {
                                    "type": "string",
                                    "title": "dest",
                                    "description": "specifies the traffic destination zone and must "
                                    "refer to one of the defined zone names",
                                    "propertyOrder": 2,
                                },
                                "family": {
                                    "type": "string",
                                    "title": "family",
                                    "description": "protocol family (ipv4, ipv6 or any) to generate "
                                    "iptables rules for",
                                    "enum": ["ipv4", "ipv6", "any"],
                                    "default": "any",
                                    "propertyOrder": 3,
                                },
                            },
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
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "title": "name",
                                    "description": "unique zone name",
                                    "maxLength": 11,
                                    "propertyOrder": 1,
                                },
                                "network": {
                                    "type": "array",
                                    "title": "Network",
                                    "description": "list of interfaces attached to this zone",
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
                                    "title": "masq",
                                    "description": "specifies wether outgoing zone traffic should be "
                                    "masqueraded",
                                    "default": False,
                                    "format": "checkbox",
                                    "propertyOrder": 3,
                                },
                                "mtu_fix": {
                                    "type": "boolean",
                                    "title": "mtu_fix",
                                    "description": "enable MSS clamping for outgoing zone traffic",
                                    "default": False,
                                    "format": "checkbox",
                                    "propertyOrder": 4,
                                },
                                "input": {
                                    "allOf": [
                                        {"$ref": "#/definitions/zone_policy"},
                                        {
                                            "title": "input",
                                            "description": "default policy for incoming zone traffic",
                                            "propertyOrder": 5,
                                        },
                                    ]
                                },
                                "output": {
                                    "allOf": [
                                        {"$ref": "#/definitions/zone_policy"},
                                        {
                                            "title": "output",
                                            "description": "default policy for outgoing zone traffic",
                                            "propertyOrder": 6,
                                        },
                                    ]
                                },
                                "forward": {
                                    "allOf": [
                                        {"$ref": "#/definitions/zone_policy"},
                                        {
                                            "title": "forward",
                                            "description": "default policy for forwarded zone traffic",
                                            "propertyOrder": 7,
                                        },
                                    ]
                                },
                            },
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
                            "required": ["src", "target"],
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "title": "name",
                                    "description": "name of the rule",
                                    "propertyOrder": 1,
                                },
                                "src": {
                                    "type": "string",
                                    "title": "src",
                                    "description": "specifies the traffic source zone and must "
                                    "refer to one of the defined zone names",
                                    "propertyOrder": 2,
                                },
                                "src_ip": {
                                    "type": "string",
                                    "title": "src_ip",
                                    "description": "match incoming traffic from the specified "
                                    "source ip address",
                                    "propertyOrder": 3,
                                },
                                "src_mac": {
                                    "type": "string",
                                    "title": "src_mac",
                                    "description": "match incoming traffic from the specified "
                                    "mac address",
                                    "pattern": "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
                                    "minLength": 17,
                                    "maxLength": 17,
                                    "propertyOrder": 4,
                                },
                                "src_port": {
                                    "type": "string",
                                    "title": "src_port",
                                    "description": "match incoming traffic from the specified "
                                    "source port or port range, if relevant proto "
                                    "is specified. Multiple ports can be specified "
                                    "separated by blanks",
                                    "propertyOrder": 5,
                                },
                                "proto": {
                                    "type": "array",
                                    "title": "proto",
                                    "description": "match incoming traffic using the given protocol. "
                                    "Can be one of tcp, udp, tcpudp, udplite, icmp, esp, "
                                    "ah, sctp, or all or it can be a numeric value, "
                                    "representing one of these protocols or a different one. "
                                    "A protocol name from /etc/protocols is also allowed. "
                                    "The number 0 is equivalent to all",
                                    "default": ["tcp", "udp"],
                                    "propertyOrder": 6,
                                    "items": {
                                        "title": "Protocol type",
                                        "type": "string",
                                    },
                                },
                                "icmp_type": {
                                    "title": "icmp_type",
                                    "description": "for protocol icmp select specific icmp types to match. "
                                    "Values can be either exact icmp type numbers or type names",
                                    "type": "array",
                                    "uniqueItems": True,
                                    "additionalItems": True,
                                    "propertyOrder": 7,
                                    "items": {"title": "ICMP type", "type": "string"},
                                },
                                "dest": {
                                    "type": "string",
                                    "title": "dest",
                                    "description": "specifies the traffic destination zone and must "
                                    "refer to one of the defined zone names, or * for "
                                    "any zone. If specified, the rule applies to forwarded "
                                    "traffic; otherwise, it is treated as input rule",
                                    "propertyOrder": 8,
                                },
                                "dest_ip": {
                                    "type": "string",
                                    "title": "dest_ip",
                                    "description": "match incoming traffic directed to the specified "
                                    "destination ip address. With no dest zone, this "
                                    "is treated as an input rule",
                                    "propertyOrder": 9,
                                },
                                "dest_port": {
                                    "type": "string",
                                    "title": "dest_port",
                                    "description": "match incoming traffic directed at the given "
                                    "destination port or port range, if relevant "
                                    "proto is specified. Multiple ports can be specified "
                                    "separated by blanks",
                                    "propertyOrder": 10,
                                },
                                "target": {
                                    "allOf": [
                                        {"$ref": "#/definitions/rule_policy"},
                                        {
                                            "title": "target",
                                            "description": "firewall action for matched traffic",
                                            "propertyOrder": 11,
                                        },
                                    ]
                                },
                                "family": {
                                    "type": "string",
                                    "title": "family",
                                    "description": "protocol family to generate iptables rules for",
                                    "enum": ["ipv4", "ipv6", "any"],
                                    "default": "any",
                                    "propertyOrder": 12,
                                },
                                "limit": {
                                    "type": "string",
                                    "title": "limit",
                                    "description": "maximum average matching rate; specified as a number, "
                                    "with an optional /second, /minute, /hour or /day suffix",
                                    "propertyOrder": 13,
                                },
                                "enabled": {
                                    "type": "boolean",
                                    "title": "enable",
                                    "description": "Enable this rule.",
                                    "default": True,
                                    "format": "checkbox",
                                    "propertyOrder": 14,
                                },
                            },
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
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "title": "name",
                                    "description": "Name of redirect",
                                    "propertyOrder": 1,
                                },
                                "src": {
                                    "type": "string",
                                    "title": "src",
                                    "description": "Specifies the traffic source zone. "
                                    "Must refer to one of the defined zone names. "
                                    "For typical port forwards this usually is wan.",
                                    "propertyOrder": 2,
                                },
                                "src_ip": {
                                    "type": "string",
                                    "title": "src_ip",
                                    "description": "Match incoming traffic from the specified source ip "
                                    "address.",
                                    "format": "ipv4",
                                    "propertyOrder": 3,
                                },
                                "src_dip": {
                                    "type": "string",
                                    "title": "src_dip",
                                    "description": "For DNAT, match incoming traffic directed at the "
                                    "given destination ip address. For SNAT rewrite the source address "
                                    "to the given address.",
                                    "format": "ipv4",
                                    "propertyOrder": 4,
                                },
                                "src_mac": {
                                    "type": "string",
                                    "title": "src_mac",
                                    "description": "Match incoming traffic from the specified MAC address.",
                                    "pattern": mac_address_regex,
                                    "propertyOrder": 5,
                                },
                                "src_port": {
                                    "type": "string",
                                    "title": "src_port",
                                    "description": "Match incoming traffic originating from the given source "
                                    "port or port range on the client host.",
                                    "pattern": port_range_regex,
                                    "propertyOrder": 6,
                                },
                                "src_dport": {
                                    "type": "string",
                                    "title": "src_dport",
                                    "description": "For DNAT, match incoming traffic directed at the given "
                                    "destination port or port range on this host. For SNAT rewrite the "
                                    "source ports to the given value.",
                                    "pattern": port_range_regex,
                                    "propertyOrder": 7,
                                },
                                "proto": {
                                    "type": "array",
                                    "title": "proto",
                                    "description": "Match incoming traffic using the given protocol. "
                                    "Can be one of tcp, udp, tcpudp, udplite, icmp, esp, "
                                    "ah, sctp, or all or it can be a numeric value, "
                                    "representing one of these protocols or a different one. "
                                    "A protocol name from /etc/protocols is also allowed. "
                                    "The number 0 is equivalent to all",
                                    "default": ["tcp", "udp"],
                                    "propertyOrder": 8,
                                    "items": {
                                        "title": "Protocol type",
                                        "type": "string",
                                    },
                                },
                                "dest": {
                                    "type": "string",
                                    "title": "dest",
                                    "description": "Specifies the traffic destination zone. Must refer to "
                                    "on of the defined zone names. For DNAT target on Attitude Adjustment, "
                                    'NAT reflection works only if this is equal to "lan".',
                                    "propertyOrder": 9,
                                },
                                "dest_ip": {
                                    "type": "string",
                                    "title": "dest_ip",
                                    "description": "For DNAT, redirect matches incoming traffic to the "
                                    "specified internal host. For SNAT, it matches traffic directed at "
                                    "the given address. For DNAT, if the dest_ip is not specified, the rule "
                                    "is translated in a iptables/REDIRECT rule, otherwise it is a "
                                    "iptables/DNAT rule.",
                                    "format": "ipv4",
                                    "propertyOrder": 10,
                                },
                                "dest_port": {
                                    "type": "string",
                                    "title": "dest_port",
                                    "description": "For DNAT, redirect matched incoming traffic to the given "
                                    "port on the internal host. For SNAT, match traffic directed at the "
                                    "given ports. Only a single port or range can be specified.",
                                    "pattern": port_range_regex,
                                    "propertyOrder": 11,
                                },
                                "ipset": {
                                    "type": "string",
                                    "title": "ipset",
                                    "description": "Match traffic against the given ipset. The match can be "
                                    "inverted by prefixing the value with an exclamation mark.",
                                    "propertyOrder": 12,
                                },
                                "mark": {
                                    "type": "string",
                                    "title": "mark",
                                    "description": 'Match traffic against the given firewall mark, e.g. '
                                    '"0xFF" to match mark 255 or "0x0/0x1" to match any even mark value. '
                                    'The match can be inverted by prefixing the value with an exclamation '
                                    'mark, e.g. "!0x10" to match all but mark #16.',
                                    "propertyOrder": 13,
                                },
                                "start_date": {
                                    "type": "string",
                                    "title": "start_date",
                                    "description": "Only match traffic after the given date (inclusive).",
                                    "pattern": date_regex,
                                    # "format": "date", TODO: replace pattern with this
                                    # when adopt draft07
                                    "propertyOrder": 14,
                                },
                                "stop_date": {
                                    "type": "string",
                                    "title": "stop_date",
                                    "description": "Only match traffic before the given date (inclusive).",
                                    "pattern": date_regex,
                                    # "format": "date", TODO: replace pattern with this
                                    # when adopt draft07
                                    "propertyOrder": 15,
                                },
                                "start_time": {
                                    "type": "string",
                                    "title": "start_time",
                                    "description": "Only match traffic after the given time of day "
                                    "(inclusive).",
                                    "pattern": time_regex,
                                    "propertyOrder": 16,
                                },
                                "stop_time": {
                                    "type": "string",
                                    "title": "stop_time",
                                    "description": "Only match traffic before the given time of day "
                                    "(inclusive).",
                                    "pattern": time_regex,
                                    "propertyOrder": 17,
                                },
                                # Note: here we don't support negation of values like
                                # the UCI syntax does, as it's not necessary.
                                "weekdays": {
                                    "type": "array",
                                    "title": "weekdays",
                                    "description": "Only match traffic during the given week days, "
                                    'e.g. ["sun", "mon", "thu", "fri"] to only match on Sundays, '
                                    "Mondays, Thursdays and Fridays.",
                                    "propertyOrder": 18,
                                    "items": {
                                        "type": "string",
                                        "title": "weekday",
                                        "enum": [
                                            "mon",
                                            "tue",
                                            "wed",
                                            "thu",
                                            "fri",
                                            "sat",
                                            "sun",
                                        ],
                                    },
                                },
                                # Note: here we don't support negation of values like
                                # the UCI syntax does, as it's not necessary.
                                "monthdays": {
                                    "type": "array",
                                    "title": "monthdays",
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
                                    "title": "utc_time",
                                    "description": "Treat all given time values as UTC time instead of local "
                                    "time.",
                                    "default": False,
                                    "propertyOrder": 20,
                                },
                                "target": {
                                    "type": "string",
                                    "title": "target",
                                    "description": "NAT target (DNAT or SNAT) to use when generating the "
                                    "rule.",
                                    "enum": ["DNAT", "SNAT"],
                                    "default": "DNAT",
                                    "propertyOrder": 21,
                                },
                                "family": {
                                    "type": "string",
                                    "title": "family",
                                    "description": "Protocol family (ipv4, ipv6 or any) to generate iptables "
                                    "rules for",
                                    "enum": ["ipv4", "ipv6", "any"],
                                    "default": "any",
                                    "propertyOrder": 22,
                                },
                                "reflection": {
                                    "type": "boolean",
                                    "title": "reflection",
                                    "description": "Activate NAT reflection for this redirect. Applicable to "
                                    "DNAT targets.",
                                    "default": True,
                                    "propertyOrder": 23,
                                },
                                "reflection_src": {
                                    "type": "string",
                                    "title": "reflection_src",
                                    "description": "The source address to use for NAT-reflected packets if "
                                    "reflection is True. This can be internal or external, specifying which "
                                    "interface’s address to use. Applicable to DNAT targets.",
                                    "enum": ["internal", "external"],
                                    "default": "internal",
                                    "propertyOrder": 24,
                                },
                                "limit": {
                                    "type": "string",
                                    "title": "limit",
                                    "description": "Maximum average matching rate; specified as a number, "
                                    "with an optional /second, /minute, /hour or /day suffix. "
                                    "Examples: 3/second, 3/sec or 3/s.",
                                    "propertyOrder": 25,
                                },
                                "limit_burst": {
                                    "type": "integer",
                                    "title": "limit_burst",
                                    "description": "Maximum initial number of packets to match, allowing a "
                                    "short-term average above limit.",
                                    "default": 5,
                                    "propertyOrder": 26,
                                },
                                "enabled": {
                                    "type": "boolean",
                                    "title": "enable",
                                    "description": "Enable this redirect.",
                                    "default": True,
                                    "format": "checkbox",
                                    "propertyOrder": 27,
                                },
                            },
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
