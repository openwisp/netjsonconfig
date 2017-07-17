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
        },
    }

schema = merge_config(
        default_schema,
        override_schema
        )

__all__ = [schema]
