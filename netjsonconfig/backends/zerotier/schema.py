"""
ZeroTier specific JSON-Schema definition
"""

from copy import deepcopy

from ...schema import schema as default_schema

# The schema is taken from OpenAPI specification:
# https://docs.zerotier.com/service/v1/ (self-hosted controllers)
# https://docs.zerotier.com/openapi/centralv1.json (central controllers)
base_zerotier_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "additionalProperties": True,
    "properties": {
        "zerotier": {
            "type": "array",
            "title": "ZeroTier",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 12,
            "items": {
                "type": "object",
                "title": "ZeroTier",
                "additionalProperties": True,
                "required": ["name", "id"],
                "properties": {
                    "id": {
                        "title": "network id",
                        "description": "ZeroTier network ID",
                        "type": "string",
                        "minLength": 16,
                        "maxLength": 16,
                        "propertyOrder": 1,
                    },
                    "nwid": {
                        "title": "network id (legacy field)",
                        "description": "ZeroTier network ID (legacy field)",
                        "type": "string",
                        "minLength": 16,
                        "maxLength": 16,
                        "propertyOrder": 2,
                    },
                    "name": {
                        "title": "network name",
                        "description": "ZeroTier network name",
                        "type": "string",
                        "propertyOrder": 3,
                    },
                    "private": {
                        "title": "private",
                        "type": "boolean",
                        "description": (
                            "Whether or not the zerotier network is private."
                            "If false, members will NOT need to be authorized to join.",
                        ),
                        "propertyOrder": 4,
                    },
                },
            },
        }
    },
}

schema = deepcopy(base_zerotier_schema)
schema['required'] = ['zerotier']
schema['properties']['files'] = default_schema['properties']['files']
