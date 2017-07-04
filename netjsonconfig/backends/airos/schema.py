"""
AirOS specific JSON-Schema definition
"""
from ...schema import schema as default_schema
from ...schema import DEFAULT_FILE_MODE  # noqa - backward compatibility
from ...utils import merge_config

"""
This schema override the possible encryption for AirOS from the default schema
"""
wpasupplicant_schema = {
    "encryption_wireless_property_sta": {
        "properties": {
            "encryption": {
                "type": "object",
                "title": "Encryption",
                "required": "protocol",
                "propertyOrder": 20,
                "oneOf": [
                    {"$ref": "#/definitions/encryption_none"},
                    {"$ref": "#/definitions/encryption_wpa_personal"},
                    {"$ref": "#/definitions/encryption_wpa_enterprise_sta"},
                ],
            },
        },
    },
    "encryption_wireless_property_ap": {
        "properties": {
            "encryption": {
                "type": "object",
                "title": "Encryption",
                "required": "protocol",
                "propertyOrder": 20,
                "oneOf": [
                    {"$ref": "#/definitions/encryption_none"},
                    {"$ref": "#/definitions/encryption_wpa_personal"},
                    {"$ref": "#/definitions/encryption_wpa_enterprise_sta"},
                ],
            },
        },
    },
}



schema = merge_config(default_schema, wpasupplicant_schema)
