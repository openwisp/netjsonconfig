================
ZeroTier Backend
================

The ``ZeroTier`` backend generates JSON configurations that can be
used with the `ZeroTier Service API <https://docs.zerotier.com/service/v1/>`_ 
to manage ZeroTier networks on `Self-hosted ZeroTier controllers
<https://docs.zerotier.com/self-hosting/introduction>`_.

Its schema is limited to a subset of the features available in ZeroTier
and it doesn't recognize interfaces, radios, wireless settings and so on.

The main methods work just like the :doc:`OpenWRT backend </backends/openwrt>`:

 * ``__init__``
 * ``render``
 * ``generate``
 * ``write``
 * ``json``

The main differences are in the resulting configuration and in its schema.

See an example of initialization and rendering below:

.. code-block:: python

    from netjsonconfig import ZeroTier

    config = ZeroTier({
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
    })
    print(config.render())

Will return the following output::

    // zerotier controller config: 9536600adf654321.json

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

.. _zerotier_backend_schema:

ZeroTier backend schema
-----------------------

The ``ZeroTier`` backend schema is limited, it only recognizes 
an ``zerotier`` key with a list of dictionaries representing vpn instances. 
The structure of these dictionaries is described below.

Alternatively you may also want to take a look at the `ZeroTier JSON-Schema source code
<https://github.com/openwisp/netjsonconfig/blob/master/netjsonconfig/backends/zerotier/schema.py>`_.

According to the `NetJSON <http://netjson.org>`_ spec, any unrecognized property will be ignored.

Server specific settings
~~~~~~~~~~~~~~~~~~~~~~~~

Required properties:

* name

+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| key name               | type    | default      | description                                                                                        |
+========================+=========+==============+====================================================================================================+
| ``name``               | string  |              | name of the network                                                                                |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``id``                 | string  |              | **16-digit** hexadecimal Network ID                                                                |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``nwid``               | string  |              | **16-digit** hexadecimal Network ID (legacy field)                                                 |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``objtype``            | string  | ``network``  | specifies the type of object                                                                       |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``revision``           | integer |              | revision number of the network configuration                                                       |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``creationTime``       | integer |              | time when the network was created                                                                  |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``private``            | boolean |              | whether or not the network is private if ``False``                                                 |
|                        |         |              |                                                                                                    |
|                        |         |              | members will NOT need to be authorized to join                                                     |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``enableBroadcast``    | boolean |              | enable broadcast packets on the network                                                            |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``v4AssignMode``       | object  | ``{}``       |                                                                                                    |
|                        |         |              | +----------------------+---------+----------------------------------------------------------+      |
|                        |         |              | | key name             | type    | description                                              |      |
|                        |         |              | +======================+=========+==========================================================+      |
|                        |         |              | | ``zt``               | boolean | whether ZeroTier should assign IPv4 addresses to members |      |
|                        |         |              | +----------------------+---------+----------------------------------------------------------+      |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``v6AssignMode``       | dict    | ``{}``       |                                                                                                    |
|                        |         |              | +----------------------+---------+---------------------------------------------------------------+ |
|                        |         |              | | key name             | type    | description                                                   | |
|                        |         |              | +======================+=========+===============================================================+ |
|                        |         |              | | ``6plane``           | boolean | whether 6PLANE addressing should be used for IPv6 assignment  | |
|                        |         |              | +----------------------+---------+---------------------------------------------------------------+ |
|                        |         |              | | ``rfc4193``          | boolean | whether RFC4193 addressing should be used for IPv6 assignment | |
|                        |         |              | +----------------------+---------+---------------------------------------------------------------+ |
|                        |         |              | | ``zt``               | boolean | whether ZeroTier should assign IPv6 addresses to members      | |
|                        |         |              | +----------------------+---------+---------------------------------------------------------------+ |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``mtu``                | integer |              | MTU to set on the client virtual network adapter                                                   |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``multicastLimit``     | integer |              | maximum number of recipients per multicast or broadcast,                                           |
|                        |         |              |                                                                                                    |
|                        |         |              | warning - Setting this to ``0`` will disable IPv4 communication on your network                    |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``routes``             | list    | ``[{}]``     | | list of route dictionaries                                                                       |
|                        |         |              |                                                                                                    |
|                        |         |              | +----------------------+---------+------------------------------------------+                      |
|                        |         |              | | key name             | type    | description                              |                      |
|                        |         |              | +======================+=========+==========================================+                      |
|                        |         |              | | ``target``           | string  | target IP address range for the route    |                      |
|                        |         |              | +----------------------+---------+------------------------------------------+                      |
|                        |         |              | | ``via``              | string  | IP address of the next hop for the route |                      |
|                        |         |              | +----------------------+---------+------------------------------------------+                      |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``ipAssignmentPools``  | list    | ``[{}]``     | | list that contains dictionaries specifying                                                       |
|                        |         |              | | a range of IP addresses for the auto assign pool                                                 |
|                        |         |              |                                                                                                    |
|                        |         |              | +----------------------+---------+---------------------------------------+                         |
|                        |         |              | | key name             | type    | description                           |                         |
|                        |         |              | +======================+=========+=======================================+                         |
|                        |         |              | | ``ipRangeStart``     | string  | starting IP address of the pool range |                         |
|                        |         |              | +----------------------+---------+---------------------------------------+                         |
|                        |         |              | | ``ipRangeEnd``       | string  | ending IP address of the pool range   |                         |
|                        |         |              | +----------------------+---------+---------------------------------------+                         |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``dns``                | dict    | ``{}``       | +----------------------+---------+---------------------------+                                     |
|                        |         |              | | key name             | type    | description               |                                     |
|                        |         |              | +======================+=========+===========================+                                     |
|                        |         |              | | ``domain``           | string  | domain for DNS resolution |                                     |
|                        |         |              | +----------------------+---------+---------------------------+                                     |
|                        |         |              | | ``server``           | list    | DNS server IP addresses   |                                     |
|                        |         |              | +----------------------+---------+---------------------------+                                     |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``rules``              | list    | ``[{}]``     | list of network rules dictionaries                                                                 |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``tags``               | list    | ``[{}]``     | list of network tags dictionaries                                                                  |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``remoteTraceTarget``  | string  |              | remote target ID for network tracing                                                               |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+
| ``remoteTraceLevel``   | integer |              | level of network tracing                                                                           |
+------------------------+---------+--------------+----------------------------------------------------------------------------------------------------+


Working around schema limitations
---------------------------------

The schema does not include all the possible ZeroTier settings, but it can render appropiately
any property not included in the schema as long as its type is one the following:

* boolean
* integer
* strings
* lists

For a list of all ZeroTier network configuration settings, refer to the following OpenAPI API specifications:

- `ZeroTier Service (schema: ControllerNetwork) <https://docs.zerotier.com/openapi/servicev1.json>`_

- `ZeroTier Central (schema: NetworkConfig) <https://docs.zerotier.com/openapi/centralv1.json>`_

