"""
OpenWrt specific JSON-Schema definition
"""
from ...schema import schema as default_schema
from ...utils import merge_config
from .timezones import timezones

DEFAULT_FILE_MODE = '0644'

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
                    "default": "UTC",
                    "enum": list(timezones.keys()),
                    "propertyOrder": 1,
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
                        ],
                        "propertyOrder": 0,
                    },
                    "protocol": {
                        "type": "string",
                        "enum": [
                            "802.11a",
                            "802.11b",
                            "802.11g",
                            "802.11n",
                            "802.11ac"
                        ],
                        "propertyOrder": 1,
                    }
                }
            }
        },
        "ntp": {
            "type": "object",
            "title": "ntp settings",
            "additionalProperties": True,
            "propertyOrder": 7,
            "properties": {
                "enabled": {
                    "type": "boolean",
                    "default": True,
                    "propertyOrder": 1,
                },
                "enable_server": {
                    "type": "boolean",
                    "default": False,
                    "propertyOrder": 2,
                },
                "server": {
                    "type": "array",
                    "uniqueItems": True,
                    "additionalItems": True,
                    "propertyOrder": 3,
                    "items": {
                        "type": "string"
                    },
                    "default": [
                        "0.openwrt.pool.ntp.org",
                        "1.openwrt.pool.ntp.org",
                        "2.openwrt.pool.ntp.org",
                        "3.openwrt.pool.ntp.org",
                    ]
                }
            }
        },
        "switch": {
            "type": "array",
            "title": "VLANs",
            "uniqueItems": True,
            "additionalItems": True,
            "title": "Switch",
            "propertyOrder": 8,
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
                        "type": "string",
                        "propertyOrder": 1,
                    },
                    "reset": {
                        "type": "boolean",
                        "default": True,
                        "propertyOrder": 2,
                    },
                    "enable_vlan": {
                        "type": "boolean",
                        "title": "enable vlan",
                        "default": True,
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
                            "required": [
                                "device",
                                "vlan",
                                "ports"
                            ],
                            "properties": {
                                "device": {
                                    "type": "string",
                                    "propertyOrder": 1,
                                },
                                "vlan": {
                                    "type": "integer",
                                    "propertyOrder": 2,
                                },
                                "ports": {
                                    "type": "string",
                                    "propertyOrder": 3,
                                }
                            }
                        }
                    }
                }
            }
        },
        "ip_rules": {
            "type": "array",
            "title": "Ip rules",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 9,
            "items": {
                "type": "object",
                "title": "Ip rule",
                "additionalProperties": True,
                "properties": {
                    "in": {
                        "type": "string",
                        "propertyOrder": 1,
                    },
                    "out": {
                        "type": "string",
                        "propertyOrder": 2,
                    },
                    "src": {
                        "type": "string",
                        "propertyOrder": 3,
                    },
                    "dest": {
                        "type": "string",
                        "propertyOrder": 4,
                    },
                    "tos": {
                        "type": "integer",
                        "propertyOrder": 5,
                    },
                    "mark": {
                        "type": "string",
                        "propertyOrder": 6,
                    },
                    "invert": {
                        "type": "boolean",
                        "default": False,
                        "propertyOrder": 7,
                    },
                    "lookup": {
                        "type": "string",
                        "propertyOrder": 8,
                    },
                    "goto": {
                        "type": "integer",
                        "propertyOrder": 9,
                    },
                    "action": {
                        "type": "string",
                        "enum": [
                            "prohibit",
                            "unreachable",
                            "blackhole",
                            "throw"
                        ],
                        "propertyOrder": 10,
                    }
                }
            }
        },
        "led": {
            "type": "array",
            "title": "LED config",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 10,
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
                        "type": "string",
                        "propertyOrder": 1,
                    },
                    "default": {
                        "type": "boolean",
                        "propertyOrder": 2,
                    },
                    "dev": {
                        "type": "string",
                        "propertyOrder": 3,
                    },
                    "sysfs": {
                        "type": "string",
                        "propertyOrder": 4,
                    },
                    "trigger": {
                        "type": "string",
                        "propertyOrder": 5,
                    },
                    "delayoff": {
                        "type": "integer",
                        "propertyOrder": 6,
                    },
                    "delayon": {
                        "type": "integer",
                        "propertyOrder": 7,
                    },
                    "interval": {
                        "type": "integer",
                        "propertyOrder": 8,
                    },
                    "message": {
                        "type": "string",
                        "propertyOrder": 9,
                    },
                    "mode": {
                        "type": "string",
                        "propertyOrder": 10,
                    }
                }
            }
        },
        "files": {
            "type": "array",
            "title": "files",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 11,
            "items": {
                "type": "object",
                "title": "file",
                "additionalProperties": False,
                "required": [
                    "path",
                    "mode",
                    "contents"
                ],
                "properties": {
                    "path": {
                        "type": "string",
                        "propertyOrder": 1,
                    },
                    "mode": {
                        "type": "string",
                        "maxLength": 4,
                        "minLength": 3,
                        "pattern": "^[0-7]*$",
                        "default": DEFAULT_FILE_MODE,
                        "propertyOrder": 2,
                    },
                    "contents": {
                        "type": "string",
                        "format": "textarea",
                        "propertyOrder": 3,
                    },
                }
            }
        }
    }
})
