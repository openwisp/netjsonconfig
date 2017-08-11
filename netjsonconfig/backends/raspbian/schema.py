from copy import deepcopy

from ...schema import schema as default_schema
from ...utils import merge_config
from ..openwrt.timezones import timezones

schema = merge_config(default_schema, {
    "definitions": {
        "ap_wireless_settings": {
            "allOf": [
                {
                    "properties": {
                        "wmm": {
                            "type": "boolean",
                            "title": "WMM (802.11e)",
                            "description": "enables WMM (802.11e) support; "
                                           "required for 802.11n support",
                            "default": True,
                            "format": "checkbox",
                            "propertyOrder": 8,
                        },
                        "isolate": {
                            "type": "boolean",
                            "title": "isolate clients",
                            "description": "isolate wireless clients from one another",
                            "default": False,
                            "format": "checkbox",
                            "propertyOrder": 9,
                        },
                        "macfilter": {
                            "type": "string",
                            "title": "MAC Filter",
                            "description": "specifies the mac filter policy, \"disable\" to disable "
                                           "the filter, \"allow\" to treat it as whitelist or "
                                           "\"deny\" to treat it as blacklist",
                            "enum": [
                                "disable",
                                "accept",
                                "deny",
                            ],
                            "default": "disable",
                            "propertyOrder": 15,
                        },
                        "maclist": {
                            "type": "array",
                            "title": "MAC List",
                            "description": "mac addresses that will be filtered according to the policy "
                                           "specified in the \"macfilter\" option",
                            "propertyOrder": 16,
                            "items": {
                                "type": "string",
                                "title": "MAC address",
                                "pattern": "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
                                "minLength": 17,
                                "maxLength": 17,
                            }
                        }
                    }
                }
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
schema = deepcopy(schema)
del schema['properties']['general']['properties']['ula_prefix']
del schema['properties']['general']['properties']['maintainer']
del schema['properties']['general']['properties']['description']
del schema['properties']['routes']['items']['required'][3]
del schema['properties']['routes']['items']['properties']['cost']
del schema['properties']['routes']['items']['properties']['source']

del schema['definitions']['wireless_interface']['allOf'][0]['properties']['wireless']['oneOf'][4]
del schema['definitions']['wireless_interface']['allOf'][0]['properties']['wireless']['oneOf'][3]
del schema['definitions']['base_wireless_settings']['properties']['ack_distance']
del schema['definitions']['ap_wireless_settings']['allOf'][4]
del schema['definitions']['sta_wireless_settings']['allOf'][4]
del schema['definitions']['base_radio_settings']['properties']['phy']
del schema['definitions']['base_radio_settings']['properties']['tx_power']
