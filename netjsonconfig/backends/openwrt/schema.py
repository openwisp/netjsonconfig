"""
OpenWrt specific JSON-Schema definition
"""
from netjsonconfig.schema import schema as default_schema

schema = default_schema.copy()

# add timezone to general
schema['properties']['general']['properties'].update({
    "timezone": {
        "id": "timezone",
        "type": "string",
        "default": "UTC"
    }
})

# add driver and protocol
schema['properties']['radios']['items']['properties'].update({
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
})

# mark driver and protocol as required
schema['properties']['radios']['items']['required'] += [
    'driver',
    'protocol'
]
