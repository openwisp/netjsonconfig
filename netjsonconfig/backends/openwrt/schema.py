"""
OpenWrt specific JSON-Schema definition
"""
from .timezones import timezones
from ...schema import schema as default_schema
from ...utils import merge_config

schema = merge_config(default_schema, {
    "definitions": {
        "interface_settings": {
            "properties": {
                "network": {
                    "type": "string",
                    "maxLength": 9,
                    "pattern": "^[a-zA-z0-9_]*$"
                },
                "addresses": {
                    "items": {
                        "properties": {
                            "proto": {
                                "enum": [
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
                                    'grev6tap',
                                    'none'
                                ]
                            }
                        }
                    }
                }
            }
        },
        "wireless_interface": {
            "properties": {
                "wireless": {
                    "properties": {
                        "network": {
                            "type": "array",
                            "uniqueItems": True,
                            "additionalItems": True,
                            "minItems": 1,
                            "items": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        }
    },
    "properties": {
        "general": {
            "properties": {
                "timezone": {
                    "type": "string",
                    "default": "Coordinated Universal Time",
                    "enum": list(timezones.keys())
                }
            }
        },
        "radios": {
            "items": {
                "required": [
                    "driver",
                    "protocol"
                ],
                "properties": {
                    "driver": {
                        "type": "string",
                        "enum": [
                            "mac80211",
                            "madwifi",
                            "ath5k",
                            "ath9k",
                            "broadcom"
                        ]
                    },
                    "protocol": {
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
            "type": "object",
            "title": "ntp settings",
            "additionalProperties": True,
            "properties": {
                "enabled": {
                    "type": "boolean"
                },
                "enable_server": {
                    "type": "boolean"
                },
                "server": {
                    "type": "array",
                    "uniqueItems": True,
                    "additionalItems": True,
                    "items": {
                        "type": "string"
                    }
                }
            }
        },
        "ip_rules": {
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
                        "type": "string"
                    },
                    "out": {
                        "type": "string"
                    },
                    "src": {
                        "type": "string"
                    },
                    "dest": {
                        "type": "string"
                    },
                    "tos": {
                        "type": "integer"
                    },
                    "mark": {
                        "type": "string"
                    },
                    "invert": {
                        "type": "boolean",
                        "default": False
                    },
                    "lookup": {
                        "type": "string"
                    },
                    "goto": {
                        "type": "integer"
                    },
                    "action": {
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
                        "type": "string"
                    },
                    "default": {
                        "type": "boolean"
                    },
                    "dev": {
                        "type": "string"
                    },
                    "sysfs": {
                        "type": "string"
                    },
                    "trigger": {
                        "type": "string"
                    },
                    "delayoff": {
                        "type": "integer"
                    },
                    "delayon": {
                        "type": "integer"
                    },
                    "interval": {
                        "type": "integer"
                    },
                    "message": {
                        "type": "string"
                    },
                    "mode": {
                        "type": "string"
                    }
                }
            }
        },
        "switch": {
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
                        "type": "string"
                    },
                    "reset": {
                        "type": "boolean"
                    },
                    "enable_vlan": {
                        "type": "boolean"
                    },
                    "vlan": {
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
                                    "type": "string"
                                },
                                "vlan": {
                                    "type": "integer"
                                },
                                "ports": {
                                    "type": "string"
                                }
                            }
                        }
                    }
                }
            }
        },
        "files": {
            "type": "array",
            "title": "files",
            "uniqueItems": True,
            "additionalItems": True,
            "items": {
                "type": "object",
                "title": "file",
                "additionalProperties": False,
                "required": [
                    "path",
                    "contents"
                ],
                "properties": {
                    "path": {
                        "type": "string"
                    },
                    "contents": {
                        "anyOf": [
                            {"type": "string", "format": "textarea"},
                            {"type": "array"}
                        ]
                    },
                    "mode": {
                        "type": "string",
                        "maxLength": 4
                    }
                }
            }
        }
    }
})
