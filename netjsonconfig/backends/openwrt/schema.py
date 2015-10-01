"""
OpenWrt specific JSON-Schema definition
"""
from .timezones import timezones
from ...schema import schema as default_schema
from ...utils import merge_dict

schema = merge_dict(default_schema, {
    "properties": {
        "general": {
            "properties": {
                "timezone": {
                    "id": "timezone",
                    "type": "string",
                    "default": "Coordinated Universal Time",
                    "enum": list(timezones.keys())
                }
            }
        },
        "radios": {
            "items": {
                "properties": {
                    "driver": {
                        "id": "driver",
                        "type": "string",
                        "enum": [
                            "mac80211",
                            "ath5k",
                            "ath9k",
                            "broadcom"
                        ]
                    },
                    "protocol": {
                        "id": "protocol",
                        "type": "string",
                        "enum": [
                            "802.11a",
                            "802.11b",
                            "802.11g",
                            "802.11n",
                            "802.11ac"
                        ]
                    }
                }
            }
        },
        "ntp": {
            "id": "ntp",
            "type": "object",
            "title": "ntp settings",
            "additionalProperties": True,
            "properties": {
                "enabled": {
                    "id": "enabled",
                    "type": "boolean"
                },
                "enable_server": {
                    "id": "enable_server",
                    "type": "boolean"
                },
                "server": {
                    "id": "server",
                    "type": "array"
                }
            }
        },
        "ip_rules": {
            "id": "ip_rules",
            "type": "array",
            "title": "Ip rules",
            "uniqueItems": True,
            "additionalItems": True,
            "items": {
                "type": "object",
                "title": "Ip rule",
                "additionalProperties": True,
                "properties": {
                    "in": {
                        "id": "in",
                        "type": "string"
                    },
                    "out": {
                        "id": "out",
                        "type": "string"
                    },
                    "src": {
                        "id": "src",
                        "type": "string"
                    },
                    "dest": {
                        "id": "dest",
                        "type": "string"
                    },
                    "tos": {
                        "id": "tos",
                        "type": "integer"
                    },
                    "mark": {
                        "id": "mark",
                        "type": "string"
                    },
                    "invert": {
                        "id": "invert",
                        "type": "boolean",
                        "default": False
                    },
                    "lookup": {
                        "id": "invert",
                        "type": "string"
                    },
                    "goto": {
                        "id": "goto",
                        "type": "integer"
                    },
                    "action": {
                        "id": "action",
                        "type": "string",
                        "enum": [
                            "prohibit",
                            "unreachable",
                            "blackhole",
                            "throw"
                        ]
                    }
                }
            }
        },
        "led": {
            "id": "led",
            "type": "array",
            "title": "LED config",
            "uniqueItems": True,
            "additionalItems": True,
            "items": {
                "type": "object",
                "title": "LED",
                "additionalProperties": True,
                "required": [
                    "name",
                    "sysfs",
                    "trigger"
                ],
                "properties": {
                    "name": {
                        "id": "name",
                        "type": "string"
                    },
                    "default": {
                        "id": "default",
                        "type": "boolean"
                    },
                    "dev": {
                        "id": "dev",
                        "type": "string"
                    },
                    "sysfs": {
                        "id": "sysfs",
                        "type": "string"
                    },
                    "trigger": {
                        "id": "trigger",
                        "type": "string"
                    },
                    "delayoff": {
                        "id": "delayoff",
                        "type": "integer"
                    },
                    "delayon": {
                        "id": "delayon",
                        "type": "integer"
                    },
                    "interval": {
                        "id": "interval",
                        "type": "integer"
                    },
                    "message": {
                        "id": "message",
                        "type": "string"
                    },
                    "mode": {
                        "id": "mode",
                        "type": "string"
                    }
                }
            }
        },
        "switch": {
            "id": "switch",
            "type": "array",
            "title": "VLANs",
            "uniqueItems": True,
            "additionalItems": True,
            "title": "Programmable Switch",
            "items": {
                "type": "object",
                "additionalProperties": True,
                "required": [
                    "name",
                    "reset",
                    "enable_vlan",
                    "vlan"
                ],
                "properties": {
                    "name": {
                        "id": "name",
                        "type": "string"
                    },
                    "reset": {
                        "id": "reset",
                        "type": "boolean"
                    },
                    "enable_vlan": {
                        "id": "enable_vlan",
                        "type": "boolean"
                    },
                    "vlan": {
                        "id": "vlan",
                        "type": "array",
                        "title": "VLANs",
                        "uniqueItems": True,
                        "additionalItems": True,
                        "items": {
                            "type": "object",
                            "title": "VLAN",
                            "additionalProperties": True,
                            "required": [
                                "device",
                                "vlan",
                                "ports"
                            ],
                            "properties": {
                                "device": {
                                    "id": "device",
                                    "type": "string"
                                },
                                "vlan": {
                                    "id": "vlan",
                                    "type": "integer"
                                },
                                "ports": {
                                    "id": "ports",
                                    "type": "string"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})

# add interface protos
schema['properties']['interfaces']['items']['properties']\
      ['addresses']['items']['properties']['proto']['enum'] += [
    'dhcpv6',
    'ppp',
    'pppoe',
    'pppoa',
    '3g',
    'qmi',
    'ncm',
    'hnet',
    'pptp',
    '6in4',
    'aiccu',
    '6to4',
    '6rd',
    'dslite',
    'l2tp',
    'relay',
    'gre',
    'gretap',
    'grev6',
    'grev6tap'
]

# mark driver and protocol as required
schema['properties']['radios']['items']['required'] += [
    'driver',
    'protocol'
]
