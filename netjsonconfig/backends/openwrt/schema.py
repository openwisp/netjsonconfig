"""
OpenWrt specific JSON-Schema definition
"""
from .timezones import timezones
from ...schema import schema as default_schema
from ...utils import merge_dict

schema = merge_dict(default_schema, {
    "properties": {
        "general": {
            "properties": {
                "timezone": {
                    "id": "timezone",
                    "type": "string",
                    "default": "Coordinated Universal Time",
                    "enum": list(timezones.keys())
                }
            }
        },
        "radios": {
            "items": {
                "properties": {
                    "driver": {
                        "id": "driver",
                        "type": "string",
                        "enum": [
                            "mac80211",
                            "ath5k",
                            "ath9k",
                            "broadcom"
                        ]
                    },
                    "protocol": {
                        "id": "protocol",
                        "type": "string",
                        "enum": [
                            "802.11a",
                            "802.11b",
                            "802.11g",
                            "802.11n",
                            "802.11ac"
                        ]
                    }
                }
            }
        }
    }
})

# add interface protos
schema['properties']['interfaces']['items']['properties']\
      ['addresses']['items']['properties']['proto']['enum'] += [
    'dhcpv6',
    'ppp',
    'pppoe',
    'pppoa',
    '3g',
    'qmi',
    'ncm',
    'hnet',
    'pptp',
    '6in4',
    'aiccu',
    '6to4',
    '6rd',
    'dslite',
    'l2tp',
    'relay',
    'gre',
    'gretap',
    'grev6',
    'grev6tap'
]

# mark driver and protocol as required
schema['properties']['radios']['items']['required'] += [
    'driver',
    'protocol'
]
