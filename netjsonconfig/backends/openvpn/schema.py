"""
OpenVpn 2.3 specific JSON-Schema definition
"""

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "additionalProperties": True,
    "definitions": {
        "tunnel": {
            "type": "object",
            "required": [
                "name",
                "mode",
                "proto",
                "dev"
            ],
            "properties": {
                "name": {
                    "title": "name",
                    "description": "descriptive name for internal use, (only alphanumeric "
                                   "characters, dashes and underscores allowed)",
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 24,
                    "pattern": "^[0-9A-Za-z_-]*$",
                    "propertyOrder": 0,
                },
                "mode": {
                    "title": "mode",
                    "type": "string",
                    "propertyOrder": 1,
                },
                "proto": {
                    "title": "protocol",
                    "type": "string",
                    "propertyOrder": 2,
                },
                "port": {
                    "title": "port",
                    "type": "integer",
                    "default": 1194,
                    "maximum": 65535,
                    "minimum": 1,
                    "propertyOrder": 3,
                },
                "dev-type": {
                    "title": "device type",
                    "description": "tun (layer3) or tap (layer2)",
                    "type": "string",
                    "enum": ["tun", "tap"],
                    "propertyOrder": 4,
                },
                "dev": {
                    "title": "device name",
                    "description": "VPN interface name",
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 15,
                    "pattern": "^[^\\s]*$",
                    "propertyOrder": 5,
                },
                "local": {
                    "title": "local",
                    "type": "string",
                    "description": "Local hostname or IP address on which OpenVPN will listen to. "
                                   "If unspecified, OpenVPN will bind to all interfaces.",
                    "propertyOrder": 7,
                },
                "comp-lzo": {
                    "title": "LZO compression",
                    "description": "Use fast LZO compression; may add up to 1 "
                                   "byte per packet for incompressible data",
                    "type": "string",
                    "enum": ["yes", "no", "adaptive"],
                    "default": "adaptive",
                    "propertyOrder": 8,
                },
                "auth": {
                    "title": "auth digest algorithm",
                    "type": "string",
                    "enum": ["DSA", "DSA-SHA", "DSA-SHA1", "DSA-SHA1-old", "MD4", "MD5", "MDC2",
                             "RIPEMD160", "RSA-MD4", "RSA-MD5", "RSA-MDC2", "RSA-RIPEMD160",
                             "RSA-SHA", "RSA-SHA1", "RSA-SHA1-2", "RSA-SHA224", "RSA-SHA256",
                             "RSA-SHA384", "RSA-SHA512", "SHA", "SHA1", "SHA224", "SHA256",
                             "SHA384", "SHA512", "ecdsa-with-SHA1", "whirlpool", "none"],
                    "default": "SHA1",
                    "propertyOrder": 10,
                },
                "cipher": {
                    "title": "cipher",
                    "type": "string",
                    "description": "Encrypt data channel packets with cipher algorithm",
                    "enum": ["AES-128-CBC", "AES-128-CFB", "AES-128-CFB1", "AES-128-CFB8", "AES-128-OFB",
                             "AES-192-CBC", "AES-192-CFB", "AES-192-CFB1", "AES-192-CFB8", "AES-192-OFB",
                             "AES-256-CBC", "AES-256-CFB", "AES-256-CFB1", "AES-256-CFB8", "AES-256-OFB",
                             "BF-CBC", "BF-CFB", "BF-OFB", "CAMELLIA-128-CBC", "CAMELLIA-128-CFB1",
                             "CAMELLIA-128-CFB8", "CAMELLIA-128-OFB", "CAMELLIA-192-CBC",
                             "CAMELLIA-192-CFB", "CAMELLIA-192-CFB1", "CAMELLIA-192-CFB8",
                             "CAMELLIA-192-OFB", "CAMELLIA-256-CBC", "none"],
                    "default": "BF-CBC",
                    "propertyOrder": 11,
                },
                "engine": {
                    "title": "engine",
                    "type": "string",
                    "description": "Enable OpenSSL hardware-based crypto engine functionality",
                    "enum": ["", "bsd", "rsax", "dynamic"],
                    "options": {
                        "enum_titles": [
                            "No hardware crypto acceleration",
                            "BSD cryptodev engine",
                            "RSAX engine support",
                            "Dynamic engine loading support",
                        ]
                    },
                    "default": "",
                    "propertyOrder": 12,
                },
                "ca": {
                    "title": "CA",
                    "description": "Path to Certificate authority (CA) file in PEM format",
                    "type": "string",
                    "pattern": "^(\\S*)$",
                    "propertyOrder": 13,
                },
                "cert": {
                    "title": "cert",
                    "description": "Path to local peer's signed certificate in PEM format. Must be signed by "
                                   "a certificate authority whose certificate is specified in the CA option",
                    "type": "string",
                    "pattern": "^(\\S*)$",
                    "propertyOrder": 14,
                },
                "key": {
                    "title": "key",
                    "description": "Path to local peer's private key in PEM format. Use the private "
                                   "key which was generated when you built your peer's certificate",
                    "type": "string",
                    "pattern": "^(\\S*)$",
                    "propertyOrder": 15,
                },
                "ns-cert-type": {
                    "title": "NS cert type",
                    "type": "string",
                    "default": "",
                    "propertyOrder": 18
                },
                "mtu-disc": {
                    "title": "MTU discovery",
                    "type": "string",
                    "enum": ["no", "maybe", "yes"],
                    "default": "no",
                    "options": {
                        "enum_titles": [
                            "No - never send DF frames",
                            "Maybe - Use per-route hints",
                            "Yes - always DF"
                        ]
                    },
                    "propertyOrder": 19,
                },
                "mtu-test": {
                    "title": "MTU test",
                    "description": "Empirically measures MTU on connection startup, can take up to "
                                   "3 minutes to complete",
                    "type": "boolean",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 20,
                },
                "fragment": {
                    "title": "fragment",
                    "type": "integer",
                    "description": "Enable internal datagram fragmentation so that no UDP datagrams "
                                   "are sent which are larger than max bytes. 0 means disabled. "
                                   "Valid only when using UDP",
                    "default": 0,
                    "propertyOrder": 21,
                },
                "mssfix": {
                    "title": "mssfix",
                    "type": "integer",
                    "description": "Announce to TCP sessions running over the tunnel that they "
                                   "should limit their send packet sizes such that after OpenVPN has "
                                   "encapsulated them, the resulting UDP packet size that OpenVPN sends "
                                   "to its peer will not exceed max bytes. Valid only when using UDP",
                    "default": 1450,
                    "propertyOrder": 22,
                },
                "keepalive": {
                    "type": "string",
                    "title": "keep alive",
                    "description": "Two numbers separated by space. Refer to the OpenVPN manual page"
                                   "for more information",
                    "pattern": "^(([0-9]*) ([0-9]*)|)$",
                    "propertyOrder": 23,
                },
                "persist-tun": {
                    "title": "persist tunnel",
                    "description": "Don't close and reopen TUN/TAP device or run up/down scripts across "
                                   "SIGUSR1 or ping-restarts",
                    "type": "boolean",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 24,
                },
                "persist-key": {
                    "title": "persist key",
                    "description": "Don't re-read key files across SIGUSR1 or ping-restarts",
                    "type": "boolean",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 25,
                },
                "tun-ipv6": {
                    "title": "tun ipv6",
                    "description": "Build a tun link capable of forwarding IPv6 traffic",
                    "type": "boolean",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 26,
                },
                "up": {
                    "title": "up command",
                    "description": "Run command after successful TUN/TAP device open (pre user UID change)",
                    "type": "string",
                    "pattern": "^(\\S*)$",
                    "propertyOrder": 27,
                },
                "up-delay": {
                    "title": "up delay",
                    "type": "integer",
                    "description": "Delay TUN/TAP open and up script execution until after TCP/UDP "
                                   "connection establishment with peer",
                    "default": 0,
                    "propertyOrder": 28,
                },
                "down": {
                    "title": "down command",
                    "description": "Run command after a TUN/TAP device is closed",
                    "type": "string",
                    "pattern": "^(\\S*)$",
                    "propertyOrder": 29,
                },
                "script-security-level": {
                    "title": "script security level",
                    "type": "integer",
                    "enum": [0, 1, 2, 3],
                    "default": 1,
                    "options": {
                        "enum_titles": [
                            "0 - Strictly no calling of external programs",
                            "1 - Only call built-in executables such as ifconfig, ip, route, or netsh",
                            "2 - Allow calling of built-in executables and user-defined scripts",
                            "3 - Allow passwords to be passed to scripts via environmental variables"
                            " (potentially unsafe)",
                        ]
                    },
                    "propertyOrder": 30,
                },
                "user": {
                    "title": "user",
                    "description": "Change the user ID of the OpenVPN process to the specified user "
                                   "after initialization, dropping privileges in the process",
                    "type": "string",
                    "propertyOrder": 31,
                },
                "group": {
                    "title": "group",
                    "description": "Change the group ID of the OpenVPN process to the speified "
                                   "group after initialization",
                    "type": "string",
                    "propertyOrder": 32,
                },
                "mute": {
                    "title": "mute",
                    "type": "integer",
                    "description": "limit repetitive logging of similar message types to max n occurrences",
                    "propertyOrder": 33,
                },
                "status": {
                    "title": "status file",
                    "description": "Write operational status to file every n seconds; "
                                   "eg: \"/var/run/openvpn.status 10\"",
                    "type": "string",
                    "pattern": "^((\\S*) ([0-9]*)|)$",
                    "propertyOrder": 34,
                },
                "status-version": {
                    "title": "status version format",
                    "type": "integer",
                    "enum": [1, 2, 3],
                    "default": 1,
                    "description": "Status file format version number. Defaults to 1",
                    "propertyOrder": 35,
                },
                "mute-replay-warnings": {
                    "title": "mute replay warnings",
                    "description": "Silence the output of replay warnings, which "
                                   "are a common false alarm on WiFi networks",
                    "type": "boolean",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 36,
                },
                "secret": {
                    "title": "secret",
                    "description": "Path to key for Static Key encryption mode (non-TLS)",
                    "type": "string",
                    "pattern": "^(\\S*)$",
                    "propertyOrder": 37,
                },
                "fast-io": {
                    "title": "fast IO",
                    "description": "(Experimental) Optimize TUN/TAP/UDP I/O writes by avoiding a "
                                   "call to poll/epoll/select prior to the write operation",
                    "type": "boolean",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 49,
                },
                "log": {
                    "title": "log",
                    "description": "Output log messages to file, including output to "
                                   "stdout/stderr which is generated by called scripts",
                    "type": "string",
                    "pattern": "^(\\S*)$",
                    "propertyOrder": 50,
                },
                "verb": {
                    "title": "verbosity",
                    "type": "integer",
                    "enum": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                    "options": {
                        "enum_titles": [
                            "0 - disabled",
                            "1 - default",
                            "2",
                            "3 - recommended",
                            "4", "5", "6", "7", "8", "9", "10", "11"
                        ]
                    },
                    "default": 1,
                    "description": "Set output verbosity for logging and debugging",
                    "propertyOrder": 51,
                },
            }
        },
        "client": {
            "title": "Client",
            "allOf": [
                {"$ref": "#/definitions/tunnel"},
                {
                    "type": "object",
                    "required": ["remote"],
                    "properties": {
                        "mode": {"enum": ["client"]},
                        "proto": {
                            "enum": ["udp", "tcp-client"],
                            "default": "udp",
                            "options": {"enum_titles": ["UDP", "TCP"]}
                        },
                        "remote": {
                            "title": "remote",
                            "type": "array",
                            "additionalItems": True,
                            "minItems": 1,
                            "propertyOrder": 7,
                            "items": {
                                "type": "object",
                                "title": "remote",
                                "additionalProperties": False,
                                "required": [
                                    "host",
                                    "port"
                                ],
                                "properties": {
                                    "host": {
                                        "type": "string",
                                        "maxLength": 63,
                                        "minLength": 1,
                                        "format": "hostname",
                                        "propertyOrder": 1,
                                    },
                                    "port": {
                                        "type": "integer",
                                        "default": 1194,
                                        "maximum": 65535,
                                        "minimum": 1,
                                        "propertyOrder": 2,
                                    }
                                }
                            }
                        },
                        "nobind": {
                            "title": "nobind",
                            "description": "ports are dynamically selected",
                            "type": "boolean",
                            "default": True,
                            "format": "checkbox",
                            "propertyOrder": 6,
                        },
                        "port": {
                            "description": "Use specific local port, ignored if nobind is enabled",
                        },
                        "resolv-retry": {
                            "title": "resolv-retry infinite",
                            "type": "boolean",
                            "description": "If hostname resolution fails, retry to resolve indefinitely",
                            "default": True,
                            "format": "checkbox",
                            "propertyOrder": 8,
                        },
                        "tls-client": {
                            "title": "TLS Client",
                            "description": "Enable TLS authentication",
                            "type": "boolean",
                            "default": True,
                            "format": "checkbox",
                            "propertyOrder": 9,
                        },
                        "ns-cert-type": {
                            "description": "Require that peer certificate was signed with an explicit "
                                           "nsCertType designation of \"server\"",
                            "enum": ["", "server"],
                            "options": {"enum_titles": ["disabled", "server"]}
                        },
                        "auth-user-pass": {
                            "title": "auth user pass",
                            "description": "Path to file containing username/password on 2 lines, "
                                           "only valid when using password authentication",
                            "type": "string",
                            "pattern": "^(\\S*)$",
                            "propertyOrder": 39,
                        }
                    }
                }
            ]
        },
        "server": {
            "title": "Server",
            "allOf": [
                {"$ref": "#/definitions/tunnel"},
                {
                    "type": "object",
                    "properties": {
                        "mode": {"enum": ["server"]},
                        "proto": {
                            "enum": ["udp", "tcp-server"],
                            "default": "udp",
                            "options": {"enum_titles": ["UDP", "TCP"]}
                        },
                        "tls-server": {
                            "title": "TLS Server",
                            "description": "Enable TLS authentication",
                            "type": "boolean",
                            "default": True,
                            "format": "checkbox",
                            "propertyOrder": 9,
                        },
                        "dh": {
                            "title": "DH",
                            "description": "Path to file containing Diffie Hellman parameters in PEM format, "
                                           "required only in TLS-server mode",
                            "type": "string",
                            "propertyOrder": 16,
                        },
                        "crl-verify": {
                            "title": "CRL",
                            "description": "Path to CRL file in PEM format",
                            "type": "string",
                            "pattern": "^(\\S*)$",
                            "propertyOrder": 17,
                        },
                        "ns-cert-type": {
                            "description": "Require that peer certificate was signed with an explicit "
                                           "nsCertType designation of \"client\"",
                            "enum": ["", "client"],
                            "options": {"enum_titles": ["disabled", "client"]}
                        },
                        "duplicate-cn": {
                            "title": "duplicate cn",
                            "description": "Allow multiple clients with the same "
                                           "common name to concurrently connect",
                            "type": "boolean",
                            "default": False,
                            "format": "checkbox",
                            "propertyOrder": 40,
                        },
                        "client-to-client": {
                            "title": "client to client",
                            "description": "Enable client to client communication",
                            "type": "boolean",
                            "default": False,
                            "format": "checkbox",
                            "propertyOrder": 41,
                        },
                        "client-cert-not-required": {
                            "title": "client cert not required",
                            "description": "Don't require client certificate, client will authenticate "
                                           "using username/password only",
                            "type": "boolean",
                            "default": False,
                            "format": "checkbox",
                            "propertyOrder": 42,
                        },
                        "username-as-common-name": {
                            "title": "username as cn",
                            "description": "Valid only for password authentication, use the "
                                           "authenticated username as the common name",
                            "type": "boolean",
                            "default": False,
                            "format": "checkbox",
                            "propertyOrder": 43,
                        },
                        "auth-user-pass-verify": {
                            "title": "auth user pass verify",
                            "description": "Command and method used for password authentication. "
                                           "If set requires the client to provide username and password",
                            "type": "string",
                            "pattern": "^((\\S*) (\\S*)|)$",
                            "propertyOrder": 44,
                        }
                    }
                }
            ]
        }
    },
    "properties": {
        "openvpn": {
            "type": "array",
            "title": "OpenVPN",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 11,
            "items": {
                "type": "object",
                "title": "VPN",
                "additionalProperties": True,
                "oneOf": [
                    {"$ref": "#/definitions/client"},
                    {"$ref": "#/definitions/server"},
                ]
            }
        }
    }
}
