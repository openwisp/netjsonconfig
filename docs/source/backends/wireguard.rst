=================
WireGuard Backend
=================

.. include:: ../_github.rst

The ``WireGuard`` backend allows to generate WireGuard configurations.

Its schema is limited to a subset of the features available in WireGuard and it doesn't recognize
interfaces, radios, wireless settings and so on.

The main methods work just like the :doc:`OpenWRT backend </backends/openwrt>`:

* ``__init__``
* ``render``
* ``generate``
* ``write``
* ``json``

The main differences are in the resulting configuration and in its schema.

See an example of initialization and rendering below:

.. code-block:: python

    from netjsonconfig import Wireguard

    config = Wireguard(
        {
            "wireguard": [
                {
                    "name": "wg",
                    "private_key": "QFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=",
                    "port": 40842,
                    "address": "10.0.0.1/24",
                    "peers": [
                        {
                            "public_key": "jqHs76yCH0wThMSqogDshndAiXelfffUJVcFmz352HI=",
                            "allowed_ips": "10.0.0.3/32",
                        },
                        {
                            "public_key": "94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE=",
                            "allowed_ips": "10.0.0.4/32",
                            "preshared_key": "xisFXck9KfEZga4hlkproH6+86S8ki1tmLtMtqVipjg=",
                            "endpoint_host": "192.168.1.35",
                            "endpoint_port": 4908,
                        },
                    ],
                }
            ]
        }
    )
    print(config.render())

Will return the following output:

.. code-block:: text

    # wireguard config: wg

    [Interface]
    Address = 10.0.0.1/24
    ListenPort = 40842
    PrivateKey = QFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=

    [Peer]
    AllowedIPs = 10.0.0.3/32
    PublicKey = jqHs76yCH0wThMSqogDshndAiXelfffUJVcFmz352HI=

    [Peer]
    AllowedIPs = 10.0.0.4/32
    Endpoint = 192.168.1.35:4908
    PreSharedKey = xisFXck9KfEZga4hlkproH6+86S8ki1tmLtMtqVipjg=
    PublicKey = 94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE=

.. _wireguard_backend_schema:

WireGuard backend schema
------------------------

The ``Wireguard`` backend schema is limited, it only recognizes an ``wireguard`` key with
a list of dictionaries representing vpn instances. The structure of these dictionaries
is described below.

Alternatively you may also want to take a look at the `WireGuard JSON-Schema source code
<https://github.com/openwisp/netjsonconfig/blob/wireguard-vxlan/netjsonconfig/backends/wireguard/schema.py>`_.

According to the `NetJSON <http://netjson.org>`_ spec, any unrecognized property will be ignored.

Server settings (valid both for client and server)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Required properties:

- name
- port
- private_key

+-----------------+---------+--------------+------------------------------------------------------------------------------------+
| key name        | type    | default      | allowed values                                                                     |
+=================+=========+==============+====================================================================================+
| ``name``        | string  |              | 2 to 15 alphanumeric characters, dashes and underscores                            |
+-----------------+---------+--------------+------------------------------------------------------------------------------------+
| ``port``        | integer | ``51820``    | integers                                                                           |
+-----------------+---------+--------------+------------------------------------------------------------------------------------+
| ``private_key`` | string  |              | base64-encoded private key                                                         |
+-----------------+---------+--------------+------------------------------------------------------------------------------------+
| ``peers``       | list    | ``[]``       | list of dictionaries containing following information of                           |
|                 |         |              | each peer:                                                                         |
|                 |         |              |                                                                                    |
|                 |         |              | +-------------------+---------+--------------------------------------------------+ |
|                 |         |              | | key name          | type    | allowed values                                   | |
|                 |         |              | +===================+=========+==================================================+ |
|                 |         |              | | ``public_key``    | string  | base64-encoded public key of peer                | |
|                 |         |              | +-------------------+---------+--------------------------------------------------+ |
|                 |         |              | | ``allowed_ips``   | string  | internal VPN IP address of peer in CIDR notation | |
|                 |         |              | +-------------------+---------+--------------------------------------------------+ |
|                 |         |              | | ``endpoint_host`` | string  | public IP address of peer                        | |
|                 |         |              | +-------------------+---------+--------------------------------------------------+ |
|                 |         |              | | ``endpoint_port`` | integer | integers                                         | |
|                 |         |              | +-------------------+---------+--------------------------------------------------+ |
|                 |         |              | | ``preshared_key`` | string  | base64-encoded pre-shared key                    | |
|                 |         |              | +-------------------+---------+--------------------------------------------------+ |
+-----------------+---------+--------------+------------------------------------------------------------------------------------+

Working around schema limitations
---------------------------------

The schema does not include all the possible WireGuard settings, but it can render appropriately
any property not included in the schema as long as its type is one the following:

* boolean
* integer
* strings
* lists

For a list of all the WireGuard configuration settings, refer to the `"Configuration" section
of wg-quick(8) <https://git.zx2c4.com/wireguard-tools/about/src/man/wg-quick.8>`_ and
`"Configuration File Format" section of wg(8) <https://git.zx2c4.com/wireguard-tools/about/src/man/wg.8>`_

Automatic generation of clients
-------------------------------

.. automethod:: netjsonconfig.OpenWrt.wireguard_auto_client

Example:

.. code-block:: python

    from netjsonconfig import OpenWrt

    server_config = {
        "name": "wg",
        "port": 51820,
        "public_key": "94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE=",
        "server_ip_network": "10.0.0.1/32"
    }
    client_config = OpenWrt.wireguard_auto_client(host='wireguard.test.com',
                                        server=server_config,
                                        public_key=server_config['public_key'],
                                        port=51820,
                                        private_key='QFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=',
                                        ip_address='10.0.0.5/32',
                                        server_ip_network=server_config['server_ip_network'])
    print(OpenWrt(client_config).render())

Will be rendered as:

.. code-block:: text

    package network

    config interface 'wg'
            list addresses '10.0.0.5/32/32'
            option listen_port '51820'
            option mtu '1420'
            option nohostroute '0'
            option private_key 'QFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI='
            option proto 'wireguard'

    config wireguard_wg 'wgpeer'
            list allowed_ips '10.0.0.1/32'
            option endpoint_host 'wireguard.test.com'
            option endpoint_port '51820'
            option persistent_keepalive '60'
            option public_key '94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE='
            option route_allowed_ips '1'

.. note::

    The current implementation of **WireGuard VPN** backend is implemented with
    **OpenWrt** backend. Hence, the example above shows configuration generated for
    OpenWrt.
