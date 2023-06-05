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
                "title": "ZeroTier Network",
                "uniqueItems": True,
                "additionalProperties": True,
                "required": ["name"],
                "properties": {
                    # Read-only properties
                    "name": {
                        "type": "string",
                        # Since it is intended to be set by
                        # the VPN backend's name field, it is read-only
                        "readOnly": True,
                        "propertyOrder": 1,
                        "example": "openwisp-wifi-network",
                        "description": "Name of the network",
                    },
                    "id": {
                        "type": "string",
                        "maxLength": 16,
                        "readOnly": True,
                        "propertyOrder": 2,
                        "example": "3e245e31af000001",
                        "description": "Network ID",
                    },
                    "nwid": {
                        "type": "string",
                        "maxLength": 16,
                        "readOnly": True,
                        "propertyOrder": 3,
                        "example": "3e245e31af000001",
                        "description": "Network ID legacy field (same as 'id')",
                    },
                    "objtype": {
                        "type": "string",
                        "readOnly": True,
                        "propertyOrder": 4,
                        "default": "network",
                        "example": "network",
                    },
                    "revision": {
                        "type": "integer",
                        "example": 1,
                        "readOnly": True,
                        "propertyOrder": 5,
                        "description": "The revision number of the network configuration",
                    },
                    "creationTime": {
                        "type": "number",
                        "readOnly": True,
                        "propertyOrder": 6,
                        "example": 1623101592,
                        "description": "Time when the network was created",
                    },
                    # Configurable properties
                    "private": {
                        "type": "boolean",
                        "default": True,
                        "propertyOrder": 7,
                        "description": (
                            "Whether or not the network is private "
                            "If false, members will NOT need to be authorized to join"
                        ),
                    },
                    "enableBroadcast": {
                        "type": "boolean",
                        "propertyOrder": 8,
                        "description": "Enable broadcast packets on the network",
                    },
                    "v4AssignMode": {
                        "type": "object",
                        "propertyOrder": 9,
                        "properties": {
                            "zt": {
                                "type": "boolean",
                                "description": "Whether ZeroTier should assign IPv4 addresses to members",
                            },
                        },
                    },
                    "v6AssignMode": {
                        "type": "object",
                        "propertyOrder": 11,
                        "properties": {
                            "6plane": {
                                "type": "boolean",
                                "description": "Whether 6PLANE addressing should be used for IPv6 assignment",
                            },
                            "rfc4193": {
                                "type": "boolean",
                                "description": "Whether RFC4193 addressing should be used for IPv6 assignment",  # noqa
                            },
                            "zt": {
                                "type": "boolean",
                                "description": "Whether ZeroTier should assign IPv6 addresses to members",
                            },
                        },
                    },
                    "mtu": {
                        "type": "integer",
                        "propertyOrder": 12,
                        "example": 2800,
                        "description": "MTU to set on the client virtual network adapter",
                    },
                    "multicastLimit": {
                        "type": "integer",
                        "propertyOrder": 13,
                        "example": 32,
                        "description": (
                            "Maximum number of recipients per multicast or broadcast. "
                            "Warning - Setting this to 0 will disable IPv4 communication on your network!"
                        ),
                    },
                    "routes": {
                        "type": "array",
                        "propertyOrder": 14,
                        "items": {
                            "type": "object",
                            "properties": {
                                "target": {
                                    "type": "string",
                                    "propertyOrder": 1,
                                    "example": "192.168.192.0/24",
                                    "description": "The target IP address range for the route",
                                },
                                "via": {
                                    "type": "string",
                                    "propertyOrder": 2,
                                    "example": "192.168.192.1",
                                    "description": "The IP address of the next hop for the route",
                                },
                            },
                        },
                        "description": "Array of route objects",
                    },
                    "ipAssignmentPools": {
                        "type": "array",
                        "propertyOrder": 15,
                        "items": {
                            "type": "object",
                            "properties": {
                                "ipRangeStart": {
                                    "type": "string",
                                    "example": "192.168.192.1",
                                    "propertyOrder": 1,
                                    "description": "The starting IP address of the pool range",
                                },
                                "ipRangeEnd": {
                                    "type": "string",
                                    "propertyOrder": 2,
                                    "example": "192.168.192.254",
                                    "description": "The ending IP address of the pool range",
                                },
                            },
                        },
                        "description": "Range of IP addresses for the auto assign pool",
                    },
                    "dns": {
                        "type": "object",
                        "propertyOrder": 16,
                        "properties": {
                            "domain": {
                                "type": "string",
                                "propertyOrder": 1,
                                "example": "zerotier.openwisp.io",
                                "description": "The domain for DNS resolution",
                            },
                            "servers": {
                                "type": "array",
                                "propertyOrder": 2,
                                "items": {
                                    "type": "string",
                                    "example": "10.147.20.3",
                                    "description": "The DNS server IP addresses",
                                },
                            },
                        },
                    },
                    "rules": {
                        "type": "array",
                        "items": {"type": "object"},
                        "propertyOrder": 17,
                        "description": "Array of network rule objects",
                    },
                    "capabilities": {
                        "type": "array",
                        "items": {"type": "object"},
                        "propertyOrder": 18,
                        "description": "Array of network capabilities",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "object"},
                        "propertyOrder": 19,
                        "description": "Array of network tag objects",
                    },
                    "remoteTraceTarget": {
                        "type": "string",
                        "propertyOrder": 20,
                        "example": "7f5d90eb87",
                        "description": "The remote target ID for network tracing",
                    },
                    "remoteTraceLevel": {
                        "type": "integer",
                        "propertyOrder": 21,
                        "description": "The level of network tracing",
                    },
                },
            },
        },
    },
}

schema = deepcopy(base_zerotier_schema)
schema['required'] = ['zerotier']
schema['properties']['files'] = default_schema['properties']['files']
