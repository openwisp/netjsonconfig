from copy import deepcopy

from ..wireguard.schema import schema as base_schema

base_vxlan_properties = {
    "vxlan": {
        "type": "array",
        "title": "VXLAN",
        "uniqueItems": True,
        "additionalItems": True,
        "propertyOrder": 13,
        "items": {
            "type": "object",
            "title": "VXLAN tunnel",
            "additionalProperties": True,
            "properties": {
                "name": {
                    "title": "interface name",
                    "description": "VXLAN interface name",
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 15,
                    "pattern": "^[^\\s]*$",
                    "propertyOrder": 1,
                },
                "vni": {
                    "type": "integer",
                    "title": "VNI",
                    "description": (
                        "VXLAN Network Identifier, if set to \"0\", each tunnel will have"
                        " different VNI. If a non-zero VNI is specified, then it will be"
                        " used for all VXLAN tunnels."
                    ),
                    "propertyOrder": 2,
                    "default": 0,
                    "minimum": 0,
                    "maximum": 16777216,
                },
            },
        },
    }
}


schema = deepcopy(base_schema)
schema['properties'].update(base_vxlan_properties)
