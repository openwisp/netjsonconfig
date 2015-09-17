schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "id": "/",
    "type": "object",
    "additionalProperties": True,
    "required": [
        "type"
    ],
    "properties": {
        "type": {
            "id": "type",
            "type": "string",
            "default": "DeviceConfiguration",
            "pattern": "DeviceConfiguration"
        },
        "general": {
            "id": "general",
            "type": "object",
            "title": "General",
            "additionalProperties": True,
            "properties": {
                "hostname": {
                    "id": "hostname",
                    "type": "string"
                },
                "maintainer": {
                    "id": "maintainer",
                    "type": "string"
                },
                "description": {
                    "id": "description",
                    "type": "string"
                },
                "timezone": {
                    "id": "timezone",
                    "type": "string",
                    "default": "UTC"
                }
            }
        },
        "hardware": {
            "id": "hardware",
            "type": "object",
            "title": "Hardware",
            "additionalProperties": True,
            "properties": {
                "manufacturer": {
                    "id": "manufacturer",
                    "type": "string"
                },
                "model": {
                    "id": "model",
                    "type": "string"
                },
                "revision": {
                    "id": "revision",
                    "type": "number"
                },
                "cpu": {
                    "id": "cpu",
                    "type": "string"
                }
            }
        },
        "operating_system": {
            "id": "operating_system",
            "type": "object",
            "title": "Operating System",
            "additionalProperties": True,
            "properties": {
                "name": {
                    "id": "name",
                    "type": "string"
                },
                "kernel": {
                    "id": "kernel",
                    "type": "string"
                },
                "version": {
                    "id": "version",
                    "type": "string"
                },
                "revision": {
                    "id": "revision",
                    "type": "string"
                },
                "description": {
                    "id": "description",
                    "type": "string"
                }
            }
        },
        "resources": {
            "id": "resources",
            "type": "object",
            "title": "Resources",
            "additionalProperties": True,
            "properties": {
                "memory": {
                    "id": "memory",
                    "type": "object",
                    "additionalProperties": True,
                    "properties": {
                        "total": {
                            "id": "total",
                            "type": "number"
                        }
                    }
                },
                "swap": {
                    "id": "swap",
                    "type": "object",
                    "additionalProperties": True,
                    "properties": {
                        "total": {
                            "id": "total",
                            "type": "number"
                        }
                    }
                },
                "cpu": {
                    "id": "cpu",
                    "type": "object",
                    "additionalProperties": True,
                    "properties": {
                        "frequency": {
                            "id": "frequency",
                            "type": "number"
                        }
                    }
                },
                "flash": {
                    "id": "flash",
                    "type": "object",
                    "additionalProperties": True,
                    "properties": {
                        "total": {
                            "id": "total",
                            "type": "number"
                        }
                    }
                },
                "storage": {
                    "id": "storage",
                    "type": "object",
                    "additionalProperties": True,
                    "properties": {
                        "total": {
                            "id": "total",
                            "type": "number"
                        }
                    }
                }
            }
        },
        "radios": {
            "id": "radios",
            "type": "array",
            "title": "Radios",
            "uniqueItems": True,
            "additionalItems": True,
            "items": {
                "type": "object",
                "title": "Radio",
                "additionalProperties": True,
                "required": [
                    "name",
                    "channel",
                    "channel_width",
                    "tx_power"
                ],
                "properties": {
                    "name": {
                        "id": "name",
                        "type": "string"
                    },
                    "phy": {
                        "id": "phy",
                        "type": "string"
                    },
                    "channel": {
                        "id": "channel",
                        "type": "number"
                    },
                    "channel_width": {
                        "id": "channel_width",
                        "type": "number"
                    },
                    "tx_power": {
                        "id": "tx_power",
                        "type": "number"
                    },
                    "country": {
                        "id": "country",
                        "type": "string",
                        "minLength": 2,
                        "maxLength": 2
                    },
                    "disabled": {
                        "id": "disabled",
                        "type": "boolean",
                        "default": False
                    }
                }
            }
        },
        "interfaces": {
            "id": "interfaces",
            "type": "array",
            "title": "Interfaces",
            "uniqueItems": True,
            "additionalItems": True,
            "items": {
                "type": "object",
                "title": "Interface",
                "additionalProperties": True,
                "properties": {
                    "type": {
                        "id": "type",
                        "type": "string",
                        "enum": [
                            "loopback",
                            "ethernet",
                            "wireless",
                            "bridge",
                            "virtual"
                        ]
                    },
                    "name": {
                        "id": "name",
                        "type": "string"
                    },
                    "mac": {
                        "id": "mac",
                        "type": "string"
                    },
                    "mtu": {
                        "id": "mtu",
                        "type": "number",
                        "default": 1500
                    },
                    "txqueuelen": {
                        "id": "txqueuelen",
                        "type": "number"
                    },
                    "autostart": {
                        "id": "autostart",
                        "type": "boolean",
                        "default": True
                    },
                    "addresses": {
                        "id": "addresses",
                        "type": "array",
                        "title": "Addresses",
                        "uniqueItems": True,
                        "additionalItems": True,
                        "items": {
                            "type": "object",
                            "title": "Address",
                            "additionalProperties": True,
                            "properties": {
                                "address": {
                                    "id": "address",
                                    "type": "string"
                                },
                                "mask": {
                                    "id": "mask",
                                    "type": "number"
                                },
                                "family": {
                                    "id": "family",
                                    "type": "string",
                                    "enum": [
                                        "ipv4",
                                        "ipv6"
                                    ]
                                },
                                "proto": {
                                    "id": "proto",
                                    "type": "string",
                                    "enum": [
                                        "static",
                                        "dhcp"
                                    ]
                                }
                            }
                        }
                    },
                    "bridge_members": {
                        "id": "bridge_members",
                        "type": "array",
                        "title": "Bridge Members",
                        "items": [
                            {
                                "type": "string"
                            }
                        ]
                    },
                    "wireless": {
                        "id": "wireless",
                        "type": "object",
                        "title": "Wireless",
                        "additionalProperties": True,
                        "properties": {
                            "radio": {
                                "id": "radio",
                                "type": "string"
                            },
                            "bitrate": {
                                "id": "bitrate",
                                "type": "number"
                            },
                            "ack_distance": {
                                "id": "ack_distance",
                                "type": "number"
                            },
                            "rts_threshold": {
                                "id": "rts_threshold",
                                "type": "number"
                            },
                            "frag_threshold": {
                                "id": "frag_threshold",
                                "type": "number"
                            },
                            "mode": {
                                "id": "mode",
                                "type": "string",
                                "enum": [
                                    "access_point",
                                    "station",
                                    "adhoc",
                                    "wds",
                                    "monitor",
                                    "802.11s"
                                ]
                            },
                            "essid": {
                                "id": "essid",
                                "type": "string"
                            },
                            "bssid": {
                                "id": "bssid",
                                "type": "string"
                            },
                            "encryption": {
                                "id": "encryption",
                                "type": "object",
                                "title": "Encryption",
                                "properties": {
                                    "enabled": {
                                        "id": "enabled",
                                        "type": "boolean"
                                    },
                                    "wpa": {
                                        "id": "wpa",
                                        "type": "array",
                                        "items": {
                                            "type": "integer"
                                        }
                                    },
                                    "authentication": {
                                        "id": "authentication",
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        }
                                    },
                                    "ciphers": {
                                        "id": "ciphers",
                                        "type": "array",
                                        "items": {
                                            "type": "integer"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "routes": {
            "id": "routes",
            "type": "array",
            "title": "Routes",
            "uniqueItems": True,
            "additionalItems": True,
            "items": {
                "type": "object",
                "title": "Route",
                "additionalProperties": True,
                "required": [
                    "device",
                    "destination",
                    "next"
                ],
                "properties": {
                    "device": {
                        "id": "device",
                        "type": "string"
                    },
                    "next": {
                        "id": "next",
                        "type": "string"
                    },
                    "destination": {
                        "id": "destination",
                        "type": "string"
                    }
                }
            }
        },
        "dns_servers": {
            "id": "dns_servers",
            "title": "DNS Servers",
            "type": "array",
            "uniqueItems": True,
            "additionalItems": True,
            "items": {
                "type": "string"
            }
        },
        "dns_search": {
            "id": "dns_search",
            "title": "DNS Search",
            "type": "array",
            "uniqueItems": True,
            "additionalItems": True,
            "items": {
                "type": "string"
            }
        }
    }
}
