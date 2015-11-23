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
        }
    }
})
