from ...schema import schema as default_schema
from ...utils import merge_config
from ..openwrt.timezones import timezones

schema = merge_config(default_schema, {
    "definitions": {
        "network_interface": {
            "title": "Network interface",
            "allOf": [
                {
                    "properties": {
                        "type": {
                            "enum": [
                                "ethernet",
                                "virtual",
                                "loopback"
                            ],
                        }
                    }
                },
                {"$ref": "#/definitions/interface_settings"}
            ]
        },
        "radio_hwmode_11g": {
            "properties": {
                "hwmode": {
                    "type": "string",
                    "title": "hardware mode",
                    "readOnly": True,
                    "propertyOrder": 8,
                    "default": "11g",
                    "enum": ["11g"],
                }
            }
        },
        "radio_hwmode_11a": {
            "properties": {
                "hwmode": {
                    "type": "string",
                    "title": "hardware mode",
                    "readOnly": True,
                    "propertyOrder": 8,
                    "default": "11a",
                    "enum": ["11a"],
                }
            }
        },
        "radio_80211gn_settings": {
            "allOf": [{"$ref": "#/definitions/radio_hwmode_11g"}]
        },
        "radio_80211an_settings": {
            "allOf": [{"$ref": "#/definitions/radio_hwmode_11a"}]
        },
        "radio_80211ac_2ghz_settings": {
            "allOf": [{"$ref": "#/definitions/radio_hwmode_11g"}]
        },
        "radio_80211ac_5ghz_settings": {
            "allOf": [{"$ref": "#/definitions/radio_hwmode_11a"}]
        },
    },
    "properties": {
        "general": {
            "properties": {
                "timezone": {
                    "enum": list(timezones.keys()),
                    "default": "UTC",
                }
            }
        },
        "ntp": {
            "type": "object",
            "title": "NTP Settings",
            "additionalProperties": True,
            "propertyOrder": 8,
            "properties": {
                "server": {
                    "title": "NTP Servers",
                    "description": "NTP server candidates",
                    "type": "array",
                    "uniqueItems": True,
                    "additionalItems": True,
                    "propertyOrder": 3,
                    "items": {
                        "title": "NTP server",
                        "type": "string",
                        "format": "hostname"
                    },
                }
            }
        }
    }
})

del schema['properties']['general']['properties']['ula_prefix']
del schema['properties']['general']['properties']['description']
del schema['properties']['general']['properties']['maintainer']
del schema['definitions']['base_wireless_settings']['properties']['ack_distance']
