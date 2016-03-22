"""
JSON-Schema implementation of NetJSON DeviceConfiguration
http://netjson.org/rfc.html
"""

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "additionalProperties": True,
    "definitions": {
        "base_address": {
            "type": "object",
            "additionalProperties": True,
            "required": [
                "proto",
                "family",
            ],
            "properties": {
                "proto": {
                    "title": "protocol",
                    "type": "string",
                    "propertyOrder": 1,
                },
                "family": {
                    "type": "string",
                    "propertyOrder": 2,
                }
            }
        },
        "static_address": {
            "required": [
                "address",
                "mask"
            ],
            "properties": {
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
        },
        "ipv4_address": {
            "title": "ipv4",
            "allOf": [
                {"$ref": "#/definitions/base_address"},
                {"$ref": "#/definitions/static_address"},
                {
                    "type": "object",
                    "properties": {
                        "proto": {"enum": ["static"]},
                        "family": {"enum": ["ipv4"]},
                        "address": {
                            "minLength": 8,
                            "maxLength": 16,
                            "format": "ipv4",
                        },
                        "mask": {
                            "minimum": 8,
                            "maxmium": 32,
                            "default": 24,
                        },
                        "gateway": {
                            "minLength": 8,
                            "maxLength": 16,
                            "format": "ipv4",
                        }
                    }
                }
            ]
        },
        "ipv6_address": {
            "title": "ipv6",
            "allOf": [
                {"$ref": "#/definitions/base_address"},
                {"$ref": "#/definitions/static_address"},
                {
                    "type": "object",
                    "required": [
                        "address",
                        "mask"
                    ],
                    "properties": {
                        "proto": {"enum": ["static"]},
                        "family": {"enum": ["ipv6"]},
                        "address": {
                            "minLength": 3,
                            "maxLength": 45,
                            "format": "ipv6",
                            "propertyOrder": 3,
                        },
                        "mask": {
                            "minimum": 4,
                            "maxmium": 128,
                            "default": 64,
                        },
                        "gateway": {
                            "minLength": 3,
                            "maxLength": 45,
                            "format": "ipv6",
                        }
                    }
                }
            ]
        },
        "dhcp_address": {
            "title": "DHCP",
            "allOf": [
                {"$ref": "#/definitions/base_address"},
                {
                    "type": "object",
                    "properties": {
                        "proto": {"enum": ["dhcp"]},
                        "family": {"enum": ["ipv4", "ipv6"]}
                    }
                }
            ]
        },
        "interface_settings": {
            "type": "object",
            "title": "Interface settings",
            "additionalProperties": True,
            "required": [
                "name",
                "type"
            ],
            "properties": {
                "name": {
                    "type": "string",
                    "maxLength": 15,
                    "minLenght": 2,
                    "pattern": "^[^\\s]*$",
                    "propertyOrder": 0,
                },
                "mac": {
                    "type": "string",
                    "title": "mac address",
                    "minLength": 17,
                    "maxLength": 17,
                    "propertyOrder": 2,
                },
                "mtu": {
                    "type": "integer",
                    "title": "MTU",
                    "default": 1500,
                    "minimum": 68,
                    "propertyOrder": 3,
                },
                "autostart": {
                    "type": "boolean",
                    "default": True,
                    "format": "checkbox",
                    "propertyOrder": 5,
                },
                "disabled": {
                    "type": "boolean",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 6,
                },
                "addresses": {
                    "type": "array",
                    "title": "Addresses",
                    "uniqueItems": True,
                    "additionalItems": True,
                    "propertyOrder": 20,
                    "items": {
                        "title": "Address",
                        "oneOf": [
                            {"$ref": "#/definitions/dhcp_address"},
                            {"$ref": "#/definitions/ipv4_address"},
                            {"$ref": "#/definitions/ipv6_address"},
                        ]
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
                            "propertyOrder": 1,
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
                            "propertyOrder": 1,
                        },
                        "wireless": {
                            "type": "object",
                            "propertyOrder": 10,
                            "oneOf": [
                                {"$ref": "#/definitions/ap_wireless_settings"},
                                {"$ref": "#/definitions/sta_wireless_settings"},
                                {"$ref": "#/definitions/adhoc_wireless_settings"},
                                {"$ref": "#/definitions/monitor_wireless_settings"},
                                {"$ref": "#/definitions/mesh_wireless_settings"},
                            ]
                        }
                    }
                },
                {"$ref": "#/definitions/interface_settings"},
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
                            "propertyOrder": 1
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
                                "title": "bridged interface",
                                "type": "string",
                                "$ref": "#/definitions/interface_settings/properties/name"
                            }
                        }
                    }
                }
            ]
        },
        "base_wireless_settings": {
            "type": "object",
            "title": "Wireless Settings",
            "additionalProperties": True,
            "propertyOrder": 8,
            "required": [
                "radio",
                "mode",
            ],
            "properties": {
                "mode": {
                    "type": "string",
                    "propertyOrder": 1,
                },
                "radio": {
                    "type": "string",
                    "minLength": 2,
                    "propertyOrder": 2,
                },
                "ack_distance": {
                    "type": "integer",
                    "title": "ACK distance",
                    "minimum": 0,
                    "propertyOrder": 10,
                },
                "rts_threshold": {
                    "type": "integer",
                    "title": "RTS threshold",
                    "minimum": 0,
                    "maximum": 2346,
                    "propertyOrder": 11,
                },
                "frag_threshold": {
                    "type": "integer",
                    "title": "fragmentation threshold",
                    "minimum": 0,
                    "maximum": 2346,
                    "propertyOrder": 12,
                }
            }
        },
        "ssid_wireless_property": {
            "required": ["ssid"],
            "properties": {
                "ssid": {
                    "type": "string",
                    "title": "SSID",
                    "maxLength": 32,
                    "propertyOrder": 3,
                }
            }
        },
        "hidden_wireless_property": {
            "properties": {
                "hidden": {
                    "type": "boolean",
                    "title": "hide SSID",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 4,
                }
            }
        },
        "bssid_wireless_property": {
            "required": ["bssid"],
            "properties": {
                "bssid": {
                    "type": "string",
                    "title": "BSSID",
                    "minLength": 17,
                    "maxLength": 17,
                    "propertyOrder": 4,
                },
            }
        },
        "wds_wireless_property": {
            "properties": {
                "wds": {
                    "title": "WDS",
                    "type": "boolean",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 5,
                }
            }
        },
        "mesh_id_wireless_property": {
            "required": ["mesh_id"],
            "properties": {
                "mesh_id": {
                    "type": "string",
                    "title": "mesh ID",
                    "pattern": "^[^\\s]*$",
                    "propertyOrder": 3,
                },
            }
        },
        "encryption_wireless_property": {
            "properties": {
                "encryption": {
                    "type": "object",
                    "title": "Encryption",
                    "required": [
                        "protocol",
                        "key"
                    ],
                    "propertyOrder": 20,
                    "properties": {
                        "protocol": {
                            "type": "string",
                            "enum": [
                                "none",
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
                            "format": "checkbox",
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
                                "type": "string",
                                "enum": [
                                    "tkip",
                                    "ccmp",
                                    "aes",
                                ]
                            }
                        }
                    }
                }
            }
        },
        "ap_wireless_settings": {
            "title": "Access Point",
            "allOf": [
                {"properties": {"mode": {"enum": ["access_point"]}}},
                {"$ref": "#/definitions/base_wireless_settings"},
                {"$ref": "#/definitions/ssid_wireless_property"},
                {"$ref": "#/definitions/hidden_wireless_property"},
                {"$ref": "#/definitions/wds_wireless_property"},
                {"$ref": "#/definitions/encryption_wireless_property"},
            ]
        },
        "sta_wireless_settings": {
            "title": "Station",
            "allOf": [
                {"properties": {"mode": {"enum": ["station"]}}},
                {"$ref": "#/definitions/base_wireless_settings"},
                {"$ref": "#/definitions/ssid_wireless_property"},
                {"$ref": "#/definitions/bssid_wireless_property"},
                {"$ref": "#/definitions/wds_wireless_property"},
                {"$ref": "#/definitions/encryption_wireless_property"},
            ]
        },
        "adhoc_wireless_settings": {
            "title": "Adhoc",
            "allOf": [
                {"properties": {"mode": {"enum": ["adhoc"]}}},
                {"$ref": "#/definitions/base_wireless_settings"},
                {"$ref": "#/definitions/ssid_wireless_property"},
                {"$ref": "#/definitions/bssid_wireless_property"},
                {"$ref": "#/definitions/encryption_wireless_property"},
            ]
        },
        "monitor_wireless_settings": {
            "title": "Monitor",
            "allOf": [
                {"properties": {"mode": {"enum": ["monitor"]}}},
                {"$ref": "#/definitions/base_wireless_settings"},
            ]
        },
        "mesh_wireless_settings": {
            "title": "802.11s (mesh)",
            "allOf": [
                {"properties": {"mode": {"enum": ["802.11s"]}}},
                {"$ref": "#/definitions/base_wireless_settings"},
                {"$ref": "#/definitions/mesh_id_wireless_property"},
                {"$ref": "#/definitions/encryption_wireless_property"},
            ]
        }
    },
    "properties": {
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
                "ula_prefix": {
                    "type": "string",
                    "title": "ULA prefix",
                    "propertyOrder": 2,
                },
                "maintainer": {
                    "type": "string",
                    "propertyOrder": 3,
                },
                "description": {
                    "type": "string",
                    "propertyOrder": 4,
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
                "title": "Interface",
                "oneOf": [
                    {"$ref": "#/definitions/network_interface"},
                    {"$ref": "#/definitions/wireless_interface"},
                    {"$ref": "#/definitions/bridge_interface"}
                ]
            }
        },
        "radios": {
            "type": "array",
            "title": "Radios",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 3,
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
                        "minLength": 3
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
                        "title": "channel width",
                        "propertyOrder": 4,
                    },
                    "tx_power": {
                        "type": "integer",
                        "title": "tx power",
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
                        "format": "checkbox",
                        "propertyOrder": 6,
                    }
                }
            }
        },
        "dns_servers": {
            "title": "DNS Configuration",
            "type": "array",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 4,
            "items": {
                "title": "DNS Server",
                "type": "string"
            }
        },
        "dns_search": {
            "title": "DNS Search List",
            "type": "array",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 5,
            "items": {
                "title": "Domain",
                "type": "string"
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
                    "next",
                    "cost"
                ],
                "properties": {
                    "device": {
                        "type": "string",
                        "propertyOrder": 1,
                    },
                    "destination": {
                        "type": "string",
                        "propertyOrder": 2,
                    },
                    "next": {
                        "title": "next hop",
                        "type": "string",
                        "propertyOrder": 2,
                    },
                    "cost": {
                        "type": "integer",
                        "propertyOrder": 4,
                        "default": 0,
                    },
                    "source": {
                        "type": "string",
                        "propertyOrder": 5,
                    }
                }
            }
        }
    }
}
