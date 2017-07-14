"""
AirOS specific JSON-Schema definition
"""
from ...schema import schema as default_schema
from ...schema import DEFAULT_FILE_MODE  # noqa - backward compatibility
from ...utils import merge_config

"""
This defines a new property in the ``Interface``.

The management interface is the one that exposes the
web interface

It can be used on a single interface (ethernet, vlan) or
on a bridge
"""

netconf_schema = {
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
            }
        }
    }

"""
This schema defines a new property for netjson

As the antenna can be in ``bridge`` or ``router`` mode
this mode can be selected from this property
"""

netmode_schema = {
        "type": "object",
        "properties": {
            "netmode": {
                "enum": [
                    "bridge",
                    "router",
                ],
                "default": "bridge",
                "type": "string",
            },
        },
    }

"""
This schema override the possible encryption for AirOS from the default schema
"""
wpasupplicant_schema = {
    "encryption_wireless_property_sta": {
        "properties": {
            "encryption": {
                "type": "object",
                "title": "Encryption",
                "required": "protocol",
                "propertyOrder": 20,
                "oneOf": [
                    {"$ref": "#/definitions/encryption_none"},
                    {"$ref": "#/definitions/encryption_wpa_personal"},
                    {"$ref": "#/definitions/encryption_wpa_enterprise_sta"},
                ],
            },
        },
    },
    "encryption_wireless_property_ap": {
        "properties": {
            "encryption": {
                "type": "object",
                "title": "Encryption",
                "required": "protocol",
                "propertyOrder": 20,
                "oneOf": [
                    {"$ref": "#/definitions/encryption_none"},
                    {"$ref": "#/definitions/encryption_wpa_personal"},
                    {"$ref": "#/definitions/encryption_wpa_enterprise_sta"},
                ],
            },
        },
    },
}


schema = merge_config(
        default_schema,
        netconf_schema,
        netmode_schema,
        wpasupplicant_schema,
    )
