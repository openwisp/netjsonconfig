"""
AirOS specific JSON-Schema definition
"""
from ...schema import schema as default_schema
from ...utils import merge_config

"""
This defines a new property in the ``Interface``.

The management interface is the one that exposes the
web interface

It can be used on a single interface (ethernet, vlan) or
on a bridge
"""

default_ntp_servers = [
    "0.pool.ntp.org",
    "1.pool.ntp.org",
    "2.pool.ntp.org",
    "3.pool.ntp.org",
]

override_schema = {
    "type": "object",
    "addtionalProperties": True,
    "definitions": {
        "base_address": {
            "properties": {
                "management": {
                    "type": "boolean",
                    "default": False,
                }
            }
        },
        "encryption_wireless_property_ap": {
            "properties": {
                "encryption": {
                    "type": "object",
                    "title": "Encryption",
                    "required": [
                        "protocol",
                    ],
                    "propertyOrder": 20,
                    "oneOf": [
                        {"$ref": "#/definitions/encryption_none"},
                        {"$ref": "#/definitions/encryption_wpa_personal"},
                        {"$ref": "#/definitions/encryption_wpa_enterprise_sta"},
                    ],
                },
            },
        },
        "encryption_wireless_property_sta": {
            "properties": {
                "encryption": {
                    "type": "object",
                    "title": "Encryption",
                    "required": [
                        "protocol",
                    ],
                    "propertyOrder": 20,
                    "oneOf": [
                        {"$ref": "#/definitions/encryption_none"},
                        {"$ref": "#/definitions/encryption_wpa_personal"},
                        {"$ref": "#/definitions/encryption_wpa_enterprise_sta"},
                    ],
                },
            },
        },
        "interface_settings": {
            "properties": {
                "autoneg": {
                    "type": "boolean",
                    "default": False,
                    "title": "Auto negotiation",
                    "description": "Enable autonegotiation on interface",
                },
                "flowcontrol": {
                    "type": "boolean",
                    "default": False,
                    "title": "Flow control",
                    "description": "Enable flow control on interface",
                }
            }
        }
    },
    "properties": {
        "netmode": {
            "enum": [
                "bridge",
                "router",
            ],
            "default": "bridge",
            "type": "string",
            "title": "Network mode for device",
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
                        "format": "hostname"
                    },
                    "default": default_ntp_servers,
                }
            }
        },
        "sshd": {
            "type": "object",
            "title": "SSHd settings",
            "additionalProperties": True,
            "properties": {
                "port": {
                    "type": "integer",
                    "default": 22,
                    "title": "Port for sshd to listen on",
                },
                "enabled": {
                    "type": "boolean",
                    "default": True,
                    "title": "Enable ssh server",
                    "format": "checkbox",
                },
                "password_auth": {
                    "type": "boolean",
                    "default": True,
                    "title": "Enable password authentication",
                    "format": "checkbox",
                },
                "keys": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "title": "Key algorithm",
                            },
                            "key": {
                                "type": "string",
                                "title": "Key file content",
                            },
                            "comment": {
                                "type": "string",
                                "default": "",
                                "title": "comment",
                            },
                            "enabled": {
                                "type": "boolean",
                                "default": True,
                                "title": "Enable key",
                                "format": "checkbox",
                            },
                        }
                    }
                },
            },
        },
        "user": {
            "additionalProperties": True,
            "properties": {
                "name": {
                    "title": "User name",
                    "type": "string",
                },
                "password": {
                    "title": "Hashed password for user",
                    "type": "string",
                },
                "salt": {
                    "title": "Salt for hashing algorithm",
                    "type": "string",
                },
            },
            "required": [
                "name",
                "password",
                "salt",
            ],
        },
    },
}

schema = merge_config(default_schema, override_schema)

schema['definitions']['encryption_wireless_property_ap'] = \
    override_schema['definitions']['encryption_wireless_property_ap']

schema['definitions']['encryption_wireless_property_sta'] = \
    override_schema['definitions']['encryption_wireless_property_sta']
