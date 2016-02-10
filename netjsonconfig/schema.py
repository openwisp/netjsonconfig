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
                    "pattern": "^[^\\s]*$",
                    "propertyOrder": 1,
                },
                "mac": {
                    "type": "string",
                    "propertyOrder": 2,
                },
                "mtu": {
                    "type": "integer",
                    "default": 1500,
                    "propertyOrder": 3,
                },
                "txqueuelen": {
                    "type": "integer",
                    "propertyOrder": 4,
                },
                "autostart": {
                    "type": "boolean",
                    "default": True,
                    "propertyOrder": 5,
                },
                "disabled": {
                    "type": "boolean",
                    "default": False,
                    "propertyOrder": 6,
                },
                "addresses": {
                    "type": "array",
                    "title": "Addresses",
                    "uniqueItems": True,
                    "additionalItems": True,
                    "propertyOrder": 7,
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
                                ],
                                "propertyOrder": 1,
                            },
                            "family": {
                                "type": "string",
                                "enum": [
                                    "ipv4",
                                    "ipv6"
                                ],
                                "propertyOrder": 2,
                            },
                            "address": {
                                "type": "string",
                                "propertyOrder": 3,
                            },
                            "mask": {
                                "type": "integer",
                                "propertyOrder": 4,
                            },
                            "gateway": {
                                "type": "string",
                                "propertyOrder": 5,
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
                            ],
                            "propertyOrder": 0,
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
                            "default": "wireless",
                            "propertyOrder": 0,
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
                            "propertyOrder": 8,
                            "required": [
                                "radio",
                                "mode",
                                "ssid"
                            ],
                            "properties": {
                                "radio": {
                                    "type": "string",
                                    "propertyOrder": 1,
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
                                    ],
                                    "propertyOrder": 2,
                                },
                                "ssid": {
                                    "type": "string",
                                    "maxLength": 32,
                                    "propertyOrder": 3,
                                },
                                "bssid": {
                                    "type": "string",
                                    "propertyOrder": 4,
                                },
                                "hidden": {
                                    "type": "boolean",
                                    "default": False,
                                    "propertyOrder": 5,
                                },
                                "ack_distance": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "propertyOrder": 6,
                                },
                                "rts_threshold": {
                                    "type": "integer",
                                    "minimum": 0,
                                    "maximum": 2346,
                                    "propertyOrder": 7,
                                },
                                "frag_threshold": {
                                    "type": "integer",
                                    "minimum": 0,
                                    "maximum": 2346,
                                    "propertyOrder": 8,
                                },
                                "encryption": {
                                    "type": "object",
                                    "title": "Encryption",
                                    "required": [
                                        "protocol",
                                        "key"
                                    ],
                                    "propertyOrder": 9,
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
                                            ],
                                            "propertyOrder": 1,
                                        },
                                        "disabled": {
                                            "type": "boolean",
                                            "default": False,
                                            "propertyOrder": 2,
                                        },
                                        "key": {
                                            "type": "string",
                                            "propertyOrder": 3,
                                        },
                                        "ciphers": {
                                            "type": "array",
                                            "propertyOrder": 4,
                                            "items": {
                                                "type": "string"
                                            }
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
                            "enum": ["bridge"],
                            "propertyOrder": 0
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
                            "propertyOrder": 8,
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
            "enum": ["DeviceConfiguration"],
            "propertyOrder": 0,
        },
        "general": {
            "type": "object",
            "title": "General",
            "additionalProperties": True,
            "propertyOrder": 1,
            "properties": {
                "hostname": {
                    "type": "string",
                    "maxLength": 63,
                    "minLength": 1,
                    "propertyOrder": 1,
                },
                "maintainer": {
                    "type": "string",
                    "propertyOrder": 2,
                },
                "description": {
                    "type": "string",
                    "propertyOrder": 3,
                }
            }
        },
        "interfaces": {
            "type": "array",
            "title": "Interfaces",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 2,
            "items": {
                "oneOf": [
                    {"$ref": "#/definitions/network_interface"},
                    {"$ref": "#/definitions/wireless_interface"},
                    {"$ref": "#/definitions/bridge_interface"}
                ]
            }
        },
        "dns_servers": {
            "title": "DNS Servers",
            "type": "array",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 3,
            "items": {
                "type": "string"
            }
        },
        "dns_search": {
            "title": "DNS Search",
            "type": "array",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 4,
            "items": {
                "type": "string"
            }
        },
        "radios": {
            "type": "array",
            "title": "Radios",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 5,
            "items": {
                "type": "object",
                "title": "Radio",
                "additionalProperties": True,
                "required": [
                    "name",
                    "channel",
                    "channel_width",
                ],
                "properties": {
                    "name": {
                        "type": "string",
                        "propertyOrder": 1,
                    },
                    "phy": {
                        "type": "string",
                        "propertyOrder": 2,
                    },
                    "channel": {
                        "type": "integer",
                        "propertyOrder": 3,
                    },
                    "channel_width": {
                        "type": "integer",
                        "propertyOrder": 4,
                    },
                    "tx_power": {
                        "type": "integer",
                        "propertyOrder": 5,
                    },
                    "country": {
                        "type": "string",
                        "minLength": 2,
                        "maxLength": 2,
                        "propertyOrder": 5,
                    },
                    "disabled": {
                        "type": "boolean",
                        "default": False,
                        "propertyOrder": 6,
                    }
                }
            }
        },
        "routes": {
            "type": "array",
            "title": "Routes",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 6,
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
                        "type": "string",
                        "propertyOrder": 1,
                    },
                    "next": {
                        "type": "string",
                        "propertyOrder": 2,
                    },
                    "destination": {
                        "type": "string",
                        "propertyOrder": 3,
                    }
                }
            }
        }
    }
}
