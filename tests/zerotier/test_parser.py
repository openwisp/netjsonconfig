import os
import unittest
from copy import deepcopy

from netjsonconfig import ZeroTier
from netjsonconfig.exceptions import ParseError, ValidationError


class TestParser(unittest.TestCase):
    """
    Tests for netjsonconfig.backends.zerotier.parser.BaseParser
    """

    # Single test config
    _TEST_CONFIG = {
        "zerotier": [
            {
                "id": "9536600adf654321",
                "nwid": "9536600adf654321",
                "objtype": "network",
                "revision": 1,
                "creationTime": 1632012345,
                "name": "zerotier-openwisp-network",
                "private": True,
                "enableBroadcast": True,
                "v4AssignMode": {"zt": True},
                "v6AssignMode": {"6plane": False, "rfc4193": True, "zt": True},
                "mtu": 2700,
                "multicastLimit": 16,
                "routes": [{"target": "10.0.0.0/24", "via": "10.0.0.1"}],
                "ipAssignmentPools": [
                    {"ipRangeStart": "10.0.0.10", "ipRangeEnd": "10.0.0.100"}
                ],
                "dns": {"domain": "zerotier.openwisp.io", "servers": ["10.147.20.3"]},
                "rules": [
                    {
                        "etherType": 2048,
                        "not": True,
                        "or": False,
                        "type": "MATCH_ETHERTYPE",
                    },
                    {"type": "ACTION_DROP"},
                ],
                "capabilities": [
                    {
                        "default": True,
                        "id": 1,
                        "rules": [
                            {
                                "etherType": 2048,
                                "not": True,
                                "or": False,
                                "type": "MATCH_ETHERTYPE",
                            }
                        ],
                    }
                ],
                "tags": [{"default": 1, "id": 1}],
                "remoteTraceTarget": "7f5d90eb87",
                "remoteTraceLevel": 1,
            }
        ]
    }

    # Multiple test config
    _TEST_MULTIPLE_CONFIG = deepcopy(_TEST_CONFIG)
    _TEST_MULTIPLE_CONFIG["zerotier"].append(
        {
            "id": "9536600adf654322",
            "nwid": "9536600adf654322",
            "objtype": "network",
            "revision": 1,
            "creationTime": 1632012345,
            "name": "zerotier-openwisp-network-2",
            "private": True,
            "enableBroadcast": True,
            "v4AssignMode": {"zt": True},
            "v6AssignMode": {"6plane": False, "rfc4193": True, "zt": True},
            "mtu": 2700,
            "multicastLimit": 16,
            "routes": [{"target": "10.0.0.0/24", "via": "10.0.0.1"}],
            "ipAssignmentPools": [
                {"ipRangeStart": "10.0.0.10", "ipRangeEnd": "10.0.0.100"}
            ],
            "dns": {"domain": "zerotier.openwisp.io", "servers": ["10.147.20.3"]},
            "tags": [{"default": 1, "id": 1}],
            "remoteTraceTarget": "7f5d90eb87",
            "remoteTraceLevel": 1,
        }
    )

    def test_parse_exception(self):
        try:
            ZeroTier(native=10)
        except Exception as e:
            self.assertIsInstance(e, ParseError)
        else:
            self.fail("Exception not raised")

    def test_parse_text(self):
        native = """// zerotier controller config: 9536600adf654321.json

{
    "capabilities": [
        {
            "default": true,
            "id": 1,
            "rules": [
                {
                    "etherType": 2048,
                    "not": true,
                    "or": false,
                    "type": "MATCH_ETHERTYPE"
                }
            ]
        }
    ],
    "creationTime": 1632012345,
    "dns": {
        "domain": "zerotier.openwisp.io",  // test
        "servers": [
            "10.147.20.3"
        ]
    },
    "enableBroadcast": true,
    "id": "9536600adf654321",
    "ipAssignmentPools": [
        {
            "ipRangeEnd": "10.0.0.100",
            "ipRangeStart": "10.0.0.10"
        }
    ],
    "mtu": 2700,  // test
    "multicastLimit": 16,
    "name": "zerotier-openwisp-network",
    "nwid": "9536600adf654321",
    "objtype": "network",
    "private": true,
    "remoteTraceLevel": 1,
    "remoteTraceTarget": "7f5d90eb87",
    "revision": 1,
    "routes": [
        {
            "target": "10.0.0.0/24",
            "via": "10.0.0.1"
        }
    ],
    "rules": [
        {
            "etherType": 2048,
            "not": true,
            "or": false,
            "type": "MATCH_ETHERTYPE"
        },
        {
            "type": "ACTION_DROP"
        }
    ],
    "tags": [
        {
            "default": 1,
            "id": 1
        }
    ],
    "v4AssignMode": {
        "zt": true  // test
    },
    "v6AssignMode": {
        "6plane": false,
        "rfc4193": true,
        "zt": true
    }
}
"""
        o = ZeroTier(native=native)
        self.assertDictEqual(o.config, self._TEST_CONFIG)

    def test_parse_text_without_comment(self):
        native = """
{
    "capabilities": [
        {
            "default": true,
            "id": 1,
            "rules": [
                {
                    "etherType": 2048,
                    "not": true,
                    "or": false,
                    "type": "MATCH_ETHERTYPE"
                }
            ]
        }
    ],
    "creationTime": 1632012345,
    "dns": {
        "domain": "zerotier.openwisp.io",
        "servers": [
            "10.147.20.3"
        ]
    },
    "enableBroadcast": true,
    "id": "9536600adf654321",
    "ipAssignmentPools": [
        {
            "ipRangeEnd": "10.0.0.100",
            "ipRangeStart": "10.0.0.10"
        }
    ],
    "mtu": 2700,
    "multicastLimit": 16,
    "name": "zerotier-openwisp-network",
    "nwid": "9536600adf654321",
    "objtype": "network",
    "private": true,
    "remoteTraceLevel": 1,
    "remoteTraceTarget": "7f5d90eb87",
    "revision": 1,
    "routes": [
        {
            "target": "10.0.0.0/24",
            "via": "10.0.0.1"
        }
    ],
    "rules": [
        {
            "etherType": 2048,
            "not": true,
            "or": false,
            "type": "MATCH_ETHERTYPE"
        },
        {
            "type": "ACTION_DROP"
        }
    ],
    "tags": [
        {
            "default": 1,
            "id": 1
        }
    ],
    "v4AssignMode": {
        "zt": true
    },
    "v6AssignMode": {
        "6plane": false,
        "rfc4193": true,
        "zt": true
    }
}
"""
        o = ZeroTier(native=native)
        self.assertDictEqual(o.config, self._TEST_CONFIG)

    _MULTIPLE_VPN_TEXT = """// zerotier controller config: 9536600adf654321.json

{
    "capabilities": [
        {
            "default": true,
            "id": 1,
            "rules": [
                {
                    "etherType": 2048,
                    "not": true,
                    "or": false,
                    "type": "MATCH_ETHERTYPE"
                }
            ]
        }
    ],
    "creationTime": 1632012345,
    "dns": {
        "domain": "zerotier.openwisp.io",
        "servers": [
            "10.147.20.3"
        ]
    },
    "enableBroadcast": true,
    "id": "9536600adf654321",
    "ipAssignmentPools": [
        {
            "ipRangeEnd": "10.0.0.100",
            "ipRangeStart": "10.0.0.10"
        }
    ],
    "mtu": 2700,
    "multicastLimit": 16,
    "name": "zerotier-openwisp-network",
    "nwid": "9536600adf654321",
    "objtype": "network",
    "private": true,
    "remoteTraceLevel": 1,
    "remoteTraceTarget": "7f5d90eb87",
    "revision": 1,
    "routes": [
        {
            "target": "10.0.0.0/24",
            "via": "10.0.0.1"
        }
    ],
    "rules": [
        {
            "etherType": 2048,
            "not": true,
            "or": false,
            "type": "MATCH_ETHERTYPE"
        },
        {
            "type": "ACTION_DROP"
        }
    ],
    "tags": [
        {
            "default": 1,
            "id": 1
        }
    ],
    "v4AssignMode": {
        "zt": true
    },
    "v6AssignMode": {
        "6plane": false,
        "rfc4193": true,
        "zt": true
    }
}

// zerotier controller config: 9536600adf654322.json

{
    "creationTime": 1632012345,
    "dns": {
        "domain": "zerotier.openwisp.io",
        "servers": [
            "10.147.20.3"
        ]
    },
    "enableBroadcast": true,
    "id": "9536600adf654322",
    "ipAssignmentPools": [
        {
            "ipRangeEnd": "10.0.0.100",
            "ipRangeStart": "10.0.0.10"
        }
    ],
    "mtu": 2700,
    "multicastLimit": 16,
    "name": "zerotier-openwisp-network-2",
    "nwid": "9536600adf654322",
    "objtype": "network",
    "private": true,
    "remoteTraceLevel": 1,
    "remoteTraceTarget": "7f5d90eb87",
    "revision": 1,
    "routes": [
        {
            "target": "10.0.0.0/24",
            "via": "10.0.0.1"
        }
    ],
    "tags": [
        {
            "default": 1,
            "id": 1
        }
    ],
    "v4AssignMode": {
        "zt": true
    },
    "v6AssignMode": {
        "6plane": false,
        "rfc4193": true,
        "zt": true
    }
}
"""

    def test_multiple_vpn(self):
        o = ZeroTier(native=self._MULTIPLE_VPN_TEXT)
        self.assertEqual(o.config, self._TEST_MULTIPLE_CONFIG)

    _MULTIPLE_VPN_TEXT_WITHOUT_COMMENT = """
{
    "capabilities": [
        {
            "default": true,
            "id": 1,
            "rules": [
                {
                    "etherType": 2048,
                    "not": true,
                    "or": false,
                    "type": "MATCH_ETHERTYPE"
                }
            ]
        }
    ],
    "creationTime": 1632012345,
    "dns": {
        "domain": "zerotier.openwisp.io",
        "servers": [
            "10.147.20.3"
        ]
    },
    "enableBroadcast": true,
    "id": "9536600adf654321",
    "ipAssignmentPools": [
        {
            "ipRangeEnd": "10.0.0.100",
            "ipRangeStart": "10.0.0.10"
        }
    ],
    "mtu": 2700,
    "multicastLimit": 16,
    "name": "zerotier-openwisp-network",
    "nwid": "9536600adf654321",
    "objtype": "network",
    "private": true,
    "remoteTraceLevel": 1,
    "remoteTraceTarget": "7f5d90eb87",
    "revision": 1,
    "routes": [
        {
            "target": "10.0.0.0/24",
            "via": "10.0.0.1"
        }
    ],
    "rules": [
        {
            "etherType": 2048,
            "not": true,
            "or": false,
            "type": "MATCH_ETHERTYPE"
        },
        {
            "type": "ACTION_DROP"
        }
    ],
    "tags": [
        {
            "default": 1,
            "id": 1
        }
    ],
    "v4AssignMode": {
        "zt": true
    },
    "v6AssignMode": {
        "6plane": false,
        "rfc4193": true,
        "zt": true
    }
}

{
    "creationTime": 1632012345,
    "dns": {
        "domain": "zerotier.openwisp.io",
        "servers": [
            "10.147.20.3"
        ]
    },
    "enableBroadcast": true,
    "id": "9536600adf654322",
    "ipAssignmentPools": [
        {
            "ipRangeEnd": "10.0.0.100",
            "ipRangeStart": "10.0.0.10"
        }
    ],
    "mtu": 2700,
    "multicastLimit": 16,
    "name": "zerotier-openwisp-network-2",
    "nwid": "9536600adf654322",
    "objtype": "network",
    "private": true,
    "remoteTraceLevel": 1,
    "remoteTraceTarget": "7f5d90eb87",
    "revision": 1,
    "routes": [
        {
            "target": "10.0.0.0/24",
            "via": "10.0.0.1"
        }
    ],
    "tags": [
        {
            "default": 1,
            "id": 1
        }
    ],
    "v4AssignMode": {
        "zt": true
    },
    "v6AssignMode": {
        "6plane": false,
        "rfc4193": true,
        "zt": true
    }
}
"""

    def test_multiple_vpn_without_comment(self):
        o = ZeroTier(native=self._MULTIPLE_VPN_TEXT_WITHOUT_COMMENT)
        self.assertEqual(o.config, self._TEST_MULTIPLE_CONFIG)

    def test_parse_tar_bytesio(self):
        conf = deepcopy(self._TEST_MULTIPLE_CONFIG)
        conf.update(
            {"files": [{"path": "/etc/dummy", "mode": "0644", "contents": "testing!"}]}
        )
        tar = ZeroTier(conf).generate()
        o = ZeroTier(native=tar)
        self.assertDictEqual(o.config, self._TEST_MULTIPLE_CONFIG)

    def test_parse_tar_file(self):
        o = ZeroTier(self._TEST_MULTIPLE_CONFIG)
        o.write(name="test", path="/tmp")
        with open("/tmp/test.tar.gz", "rb") as f:
            ZeroTier(native=f)

        os.remove("/tmp/test.tar.gz")
        self.assertDictEqual(o.config, self._TEST_MULTIPLE_CONFIG)

    def test_file_path_min_length(self):
        conf = deepcopy(self._TEST_MULTIPLE_CONFIG)
        conf.update({"files": [{"path": ".", "mode": "0644", "contents": "testing!"}]})
        with self.assertRaises(ValidationError) as err:
            ZeroTier(conf).generate()
        self.assertEqual("'.' is too short", err.exception.message)
