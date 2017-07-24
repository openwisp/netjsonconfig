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
                    "authoneg": {
                        "type": "boolean",
                    },
                    "flowcontrol": {
                        "type": "boolean",
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
            },
            "user": {
                "additionalProperties": True,
                "properties": {
                    "name": {
                        "type": "string",
                    },
                    "salt": {
                        "type": "string",
                    },
                },
                "required": [
                    "name",
                    "password",
                    "salt",
                ],
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
        },
    }

schema = merge_config(
        default_schema,
        override_schema
        )

__all__ = [schema]
