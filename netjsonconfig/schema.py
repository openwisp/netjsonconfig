"""
NetJSON DeviceConfiguration JSON-Schema definition
this should be up to date with the official spec:

http://netjson.org/rfc.html#DeviceConfiguration-schema
"""

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "additionalProperties": True,
    "definitions": {
        "interface_settings": {
            "type": "object",
            "additionalProperties": True,
            "required": [
                "name",
                "type"
            ],
            "properties": {
                "name": {
                    "type": "string",
                    "maxLength": 15,
                    "pattern": "^[^\\s]*$"
                },
                "mac": {
                    "type": "string"
                },
                "mtu": {
                    "type": "integer",
                    "default": 1500
                },
                "txqueuelen": {
                    "type": "integer"
                },
                "autostart": {
                    "type": "boolean",
                    "default": True
                },
                "disabled": {
                    "type": "boolean",
                    "default": False
                },
                "addresses": {
                    "type": "array",
                    "title": "Addresses",
                    "uniqueItems": True,
                    "additionalItems": True,
                    "items": {
                        "type": "object",
                        "title": "Address",
                        "additionalProperties": True,
                        "required": [
                            "proto",
                            "family"
                        ],
                        "properties": {
                            "proto": {
                                "type": "string",
                                "enum": [
                                    "static",
                                    "dhcp"
                                ]
                            },
                            "family": {
                                "type": "string",
                                "enum": [
                                    "ipv4",
                                    "ipv6"
                                ]
                            },
                            "address": {
                                "type": "string"
                            },
                            "mask": {
                                "type": "integer"
                            },
                            "gateway": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        },
        "network_interface": {
            "title": "Network interface",
            "allOf": [
                {
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": [
                                "ethernet",
                                "virtual",
                                "loopback",
                                "other"
                            ]
                        }
                    }
                },
                {"$ref": "#/definitions/interface_settings"}
            ]
        },
        "wireless_interface": {
            "title": "Wireless interface",
            "allOf": [
                {
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["wireless"],
                            "default": "wireless"
                        }
                    }
                },
                {"$ref": "#/definitions/interface_settings"},
                {
                    "properties": {
                        "wireless": {
                            "type": "object",
                            "title": "Wireless Interface",
                            "additionalProperties": True,
                            "required": [
                                "radio",
                                "mode",
                                "ssid"
                            ],
                            "properties": {
                                "radio": {
                                    "type": "string"
                                },
                                "mode": {
                                    "type": "string",
                                    "enum": [
                                        "access_point",
                                        "station",
                                        "adhoc",
                                        "wds",
                                        "monitor",
                                        "802.11s"
                                    ]
                                },
                                "ssid": {
                                    "type": "string",
                                    "maxLength": 32
                                },
                                "bssid": {
                                    "type": "string"
                                },
                                "hidden": {
                                    "type": "boolean",
                                    "default": False
                                },
                                "ack_distance": {
                                    "type": "integer",
                                    "minimum": 1
                                },
                                "rts_threshold": {
                                    "type": "integer",
                                    "minimum": 0,
                                    "maximum": 2346
                                },
                                "frag_threshold": {
                                    "type": "integer",
                                    "minimum": 0,
                                    "maximum": 2346
                                },
                                "encryption": {
                                    "type": "object",
                                    "title": "Encryption",
                                    "required": [
                                        "protocol",
                                        "key"
                                    ],
                                    "properties": {
                                        "protocol": {
                                            "type": "string",
                                            "enum": [
                                                "wep_open",
                                                "wep_shared",
                                                "wpa_personal",
                                                "wpa2_personal",
                                                "wpa_personal_mixed",
                                                "wpa_enterprise",
                                                "wpa2_enterprise",
                                                "wpa_enterprise_mixed",
                                                "wps"
                                            ]
                                        },
                                        "key": {
                                            "type": "string"
                                        },
                                        "ciphers": {
                                            "type": "array",
                                            "items": {
                                                "type": "string"
                                            }
                                        },
                                        "disabled": {
                                            "type": "boolean",
                                            "default": False
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            ]
        },
        "bridge_interface": {
            "title": "Bridge interface",
            "required": [
                "bridge_members"
            ],
            "allOf": [
                {
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["bridge"]
                        }
                    }
                },
                {"$ref": "#/definitions/interface_settings"},
                {
                    "properties": {
                        "bridge_members": {
                            "type": "array",
                            "title": "Bridge Members",
                            "uniqueItems": True,
                            "items": {
                                "$ref": "#/definitions/interface_settings/properties/name"
                            }
                        }
                    }
                }
            ]
        }
    },
    "required": [
        "type"
    ],
    "properties": {
        "type": {
            "type": "string",
            "enum": ["DeviceConfiguration"]
        },
        "general": {
            "type": "object",
            "title": "General",
            "additionalProperties": True,
            "properties": {
                "hostname": {
                    "type": "string"
                },
                "maintainer": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                }
            }
        },
        "hardware": {
            "type": "object",
            "title": "Hardware",
            "additionalProperties": True,
            "properties": {
                "manufacturer": {
                    "type": "string"
                },
                "model": {
                    "type": "string"
                },
                "revision": {
                    "type": "integer"
                },
                "cpu": {
                    "type": "string"
                }
            }
        },
        "operating_system": {
            "type": "object",
            "title": "Operating System",
            "additionalProperties": True,
            "properties": {
                "name": {
                    "type": "string"
                },
                "kernel": {
                    "type": "string"
                },
                "version": {
                    "type": "string"
                },
                "revision": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                }
            }
        },
        "radios": {
            "type": "array",
            "title": "Radios",
            "uniqueItems": True,
            "additionalItems": True,
            "items": {
                "type": "object",
                "title": "Radio",
                "additionalProperties": True,
                "required": [
                    "name",
                    "channel",
                    "channel_width",
                    "tx_power"
                ],
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "phy": {
                        "type": "string"
                    },
                    "channel": {
                        "type": "integer"
                    },
                    "channel_width": {
                        "type": "integer"
                    },
                    "tx_power": {
                        "type": "integer"
                    },
                    "country": {
                        "type": "string",
                        "minLength": 2,
                        "maxLength": 2
                    },
                    "disabled": {
                        "type": "boolean",
                        "default": False
                    }
                }
            }
        },
        "interfaces": {
            "type": "array",
            "title": "Interfaces",
            "uniqueItems": True,
            "additionalItems": True,
            "items": {
                "oneOf": [
                    {"$ref": "#/definitions/network_interface"},
                    {"$ref": "#/definitions/wireless_interface"},
                    {"$ref": "#/definitions/bridge_interface"}
                ]
            }
        },
        "routes": {
            "type": "array",
            "title": "Routes",
            "uniqueItems": True,
            "additionalItems": True,
            "items": {
                "type": "object",
                "title": "Route",
                "additionalProperties": True,
                "required": [
                    "device",
                    "destination",
                    "next"
                ],
                "properties": {
                    "device": {
                        "type": "string"
                    },
                    "next": {
                        "type": "string"
                    },
                    "destination": {
                        "type": "string"
                    }
                }
            }
        },
        "dns_servers": {
            "title": "DNS Servers",
            "type": "array",
            "uniqueItems": True,
            "additionalItems": True,
            "items": {
                "type": "string"
            }
        },
        "dns_search": {
            "title": "DNS Search",
            "type": "array",
            "uniqueItems": True,
            "additionalItems": True,
            "items": {
                "type": "string"
            }
        }
    }
}
