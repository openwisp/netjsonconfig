"""
OpenWrt specific JSON-Schema definition
"""
from netjsonconfig.schema import schema as default_schema

schema = default_schema.copy()
schema['properties']['general']['properties'].update({
    "timezone": {
        "id": "timezone",
        "type": "string",
        "default": "UTC"
    }
})
