============================
VXLAN over WireGuard Backend
============================

.. include:: ../_github.rst

The ``VXLAN over WireGuard`` backend extends :doc:`Wireguard backend </backends/wireguard>`
to add configurations required for configuring VXLAN tunnels encapsulated in
WireGuard tunnels.

Automatic generation of clients
-------------------------------

.. automethod:: netjsonconfig.OpenWrt.vxlan_wireguard_auto_client

Example:

.. code-block:: python

    from netjsonconfig import OpenWrt

    server_config = {
        "name": "wgvxlan",
        "port": 51820,
        "public_key": "94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE=",
        "server_ip_network": "10.0.0.1/32",
        "server_ip_address": "10.0.0.1"
    }
    client_config = OpenWrt.vxlan_wireguard_auto_client(host='wireguard.test.com',
                                        vni=1,
                                        server_ip_address=server_config['server_ip_address'],
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

    config interface 'wgvxlan'
            list addresses '10.0.0.5/32/32'
            option listen_port '51820'
            option mtu '1420'
            option nohostroute '0'
            option private_key 'QFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI='
            option proto 'wireguard'

    config interface 'vxlan'
            option enabled '1'
            option ifname 'vxlan'
            option mtu '1280'
            option peeraddr '10.0.0.1'
            option port '4789'
            option proto 'vxlan'
            option rxcsum '1'
            option ttl '64'
            option tunlink 'wgvxlan'
            option txcsum '1'
            option vid '1'

    config wireguard_wgvxlan 'wgpeer'
            list allowed_ips '10.0.0.1/32'
            option endpoint_host 'wireguard.test.com'
            option endpoint_port '51820'
            option persistent_keepalive '60'
            option public_key '94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE='
            option route_allowed_ips '1'

.. note::

    The current implementation of **VXLAN over WireGuard** VPN backend is implemented with
    **OpenWrt** backend. Hence, the example above shows configuration generated for
    OpenWrt.
