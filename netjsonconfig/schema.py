"""
JSON-Schema implementation of NetJSON DeviceConfiguration
http://netjson.org/rfc.html
"""

from .channels import channels_2and5, channels_2ghz, channels_5ghz
from .countries import countries

DEFAULT_FILE_MODE = '0644'

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "additionalProperties": True,
    "definitions": {
        "base_address": {
            "type": "object",
            "additionalProperties": True,
            "required": [
                "proto",
                "family",
            ],
            "properties": {
                "proto": {
                    "title": "protocol",
                    "type": "string",
                    "propertyOrder": 1,
                },
                "family": {
                    "type": "string",
                    "propertyOrder": 2,
                }
            }
        },
        "static_address": {
            "required": [
                "address",
                "mask"
            ],
            "properties": {
                "address": {
                    "type": "string",
                    "propertyOrder": 3,
                },
                "mask": {
                    "type": "integer",
                    "propertyOrder": 4,
                },
                "gateway": {
                    "type": "string",
                    "propertyOrder": 5,
                }
            }
        },
        "ipv4_address": {
            "title": "ipv4",
            "allOf": [
                {"$ref": "#/definitions/base_address"},
                {"$ref": "#/definitions/static_address"},
                {
                    "type": "object",
                    "properties": {
                        "proto": {"enum": ["static"]},
                        "family": {"enum": ["ipv4"]},
                        "address": {
                            "title": "ipv4 address",
                            "minLength": 7,
                            "maxLength": 15,
                            "format": "ipv4",
                        },
                        "mask": {
                            "minimum": 8,
                            "maxmium": 32,
                            "default": 24,
                        },
                        "gateway": {
                            "title": "ipv4 gateway",
                            "description": "optional ipv4 gateway",
                            "maxLength": 16,
                        }
                    }
                }
            ]
        },
        "ipv6_address": {
            "title": "ipv6",
            "allOf": [
                {"$ref": "#/definitions/base_address"},
                {"$ref": "#/definitions/static_address"},
                {
                    "type": "object",
                    "required": [
                        "address",
                        "mask"
                    ],
                    "properties": {
                        "proto": {"enum": ["static"]},
                        "family": {"enum": ["ipv6"]},
                        "address": {
                            "title": "ipv6 address",
                            "minLength": 3,
                            "maxLength": 45,
                            "format": "ipv6",
                            "propertyOrder": 3,
                        },
                        "mask": {
                            "minimum": 4,
                            "maxmium": 128,
                            "default": 64,
                        },
                        "gateway": {
                            "title": "ipv6 gateway",
                            "description": "optional ipv6 gateway",
                            "maxLength": 45,
                        }
                    }
                }
            ]
        },
        "dhcp_address": {
            "title": "DHCP",
            "allOf": [
                {"$ref": "#/definitions/base_address"},
                {
                    "type": "object",
                    "properties": {
                        "proto": {"enum": ["dhcp"]},
                        "family": {"enum": ["ipv4", "ipv6"]}
                    }
                }
            ]
        },
        "interface_settings": {
            "type": "object",
            "title": "Interface settings",
            "additionalProperties": True,
            "required": [
                "name",
                "type"
            ],
            "properties": {
                "name": {
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 15,
                    "pattern": "^[^\\s]*$",
                    "propertyOrder": 0,
                },
                "mtu": {
                    "type": "integer",
                    "title": "MTU",
                    "default": 1500,
                    "minimum": 68,
                    "propertyOrder": 2,
                },
                "mac": {
                    "type": "string",
                    "title": "MAC address",
                    "description": "if specified overrides default macaddress for this interface",
                    "pattern": "^(([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})|)$",  # can be empty
                    "maxLength": 17,
                    "propertyOrder": 3,
                },
                "autostart": {
                    "type": "boolean",
                    "title": "auto start",
                    "description": "bring up interface on boot",
                    "default": True,
                    "format": "checkbox",
                    "propertyOrder": 5,
                },
                "disabled": {
                    "type": "boolean",
                    "description": "disable this interface without deleting its configuration",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 6,
                },
                "addresses": {
                    "type": "array",
                    "title": "Addresses",
                    "uniqueItems": True,
                    "additionalItems": True,
                    "propertyOrder": 20,
                    "items": {
                        "title": "Address",
                        "oneOf": [
                            {"$ref": "#/definitions/dhcp_address"},
                            {"$ref": "#/definitions/ipv4_address"},
                            {"$ref": "#/definitions/ipv6_address"},
                        ]
                    }
                }
            }
        },
        "network_interface": {
            "title": "Network interface",
            "allOf": [
                {
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": [
                                "ethernet",
                                "virtual",
                                "loopback",
                                "other"
                            ],
                            "propertyOrder": 1,
                        }
                    }
                },
                {"$ref": "#/definitions/interface_settings"}
            ]
        },
        "wireless_interface": {
            "title": "Wireless interface",
            "allOf": [
                {
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["wireless"],
                            "default": "wireless",
                            "propertyOrder": 1,
                        },
                        "wireless": {
                            "type": "object",
                            "propertyOrder": 10,
                            "oneOf": [
                                {"$ref": "#/definitions/ap_wireless_settings"},
                                {"$ref": "#/definitions/sta_wireless_settings"},
                                {"$ref": "#/definitions/adhoc_wireless_settings"},
                                {"$ref": "#/definitions/monitor_wireless_settings"},
                                {"$ref": "#/definitions/mesh_wireless_settings"},
                            ]
                        }
                    }
                },
                {"$ref": "#/definitions/interface_settings"},
            ]
        },
        "bridge_interface": {
            "title": "Bridge interface",
            "required": [
                "bridge_members"
            ],
            "allOf": [
                {
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["bridge"],
                            "propertyOrder": 1
                        },
                        "stp": {
                            "type": "boolean",
                            "title": "STP enabled",
                            "description": "enables the spanning tree protocol",
                            "default": False,
                            "format": "checkbox",
                            "propertyOrder": 4,
                        },
                        "bridge_members": {
                            "type": "array",
                            "title": "Bridge Members",
                            "uniqueItems": True,
                            "propertyOrder": 8,
                            "items": {
                                "title": "bridged interface",
                                "type": "string",
                                "$ref": "#/definitions/interface_settings/properties/name"
                            }
                        }
                    }
                },
                {"$ref": "#/definitions/interface_settings"},
            ]
        },
        "base_wireless_settings": {
            "type": "object",
            "title": "Wireless Settings",
            "additionalProperties": True,
            "propertyOrder": 8,
            "required": [
                "radio",
                "mode",
            ],
            "properties": {
                "mode": {
                    "type": "string",
                    "propertyOrder": 1,
                },
                "radio": {
                    "type": "string",
                    "description": "reference to one of the elements defined in the \"radios\" section",
                    "minLength": 2,
                    "propertyOrder": 2,
                },
                "ack_distance": {
                    "type": "integer",
                    "title": "ACK distance",
                    "description": "distance to farthest network member in meters, "
                                   "if set to 0 this setting will be ignored",
                    "minimum": 0,
                    "propertyOrder": 10,
                },
                "rts_threshold": {
                    "type": "integer",
                    "title": "RTS threshold",
                    "description": "override RTS/CTS threshold, "
                                   "if set to 0 this setting won't be overridden",
                    "minimum": 0,
                    "maximum": 2346,
                    "propertyOrder": 11,
                },
                "frag_threshold": {
                    "type": "integer",
                    "title": "fragmentation threshold",
                    "description": "override default fragmentation threshold, "
                                   "if set to 0 this setting won't be overridden",
                    "minimum": 0,
                    "maximum": 2346,
                    "propertyOrder": 12,
                }
            }
        },
        "ssid_wireless_property": {
            "required": ["ssid"],
            "properties": {
                "ssid": {
                    "type": "string",
                    "title": "SSID",
                    "maxLength": 32,
                    "propertyOrder": 3,
                }
            }
        },
        "hidden_wireless_property": {
            "properties": {
                "hidden": {
                    "type": "boolean",
                    "title": "hide SSID",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 4,
                }
            }
        },
        "bssid_wireless_property": {
            "required": ["bssid"],
            "properties": {
                "bssid": {
                    "type": "string",
                    "title": "BSSID",
                    "pattern": "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
                    "minLength": 17,
                    "maxLength": 17,
                    "propertyOrder": 4,
                },
            }
        },
        "wds_wireless_property": {
            "properties": {
                "wds": {
                    "title": "WDS",
                    "description": "enable wireless distribution system",
                    "type": "boolean",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 5,
                }
            }
        },
        "mesh_id_wireless_property": {
            "required": ["mesh_id"],
            "properties": {
                "mesh_id": {
                    "type": "string",
                    "title": "mesh ID",
                    "description": "802.11 mesh ID: if set, the wireless interface "
                                   "will join this mesh network",
                    "pattern": "^[^\\s]*$",
                    "propertyOrder": 3,
                },
            }
        },
        "encryption_wireless_property_ap": {
            "properties": {
                "encryption": {
                    "type": "object",
                    "title": "Encryption",
                    "required": ["protocol"],
                    "propertyOrder": 20,
                    "oneOf": [
                        {"$ref": "#/definitions/encryption_none"},
                        {"$ref": "#/definitions/encryption_wpa_personal"},
                        {"$ref": "#/definitions/encryption_wpa_enterprise_ap"},
                        {"$ref": "#/definitions/encryption_wps"},
                        {"$ref": "#/definitions/encryption_wep"},
                    ]
                }
            }
        },
        "encryption_wireless_property_sta": {
            "properties": {
                "encryption": {
                    "type": "object",
                    "title": "Encryption",
                    "required": ["protocol"],
                    "propertyOrder": 20,
                    "oneOf": [
                        {"$ref": "#/definitions/encryption_none"},
                        {"$ref": "#/definitions/encryption_wpa_personal"},
                        {"$ref": "#/definitions/encryption_wpa_enterprise_sta"},
                        {"$ref": "#/definitions/encryption_wep"},
                    ]
                }
            }
        },
        "encryption_wireless_property_mesh": {
            "properties": {
                "encryption": {
                    "type": "object",
                    "title": "Encryption",
                    "required": ["protocol"],
                    "propertyOrder": 20,
                    "oneOf": [
                        {"$ref": "#/definitions/encryption_none"},
                        {"$ref": "#/definitions/encryption_wpa_personal"},
                        {"$ref": "#/definitions/encryption_wep"},
                    ]
                }
            }
        },
        "encryption_none": {
            "title": "No encryption",
            "properties": {
                "protocol": {
                    "type": "string",
                    "title": "encryption protocol",
                    "enum": ["none"],
                    "options": {"enum_titles": ["No encryption"]}
                }
            }
        },
        "encryption_base_settings": {
            "required": ["key"],
            "additionalProperties": True,
            "properties": {
                "protocol": {
                    "type": "string",
                    "title": "encryption protocol",
                    "propertyOrder": 1,
                },
                "key": {
                    "type": "string",
                    "propertyOrder": 2,
                },
                "disabled": {
                    "type": "boolean",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 20,
                },
            }
        },
        "encryption_cipher_property": {
            "properties": {
                "cipher": {
                    "type": "string",
                    "enum": [
                        "auto",
                        "ccmp",
                        "tkip",
                        "tkip+ccmp"
                    ],
                    "options": {
                        "enum_titles": [
                            "auto",
                            "Force CCMP (AES)",
                            "Force TKIP",
                            "FORCE TKIP and CCMP (AES)"
                        ]
                    },
                    "propertyOrder": 3
                }
            }
        },
        "encryption_wpa_personal": {
            "title": "WPA2/WPA Personal",
            "allOf": [
                {"$ref": "#/definitions/encryption_base_settings"},
                {"$ref": "#/definitions/encryption_cipher_property"},
                {
                    "properties": {
                        "protocol": {
                            "enum": [
                                "wpa2_personal",
                                "wpa_personal_mixed",
                                "wpa_personal",
                            ],
                            "options": {
                                "enum_titles": [
                                    "WPA2 Personal",
                                    "WPA Personal Mixed Mode",
                                    "WPA Personal",
                                ]
                            }
                        },
                        "key": {
                            "minLength": 8
                        }
                    }
                }
            ]
        },
        "encryption_wpa_enterprise_base_settings": {
            "properties": {
                "protocol": {
                    "type": "string",
                    "title": "encryption protocol",
                    "enum": [
                        "wpa2_enterprise",
                        "wpa_enterprise_mixed",
                        "wpa_enterprise",
                    ],
                    "options": {
                        "enum_titles": [
                            "WPA2 Enterprise",
                            "WPA Enterprise Mixed Mode",
                            "WPA Enterprise",
                        ]
                    },
                    "propertyOrder": 1
                }
            }
        },
        "encryption_wpa_enterprise_ap": {
            "title": "WPA2/WPA Enterprise (access point)",
            "allOf": [
                {"$ref": "#/definitions/encryption_base_settings"},
                {"$ref": "#/definitions/encryption_cipher_property"},
                {"$ref": "#/definitions/encryption_wpa_enterprise_base_settings"},
                {
                    "required": ["server"],
                    "properties": {
                        "server": {
                            "type": "string",
                            "minLength": 3,
                            "title": "radius server",
                            "propertyOrder": 4,
                        },
                        "key": {
                            "title": "shared secret",
                            "minLength": 4,
                            "propertyOrder": 5,
                        },
                        "port": {
                            "type": "integer",
                            "title": "radius port",
                            "default": 1812,
                            "propertyOrder": 6,
                        },
                        "acct_server": {
                            "type": "string",
                            "title": "accounting server",
                            "propertyOrder": 7,
                        },
                        "acct_server_port": {
                            "type": "integer",
                            "title": "accounting port",
                            "default": 1813,
                            "propertyOrder": 8,
                        },
                    }
                }
            ]
        },
        "encryption_wpa_enterprise_sta": {
            "title": "WPA2/WPA Enterprise (client)",
            "additionalProperties": True,
            "allOf": [
                {"$ref": "#/definitions/encryption_cipher_property"},
                {"$ref": "#/definitions/encryption_wpa_enterprise_base_settings"},
                {
                    "properties": {
                        "eap_type": {
                            "title": "EAP protocol",
                            "type": "string",
                            "enum": ["tls", "ttls"],
                            "options": {"enum_titles": ["EAP-TLS", "EAP-PEAP"]},
                            "propertyOrder": 4,
                        },
                        "identity": {
                            "type": "string",
                            "propertyOrder": 5,
                        },
                        "password": {
                            "type": "string",
                            "propertyOrder": 6,
                        },
                        "ca_cert": {
                            "type": "string",
                            "title": "CA certificate (path)",
                            "propertyOrder": 7,
                        },
                        "client_cert": {
                            "type": "string",
                            "title": "client certificate (path)",
                            "propertyOrder": 8,
                        },
                        "priv_key": {
                            "type": "string",
                            "title": "private key (path)",
                            "propertyOrder": 9,
                        },
                        "priv_key_pwd": {
                            "type": "string",
                            "title": "private key password",
                            "propertyOrder": 10,
                        }
                    }
                }
            ]
        },
        "encryption_wep": {
            "title": "WEP (Open System/Shared Key)",
            "description": "WEP encryption is insecure and its use is discouraged.",
            "allOf": [
                {"$ref": "#/definitions/encryption_base_settings"},
                {
                    "properties": {
                        "protocol": {
                            "enum": [
                                "wep_open",
                                "wep_shared"
                            ],
                            "options": {
                                "enum_titles": [
                                    "WEP Open System",
                                    "WEP Shared Key"
                                ]
                            }
                        },
                        "key": {
                            "minLength": 5,
                            "maxLength": 26
                        }
                    }
                }
            ]
        },
        "encryption_wps": {
            "title": "WPS (Wireless Protected Setup)",
            "additionalProperties": True,
            "properties": {
                "protocol": {
                    "type": "string",
                    "title": "encryption protocol",
                    "enum": ["wps"],
                    "options": {"enum_titles": ["WPS"]},
                    "propertyOrder": 1,
                },
                "wps_pushbutton": {
                    "type": "boolean",
                    "title": "push button mode",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 2,
                },
                "wps_label": {
                    "type": "boolean",
                    "title": "label mode",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 3,
                },
                "wps_pin": {
                    "type": "string",
                    "title": "PIN",
                    "propertyOrder": 4,
                }
            }
        },
        "ap_wireless_settings": {
            "title": "Access Point",
            "allOf": [
                {
                    "properties": {
                        "mode": {
                            "enum": ["access_point"],
                            "options": {"enum_titles": ["access point"]}
                        }
                    }
                },
                {"$ref": "#/definitions/base_wireless_settings"},
                {"$ref": "#/definitions/ssid_wireless_property"},
                {"$ref": "#/definitions/hidden_wireless_property"},
                {"$ref": "#/definitions/wds_wireless_property"},
                {"$ref": "#/definitions/encryption_wireless_property_ap"},
            ]
        },
        "sta_wireless_settings": {
            "title": "Station",
            "allOf": [
                {"properties": {"mode": {"enum": ["station"]}}},
                {"$ref": "#/definitions/base_wireless_settings"},
                {"$ref": "#/definitions/ssid_wireless_property"},
                {"$ref": "#/definitions/bssid_wireless_property"},
                {"$ref": "#/definitions/wds_wireless_property"},
                {"$ref": "#/definitions/encryption_wireless_property_sta"},
            ]
        },
        "adhoc_wireless_settings": {
            "title": "Adhoc",
            "allOf": [
                {"properties": {"mode": {"enum": ["adhoc"]}}},
                {"$ref": "#/definitions/base_wireless_settings"},
                {"$ref": "#/definitions/ssid_wireless_property"},
                {"$ref": "#/definitions/bssid_wireless_property"},
                {"$ref": "#/definitions/encryption_wireless_property_mesh"},
            ]
        },
        "monitor_wireless_settings": {
            "title": "Monitor",
            "allOf": [
                {"properties": {"mode": {"enum": ["monitor"]}}},
                {"$ref": "#/definitions/base_wireless_settings"},
            ]
        },
        "mesh_wireless_settings": {
            "title": "802.11s (mesh)",
            "allOf": [
                {
                    "properties": {
                        "mode": {
                            "enum": ["802.11s"],
                            "options": {"enum_titles": ["802.11s (mesh)"]}
                        }
                    }
                },
                {"$ref": "#/definitions/base_wireless_settings"},
                {"$ref": "#/definitions/mesh_id_wireless_property"},
                {"$ref": "#/definitions/encryption_wireless_property_mesh"},
            ]
        },
        "base_radio_settings": {
            "type": "object",
            "additionalProperties": True,
            "required": [
                "protocol",
                "name",
                "channel",
                "channel_width",
            ],
            "properties": {
                "name": {
                    "type": "string",
                    "propertyOrder": 1,
                    "minLength": 3
                },
                "protocol": {
                    "type": "string",
                    "propertyOrder": 2,
                },
                "phy": {
                    "type": "string",
                    "propertyOrder": 3,
                },
                "channel": {
                    "type": "integer",
                    "propertyOrder": 4,
                },
                "channel_width": {
                    "type": "integer",
                    "title": "channel width (mhz)",
                    "propertyOrder": 5,
                },
                "tx_power": {
                    "type": "integer",
                    "title": "transmit power (dbm)",
                    "propertyOrder": 6,
                },
                "country": {
                    "type": "string",
                    "maxLength": 2,
                    "default": "00",
                    "enum": list(countries.values()),
                    "options": {"enum_titles": list(countries.keys())},
                    "propertyOrder": 7,
                },
                "disabled": {
                    "type": "boolean",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 9,
                }
            }
        },
        "radio_2ghz_channels": {
            "properties": {
                "channel": {
                    "enum": channels_2ghz,
                    "options": {"enum_titles": ['auto']}
                }
            }
        },
        "radio_5ghz_channels": {
            "properties": {
                "channel": {
                    "enum": channels_5ghz,
                    "options": {"enum_titles": ['auto']}
                }
            }
        },
        "radio_2and5_channels": {
            "properties": {
                "channel": {
                    "enum": channels_2and5,
                    "options": {"enum_titles": ['auto']}
                }
            }
        },
        "radio_legacy_channel_width": {
            "properties": {"channel_width": {"enum": [20]}}
        },
        "radio_n_channel_width": {
            "properties": {"channel_width": {"enum": [20, 40]}}
        },
        "radio_ac_channel_width": {
            "properties": {"channel_width": {"enum": [20, 40, 80, 160]}}
        },
        "radio_80211bg_settings": {
            "title": "802.11b/g (2.4 GHz legacy)",
            "allOf": [
                {"properties": {"protocol": {"enum": ["802.11b", "802.11g"]}}},
                {"$ref": "#/definitions/base_radio_settings"},
                {"$ref": "#/definitions/radio_2ghz_channels"},
                {"$ref": "#/definitions/radio_legacy_channel_width"}
            ]
        },
        "radio_80211a_settings": {
            "title": "802.11a (5 GHz legacy)",
            "allOf": [
                {"properties": {"protocol": {"enum": ["802.11a"]}}},
                {"$ref": "#/definitions/base_radio_settings"},
                {"$ref": "#/definitions/radio_5ghz_channels"},
                {"$ref": "#/definitions/radio_legacy_channel_width"}
            ]
        },
        "radio_80211gn_settings": {
            "title": "802.11n (2.4 GHz N)",
            "allOf": [
                {"properties": {"protocol": {"enum": ["802.11n"]}}},
                {"$ref": "#/definitions/base_radio_settings"},
                {"$ref": "#/definitions/radio_2ghz_channels"},
                {"$ref": "#/definitions/radio_n_channel_width"},
            ]
        },
        "radio_80211an_settings": {
            "title": "802.11n (5 GHz N)",
            "allOf": [
                {"properties": {"protocol": {"enum": ["802.11n"]}}},
                {"$ref": "#/definitions/base_radio_settings"},
                {"$ref": "#/definitions/radio_5ghz_channels"},
                {"$ref": "#/definitions/radio_n_channel_width"},
            ]
        },
        "radio_80211ac_2ghz_settings": {
            "title": "802.11ac (2.4 GHz AC)",
            "allOf": [
                {"properties": {"protocol": {"enum": ["802.11ac"]}}},
                {"$ref": "#/definitions/base_radio_settings"},
                {"$ref": "#/definitions/radio_2ghz_channels"},
                {"$ref": "#/definitions/radio_ac_channel_width"},
            ]
        },
        "radio_80211ac_5ghz_settings": {
            "title": "802.11ac (5 GHz AC)",
            "allOf": [
                {"properties": {"protocol": {"enum": ["802.11ac"]}}},
                {"$ref": "#/definitions/base_radio_settings"},
                {"$ref": "#/definitions/radio_5ghz_channels"},
                {"$ref": "#/definitions/radio_ac_channel_width"},
            ]
        },
    },
    "properties": {
        "general": {
            "type": "object",
            "title": "General",
            "additionalProperties": True,
            "propertyOrder": 1,
            "properties": {
                "hostname": {
                    "type": "string",
                    "maxLength": 63,
                    "minLength": 1,
                    "format": "hostname",
                    "propertyOrder": 1,
                },
                "ula_prefix": {
                    "type": "string",
                    "title": "ULA prefix",
                    "description": "IPv6 Unique Local Address prefix",
                    "propertyOrder": 2,
                },
                "maintainer": {
                    "type": "string",
                    "propertyOrder": 3,
                },
                "description": {
                    "type": "string",
                    "description": "description and notes",
                    "propertyOrder": 4,
                }
            }
        },
        "interfaces": {
            "type": "array",
            "title": "Interfaces",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 2,
            "items": {
                "title": "Interface",
                "oneOf": [
                    {"$ref": "#/definitions/network_interface"},
                    {"$ref": "#/definitions/wireless_interface"},
                    {"$ref": "#/definitions/bridge_interface"}
                ]
            }
        },
        "radios": {
            "type": "array",
            "title": "Radios",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 3,
            "items": {
                "title": "Radio",
                "oneOf": [
                    {"$ref": "#/definitions/radio_80211gn_settings"},
                    {"$ref": "#/definitions/radio_80211an_settings"},
                    {"$ref": "#/definitions/radio_80211ac_2ghz_settings"},
                    {"$ref": "#/definitions/radio_80211ac_5ghz_settings"},
                    {"$ref": "#/definitions/radio_80211bg_settings"},
                    {"$ref": "#/definitions/radio_80211a_settings"},
                ]
            }
        },
        "dns_servers": {
            "title": "DNS Configuration",
            "type": "array",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 4,
            "items": {
                "title": "DNS Server",
                "type": "string"
            }
        },
        "dns_search": {
            "title": "DNS Search Domains",
            "type": "array",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 5,
            "items": {
                "title": "Domain",
                "type": "string",
                "format": "hostname"
            }
        },
        "routes": {
            "type": "array",
            "title": "Static routes",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 6,
            "items": {
                "type": "object",
                "title": "Route",
                "additionalProperties": True,
                "required": [
                    "device",
                    "destination",
                    "next",
                    "cost"
                ],
                "properties": {
                    "device": {
                        "type": "string",
                        "description": "interface name of the to which the static route should apply",
                        "propertyOrder": 1,
                    },
                    "destination": {
                        "type": "string",
                        "propertyOrder": 2,
                    },
                    "next": {
                        "title": "next hop",
                        "type": "string",
                        "propertyOrder": 2,
                    },
                    "cost": {
                        "type": "integer",
                        "propertyOrder": 4,
                        "default": 0,
                    },
                    "source": {
                        "type": "string",
                        "description": "the preferred source address when sending to destinations "
                                       "covered by the target (optional)",
                        "propertyOrder": 5,
                    }
                }
            }
        },
        "files": {
            "type": "array",
            "title": "Files",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 20,
            "items": {
                "type": "object",
                "title": "File",
                "additionalProperties": False,
                "required": [
                    "path",
                    "mode",
                    "contents"
                ],
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "filesystem path",
                        "propertyOrder": 1,
                    },
                    "mode": {
                        "type": "string",
                        "description": "filesystem permissions",
                        "maxLength": 4,
                        "minLength": 3,
                        "pattern": "^[0-7]*$",
                        "default": DEFAULT_FILE_MODE,
                        "propertyOrder": 2,
                    },
                    "contents": {
                        "type": "string",
                        "description": "content (plain-text only)",
                        "format": "textarea",
                        "propertyOrder": 3,
                    },
                }
            }
        }
    }
}
