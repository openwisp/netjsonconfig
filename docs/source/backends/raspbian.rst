================
Raspbian Backend
================

.. include:: ../_github.rst

The ``Raspbian`` backend allows to Raspbian compatible configuration files.

Initialization
--------------

.. automethod:: netjsonconfig.Raspbian.__init__


Render method
-------------

.. automethod:: netjsonconfig.OpenWrt.render

Code example:

.. code-block:: python

    from netjsonconfig import OpenWrt

    o = Raspbian({
        "interfaces": [
            {
                "name": "eth0.1",
                "type": "ethernet",
                "addresses": [
                    {
                        "address": "192.168.1.1",
                        "mask": 24,
                        "proto": "static",
                        "family": "ipv4"
                    },
                    {
                        "address": "192.168.2.1",
                        "mask": 24,
                        "proto": "static",
                        "family": "ipv4"
                    },
                    {
                        "address": "fd87::1",
                        "mask": 128,
                        "proto": "static",
                        "family": "ipv6"
                    }
                ]
            }
        ]
    })
    print o.render()

Will return the following output::

    /etc/network/interfaces
    -----------------------
    auto eth0.1
    iface eth0.1 inet static
      address 192.168.1.1
      netmask 255.255.255.0
    iface eth0.1 inet static
      address 192.168.2.1
      netmask 255.255.255.0
    iface eth0.1 inet6 static
      address fd87::1
      netmask 128

Network interfaces
------------------

The network interface settings reside in the ``interfaces`` key of the
*configuration dictionary*, which must contain a list of
`NetJSON interface objects <http://netjson.org/rfc.html#interfaces1>`_
(see the link for the detailed specification).

There are 3 main type of interfaces:

* **network interfaces**: may be of type ``ethernet``, ``virtual``, ``loopback`` or ``other``
* **wireless interfaces**: must be of type ``wireless``
* **bridge interfaces**: must be of type ``bridge``

Loopback Interface
~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "lo",
                "type": "loopback",
                "addresses": [
                    {
                        "address": "127.0.0.1",
                        "mask": 8,
                        "proto": "static",
                        "family": "ipv4"
                    }
                ]
            }
        ]
    }

Will be rendered as follows::

    /etc/network/interfaces
    -----------------------
    auto lo
    iface lo inet static
        address 127.0.0.1
        netmask 255.0.0.0

Dualstack (IPv4 & IPv6)
~~~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "eth0",
                "type": "ethernet",
                "addresses": [
                    {
                        "family": "ipv4",
                        "proto": "static",
                        "address": "10.27.251.1",
                        "mask": 24
                    },
                    {
                        "family": "ipv6",
                        "proto": "static",
                        "address": "fdb4:5f35:e8fd::1",
                        "mask": 48
                    }
                ]
            }
        ]
    }

Will be rendered as follows::

    /etc/network/interfaces
    -----------------------
    auto eth0
    iface eth0 inet static
        address 10.27.251.1
        netmask 255.255.255.0
    iface eth0 inet6 static
        address fdb4:5f35:e8fd::1
        netmask 48

DNS Servers and Search Domains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DNS servers can be set using ``dns_servers``, while search domains can be set using
``dns_search``.

If specified, these values will be automatically added in every interface which has
at least one static ip address; interfaces which have no ip address configured or are using
dynamic ip address configuration won't get the ``dns`` option in the UCI output, eg:

.. code-block:: python

    {
        "dns_servers": ["10.11.12.13", "8.8.8.8"],
        "dns_search": ["openwisp.org", "netjson.org"],
        "interfaces": [
            {
                "name": "eth0",
                "type": "ethernet",
                "addresses": [
                    {
                        "address": "192.168.1.1",
                        "mask": 24,
                        "proto": "static",
                        "family": "ipv4"
                    }
                ]
            },
            {
                "name": "eth1",
                "type": "ethernet",
                "addresses": [
                    {
                        "proto": "dhcp",
                        "family": "ipv4"
                    }
                ]
            }
        ]
    }

Will return the following UCI output::

    /etc/network/interfaces
    -----------------------
    auto eth0
    iface eth0 inet static
        address 192.168.1.1
        netmask 255.255.255.0

    auto eth1
    iface eth1 inet dhcp

    /etc/resolv.conf
    ----------------
    nameserver 10.11.12.13
    nameserver 8.8.8.8
    search openwisp.org
    search netjson.org

DHCP IPv6 Ethernet Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "eth0",
                "type": "ethernet",
                "addresses": [
                    {
                        "proto": "dhcp",
                        "family": "ipv6"
                    }
                ]
            }
        ]
    }

Will be rendered as follows::

    /etc/network/interfaces
    -----------------------
    auto eth0
    iface eth0 inet6 dhcp

Bridge Interfaces
-----------------

Interfaces of type ``bridge`` can contain a option that is specific for network bridges:

* ``bridge_members``: interfaces that are members of the bridge

.. note::
    The bridge members must be active when creating the bridge

Installing the Software
~~~~~~~~~~~~~~~~~~~~~~~

To create a bridge interface you will need to install a program called `brctl` and
is included in `bridge-utils <https://packages.debian.org/search?keywords=bridge-utils>`_.
You can install it using this command::

    $ aptitude install bridge-utils


Bridge Interface Example
~~~~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "lan_bridge",
                "type": "bridge",
                "bridge_members": [
                    "eth0:0",
                    "eth0:1"
                ],
                "addresses": [
                    {
                        "address": "172.17.0.2",
                        "mask": 24,
                        "proto": "static",
                        "family": "ipv4"
                    }
                ]
            }
        ]
    }

Will be rendered as follows::

    /etc/network/interfaces
    -----------------------
    auto lan_bridge
    iface lan_bridge inet static
        address 172.17.0.2
        netmask 255.255.255.0
        bridge_ports eth0:0 eth0:1
