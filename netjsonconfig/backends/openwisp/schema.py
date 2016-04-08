"""
OpenWisp specific JSON-Schema definition
(extends OpenWrt JSON-Schema)
"""
from ...utils import merge_config
from ..openwrt.schema import schema as openwrt_schema

schema = merge_config(openwrt_schema, {
    "properties": {
        "general": {
            "required": ["hostname"]
        },
        # added mainly for backward compatibility with OpenWISP Manager
        "tc_options": {
            "type": "array",
            "title": "Traffic Control",
            "additionalItems": True,
            "items": {
                "type": "object",
                "title": "Interface",
                "additionalProperties": False,
                "required": [
                    "name"
                ],
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "interface name",
                        "propertyOrder": 1,
                    },
                    "input_bandwidth": {
                        "title": "input bandwidth (kbps)",
                        "type": "integer",
                        "propertyOrder": 2,
                    },
                    "output_bandwidth": {
                        "title": "output bandwidth (kbps)",
                        "type": "integer",
                        "propertyOrder": 3,
                    }
                }
            }
        }
    }
})
