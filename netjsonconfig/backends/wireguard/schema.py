"""
Wireguard specific JSON-Schema definition
"""
from copy import deepcopy

from ...schema import schema as default_schema

base_wireguard_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "additionalProperties": True,
    "properties": {
        "wireguard": {
            "type": "array",
            "title": "Wireguard",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 12,
            "items": {
                "type": "object",
                "title": "Wireguard tunnel",
                "additionalProperties": True,
                "required": ["name", "port", "private_key"],
                "properties": {
                    "name": {
                        "title": "interface name",
                        "description": "Wireguard interface name",
                        "type": "string",
                        "minLength": 2,
                        "maxLength": 15,
                        "pattern": "^[^\\s]*$",
                        "propertyOrder": 1,
                    },
                    "port": {
                        "title": "port",
                        "type": "integer",
                        "default": 51820,
                        "maximum": 65535,
                        "minimum": 1,
                        "propertyOrder": 2,
                    },
                    "private_key": {
                        "title": "private key",
                        "type": "string",
                        "minLength": 44,
                        "maxLength": 44,
                        "pattern": "^[^\\s]*$",
                        "propertyOrder": 3,
                    },
                    "peers": {
                        "type": "array",
                        "title": "Peers",
                        "uniqueItems": True,
                        "additionalItems": True,
                        "propertyOrder": 11,
                        "items": {
                            "type": "object",
                            "title": "Peer",
                            "required": ["public_key", "allowed_ips"],
                            "properties": {
                                "public_key": {
                                    "title": "public key",
                                    "type": "string",
                                    "minLength": 44,
                                    "maxLength": 44,
                                    "pattern": "^[^\\s]*$",
                                    "propertyOrder": 1,
                                },
                                "allowed_ips": {
                                    "title": "public key",
                                    "type": "string",
                                    "propertyOrder": 2,
                                },
                                "endpoint": {
                                    "title": "public key",
                                    "type": "string",
                                    "propertyOrder": 3,
                                },
                                "preshared_key": {
                                    "title": "pre-shared key",
                                    "type": "string",
                                    "minLength": 44,
                                    "maxLength": 44,
                                    "pattern": "^[^\\s]*$",
                                    "propertyOrder": 4,
                                },
                            },
                        },
                    },
                },
            },
        }
    },
}

schema = deepcopy(base_wireguard_schema)
schema['required'] = ['wireguard']
schema['properties']['files'] = default_schema['properties']['files']
