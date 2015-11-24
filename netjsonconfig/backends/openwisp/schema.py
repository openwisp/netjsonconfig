"""
OpenWisp specific JSON-Schema definition
(extends OpenWrt JSON-Schema)
"""
from ..openwrt.schema import schema as openwrt_schema
from ...utils import merge_config

schema = merge_config(openwrt_schema, {
    "properties": {
        "general": {
            "required": ["hostname"]
        },
        # added mainly for backward compatibility with OpenWISP Manager
        "tc_options": {
            "type": "array",
            "title": "Traffic Control Options",
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
                        "type": "string"
                    },
                    "input_bandwidth": {
                        "title": "Input bandwidth (kbps)",
                        "type": "integer"
                    },
                    "output_bandwidth": {
                        "title": "Output bandwidth (kbps)",
                        "type": "integer"
                    }
                }
            }
        }
    }
})
