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
                "required": ["name"],
                "properties": {
                    # Read-only properties
                    "id": {
                        "type": "string",
                        "readOnly": True,
                        "example": "3e245e31af000001",
                        "description": "Network ID",
                    },
                    "nwid": {
                        "type": "string",
                        "readOnly": True,
                        "example": "3e245e31af000001",
                        "description": "Network ID legacy field (same as 'id')",
                    },
                    "objtype": {
                        "type": "string",
                        "readOnly": True,
                        "example": "network",
                    },
                    "revision": {
                        "type": "integer",
                        "example": 1,
                        "readOnly": True,
                        "description": "The revision number of the network configuration",
                    },
                    "creationTime": {
                        "type": "number",
                        "readOnly": True,
                        "example": 1623101592,
                        "description": "Time the network was created",
                    },
                    # Configurable properties
                    "name": {
                        "type": "string",
                        "example": "openwisp-wifi-network",
                        "description": "Name of the network",
                    },
                    "private": {
                        "type": "boolean",
                        "description": (
                            "Whether or not the network is private."
                            "If false, members will *NOT* need to be authorized to join."
                        ),
                    },
                    "enableBroadcast": {
                        "type": "boolean",
                        "description": "Enable broadcast packets on the network",
                    },
                    "v4AssignMode": {
                        "type": "object",
                        "properties": {
                            "zt": {"type": "boolean"},
                            "description": "Whether ZeroTier should assign IPv4 addresses to members",
                        },
                    },
                    "v6AssignMode": {
                        "type": "object",
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
                        "example": 2800,
                        "description": "MTU to set on the client virtual network adapter",
                    },
                    "multicastLimit": {
                        "type": "integer",
                        "example": 32,
                        "description": (
                            "Maximum number of recipients per multicast or broadcast."
                            "Warning - Setting this to 0 will disable IPv4 communication on your network!"
                        ),
                    },
                    "routes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "target": {
                                    "type": "string",
                                    "example": "192.168.192.0/24",
                                    "description": "The target IP address range for the route",
                                },
                                "via": {
                                    "type": "string",
                                    "example": "192.168.192.1",
                                    "description": "The IP address of the next hop for the route",
                                },
                            },
                        },
                        "description": "Array of route objects",
                    },
                    "ipAssignmentPools": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "ipRangeStart": {
                                    "type": "string",
                                    "example": "192.168.192.1",
                                    "description": "The starting IP address of the pool range",
                                },
                                "ipRangeEnd": {
                                    "type": "string",
                                    "example": "192.168.192.254",
                                    "description": "The ending IP address of the pool range",
                                },
                            },
                        },
                        "description": "Range of IP addresses for the auto assign pool",
                    },
                    "dns": {
                        "type": "object",
                        "properties": {
                            "domain": {
                                "type": "string",
                                "example": "zerotier.openwisp.io",
                                "description": "The domain for DNS resolution",
                            },
                            "servers": {
                                "type": "array",
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
                        "description": "Array of network rule objects",
                    },
                    "capabilities": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "Array of network capabilities",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "Array of network tag objects",
                    },
                    "remoteTraceTarget": {
                        "type": "string",
                        "example": "7f5d90eb87",
                        "description": "The remote target ID for network tracing",
                    },
                    "remoteTraceLevel": {
                        "type": "integer",
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
