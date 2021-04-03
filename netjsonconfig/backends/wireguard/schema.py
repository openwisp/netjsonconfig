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
                                    "maxLength": 44,
                                    "minLength": 1,
                                    "pattern": "^[^\\s]*$",
                                    "propertyOrder": 1,
                                },
                                "allowed_ips": {
                                    "title": "allowed IP addresses",
                                    "type": "string",
                                    "minLength": 1,
                                    "propertyOrder": 2,
                                },
                                "endpoint_host": {
                                    "title": "endpoint host",
                                    "type": "string",
                                    "propertyOrder": 3,
                                },
                                "endpoint_port": {
                                    "title": "endpoint port",
                                    "type": "integer",
                                    "description": (
                                        "Wireguard port. Will be ignored if "
                                        "\"endpoint host\" is left empty."
                                    ),
                                    "default": 51820,
                                    "maximum": 65535,
                                    "minimum": 1,
                                    "propertyOrder": 4,
                                },
                                "preshared_key": {
                                    "title": "pre-shared key",
                                    "description": (
                                        "Optional shared secret, to provide an "
                                        "additional layer of symmetric-key cryptography "
                                        "for post-quantum resistance"
                                    ),
                                    "type": "string",
                                    "maxLength": 44,
                                    "pattern": "^[^\\s]*$",
                                    "propertyOrder": 5,
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
