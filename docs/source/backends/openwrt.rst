===============
OpenWRT Backend
===============

.. include:: ../_github.rst

The ``OpenWrt`` backend allows to generate OpenWRT compatible configurations.

.. note::
    This backend purposely generates only named UCI blocks.

    UCI stands for `Unified Configuration Interface <https://wiki.openwrt.org/doc/uci>`_
    and it is the default configuration system installed on `OpenWRT <http://openwrt.org>`_
    and its fork `LEDE <https://www.lede-project.org/>`_.

Initialization
--------------

.. automethod:: netjsonconfig.OpenWrt.__init__

If you are unsure about the meaning of the initalization parameters,
read about the following basic concepts:

    * :ref:`configuration_dictionary`
    * :ref:`backend`
    * :ref:`template`
    * :ref:`context`

Initialization example (forward conversion):

.. code-block:: python

    from netjsonconfig import OpenWrt

    router = OpenWrt({
        "general": {
            "hostname": "HomeRouter"
        }
    })

Initialization example (backward conversion):

.. code-block:: python

    from netjsonconfig import OpenWrt

    router = OpenWrt(native=open('./openwrt-config.tar.gz'))

Render method
-------------

.. automethod:: netjsonconfig.OpenWrt.render

Code example:

.. code-block:: python

    from netjsonconfig import OpenWrt

    o = OpenWrt({
        "interfaces": [
            {
                "name": "eth0.1",
                "type": "ethernet",
                "addresses": [
                    {
                        "address": "192.168.1.2",
                        "gateway": "192.168.1.1",
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
                        "address": "fd87::2",
                        "gateway": "fd87::1",
                        "mask": 64,
                        "proto": "static",
                        "family": "ipv6"
                    }
                ]
            }
        ]
    })
    print(o.render())

Will return the following output::

    package network

    config interface 'eth0_1'
            option gateway '192.168.1.1'
            option ifname 'eth0.1'
            option ip6addr 'fd87::2/64'
            option ip6gw 'fd87::1'
            list ipaddr '192.168.1.2/24'
            list ipaddr '192.168.2.1/24'
            option proto 'static'

Generate method
---------------

.. automethod:: netjsonconfig.OpenWrt.generate

Example:

.. code-block:: python

    >>> import tarfile
    >>> from netjsonconfig import OpenWrt
    >>>
    >>> o = OpenWrt({
    ...     "interfaces": [
    ...         {
    ...             "name": "eth0",
    ...             "type": "ethernet",
    ...             "addresses": [
    ...                 {
    ...                     "proto": "dhcp",
    ...                     "family": "ipv4"
    ...                 }
    ...             ]
    ...         }
    ...     ]
    ... })
    >>> stream = o.generate()
    >>> print(stream)
    <_io.BytesIO object at 0x7fd2287fb410>
    >>> tar = tarfile.open(fileobj=stream, mode='r:gz')
    >>> print(tar.getmembers())
    [<TarInfo 'etc/config/network' at 0x7fd228790250>]

As you can see from this example, the ``generate`` method does not write to disk,
but returns an instance of ``io.BytesIO`` which contains a tar.gz file object with the
following file structure::

    /etc/config/network

The configuration archive can then be written to disk, served via HTTP or uploaded
directly on the OpenWRT router where it can be finally  "restored" with ``sysupgrade``::

    sysupgrade -r <archive>

Note that ``sysupgrade -r`` does not apply the configuration, to do this you have
to reload the services manually or reboot the router.

.. note::
   the ``generate`` method intentionally sets the timestamp of the tar.gz archive and its
   members to ``0`` in order to facilitate comparing two different archives: setting the
   timestamp would infact cause the checksum to be different each time even when contents
   of the archive are identical.

Write method
------------

.. automethod:: netjsonconfig.OpenWrt.write

Example:

.. code-block:: python

    >>> import tarfile
    >>> from netjsonconfig import OpenWrt
    >>>
    >>> o = OpenWrt({
    ...     "interfaces": [
    ...         {
    ...             "name": "eth0",
    ...             "type": "ethernet",
    ...             "addresses": [
    ...                 {
    ...                     "proto": "dhcp",
    ...                     "family": "ipv4"
    ...                 }
    ...             ]
    ...         }
    ...     ]
    ... })
    >>> o.write('dhcp-router', path='/tmp/')

Will write the configuration archive in ``/tmp/dhcp-router.tar.gz``.

Parse method
------------

.. automethod:: netjsonconfig.OpenWrt.parse

This method is automatically called when initializing the backend
with the ``native`` argument:

.. code-block:: python

    from netjsonconfig import OpenWrt

    router = OpenWrt(native=open('./openwrt-config.tar.gz'))

The argument passed to ``native`` can be a string containing a dump obtained via
``uci export``, or a file object (real file or ``BytesIO`` instance) representing
a configuration archive in tar.gz format typically used in OpenWRT/LEDE.

JSON method
-----------

.. automethod:: netjsonconfig.OpenWrt.json

Code example:

.. code-block:: python

    >>> from netjsonconfig import OpenWrt
    >>>
    >>> router = OpenWrt({
    ...     "general": {
    ...         "hostname": "HomeRouter"
    ...     }
    ... })
    >>> print(router.json(indent=4))
    {
        "type": "DeviceConfiguration",
        "general": {
            "hostname": "HomeRouter"
        }
    }

General settings
----------------

The general settings reside in the ``general`` key of the
*configuration dictionary*, which follows the
`NetJSON General object <http://netjson.org/rfc.html#general1>`_ definition
(see the link for the detailed specification).

Currently only the ``hostname`` option is processed by this backend.

General object extensions
~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the default *NetJSON General object options*, the ``OpenWrt`` backend
also supports the following custom options:

+-------------------+---------+---------------------------------------------------------------------+
| key name          | type    | function                                                            |
+===================+=========+=====================================================================+
| ``timezone``      | string  | one of the `allowed timezone values`_ (first element of each tuple) |
+-------------------+---------+---------------------------------------------------------------------+

.. _allowed timezone values: https://github.com/openwisp/netjsonconfig/blob/master/netjsonconfig/backends/openwrt/timezones.py

General settings example
~~~~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "general": {
            "hostname": "routerA",
            "timezone": "UTC",
            "ula_prefix": "fd8e:f40a:6701::/48"
        }
    }

Will be rendered as follows::

    package system

    config system 'system'
            option hostname 'routerA'
            option timezone 'UTC'
            option zonename 'UTC'

    package network

    config globals 'globals'
            option ula_prefix 'fd8e:f40a:6701::/48'

Network interfaces
------------------

The network interface settings reside in the ``interfaces`` key of the
*configuration dictionary*, which must contain a list of
`NetJSON interface objects <http://netjson.org/rfc.html#interfaces1>`_
(see the link for the detailed specification).

There are 4 main types of interfaces:

* **network interfaces**: may be of type ``ethernet``, ``virtual``, ``loopback`` or ``other``
* **wireless interfaces**: must be of type ``wireless``
* **bridge interfaces**: must be of type ``bridge``
* **dialup interfaces**: must be of type ``dialup``
* **modem manager interfaces**: must be of type ``modem-manager``

Interface object extensions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the default *NetJSON Interface object options*, the ``OpenWrt`` backend
also supports the following custom options for every type of interface:

+--------------+---------+-----------------------------------------------+
| key name     | type    | allowed values                                |
+==============+=========+===============================================+
| ``network``  | string  | logical interface name (UCI specific)         |
+--------------+---------+-----------------------------------------------+

In the following sections some examples of the most common use cases are shown.

Loopback interface example
~~~~~~~~~~~~~~~~~~~~~~~~~~

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

    package network

    config interface 'lo'
            option ifname 'lo'
            option ipaddr '127.0.0.1'
            option netmask '255.0.0.0'
            option proto 'static'

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

    package network

    config interface 'eth0'
        option ifname 'eth0'
        option ip6addr 'fdb4:5f35:e8fd::1/48'
        option ipaddr '10.27.251.1'
        option netmask '255.255.255.0'
        option proto 'static'

DNS servers and search domains
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
            # the following interface has DHCP enabled
            # and it won't contain the dns setting
            {
                "name": "eth1",
                "type": "ethernet",
                "addresses": [
                    {
                        "proto": "dhcp",
                        "family": "ipv4"
                    }
                ]
            },
            # the following VLAN interface won't get
            # the dns nor the dns_search settings
            {
                "name": "eth1.31",
                "type": "ethernet"
            }
        ]
    }

Will return the following UCI output::

    package network

    config interface 'eth0'
            option dns '10.11.12.13 8.8.8.8'
            option dns_search 'openwisp.org netjson.org'
            option ifname 'eth0'
            option ipaddr '192.168.1.1'
            option netmask '255.255.255.0'
            option proto 'static'

    config interface 'eth1'
            option dns_search 'openwisp.org netjson.org'
            option ifname 'eth1'
            option proto 'dhcp'

    config interface 'eth1_31'
            option ifname 'eth1.31'
            option proto 'none'

DHCP ipv6 ethernet interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "eth0",
                "network": "lan",
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

    package network

    config interface 'lan'
            option ifname 'eth0'
            option proto 'dchpv6'

Using different protocols
~~~~~~~~~~~~~~~~~~~~~~~~~

OpenWRT and LEDE support many protocols (pppoe, pppoa, pptp, l2tp, ecc) and
the list of supported protocols evolves over time.

OpenWISP and netjsonconfig try to stay out of your way by leaving you maximum
flexibility to use any protocol and any configuration option you may need,
just set ``type`` to ``other``, then proceed by setting `proto` and any other
configuration option according to your needs, see the example below.

PPPoE proto example
^^^^^^^^^^^^^^^^^^^

The following configuration dictionary:

.. code-block:: python

    {
        "interfaces": [
            {
                "type": "other",
                "name": "eth0",
                "network": "wan",
                "proto": "pppoe",
                "username": "<username>",
                "password": "<password>"
            }
        ]
    }

Will be rendered as follows::

    package network

    config interface 'wan'
            option ifname 'eth0'
            option password '<password>'
            option proto 'ppoe'
            option username '<username>'

Bridge settings
---------------

Interfaces of type ``bridge`` can contain a few options that are specific for network bridges:

* ``bridge_members``: interfaces that are members of the bridge
* ``stp``: spanning tree protocol

The ``OpenWrt`` backend NetJSON extensions for bridge interfaces:

+-------------------+---------+-------------+-------------------------------------------------------------+
| key name          | type    | default     | allowed values                                              |
+===================+=========+=============+=============================================================+
| ``igmp_snooping`` | boolean | ``True``    | sets the ``multicast_snooping`` kernel setting for a bridge |
+-------------------+---------+-------------+-------------------------------------------------------------+

Bridge interface example
~~~~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "eth0.1",
                "network": "lan",
                "type": "ethernet"
            },
            {
                "name": "eth0.2",
                "network": "wan",
                "type": "ethernet"
            },
            {
                "name": "lan_bridge",  # will be named "br-lan_bridge" by OpenWRT
                "type": "bridge",
                "stp": True,  # enable spanning tree protocol
                "igmp_snooping": True,  # enable imgp snooping
                "bridge_members": [
                    "eth0.1",
                    "eth0.2"
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

    package network

    config interface 'lan'
            option ifname 'eth0.1'
            option proto 'none'

    config interface 'wan'
            option ifname 'eth0.2'
            option proto 'none'

    config interface 'lan_bridge'
            option ifname 'eth0.1 eth0.2'
            option igmp_snooping '1'
            option ipaddr '172.17.0.2'
            option netmask '255.255.255.0'
            option proto 'static'
            option stp '1'
            option type 'bridge'

Wireless settings
-----------------

Interfaces of type ``wireless`` may contain a lot of different combination
of settings to configure wireless connectivity: from simple access points,
to 802.1x authentication, 802.11s mesh networks, adhoc mesh networks, WDS repeaters and much more.

The ``OpenWrt`` backend NetJSON extensions for wireless interfaces:

+---------------+---------+-------------+------------------------------------------------------+
| key name      | type    | default     | allowed values                                       |
+===============+=========+=============+======================================================+
| ``network``   | array   | ``[]``      | attached networks; if left blank will be             |
|               |         |             | automatically determined                             |
+---------------+---------+-------------+------------------------------------------------------+

Some extensions are applicable only when ``mode`` is ``access_point``:

+---------------+---------+-------------+------------------------------------------------------+
| key name      | type    | default     | allowed values                                       |
+===============+=========+=============+======================================================+
| ``wmm``       | boolean | ``True``    | enables WMM (802.11e) support                        |
+---------------+---------+-------------+------------------------------------------------------+
| ``isolate``   | boolean | ``False``   | isolate wireless clients from one another            |
+---------------+---------+-------------+------------------------------------------------------+
| ``macfilter`` | string  | ``disable`` | ACL policy, accepts: "disable", "allow" and "deny"   |
+---------------+---------+-------------+------------------------------------------------------+
| ``maclist``   | array   | ``[]``      | mac addresses filtered according to macfilter policy |
+---------------+---------+-------------+------------------------------------------------------+

These extensions must be used the ``wireless`` object of a wireless interface eg:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "wlan0",
                "type": "wireless",
                "wireless": {
                    "radio": "radio0",
                    "mode": "access_point",
                    "ssid": "myWiFi",
                    # OpenWrt backend NetJSON extensions
                    "wmm": True,
                    "isolate": True
                }
            }
        ]
    }

The same applies for custom configuration options not included in the ``OpenWrt`` backend schema:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "wlan0",
                "type": "wireless",
                "wireless": {
                    "radio": "radio0",
                    "mode": "access_point",
                    "ssid": "myWiFi",
                    # custom configuration options not defined
                    # in the OpenWrt backend schema
                    "beacon_int": 200,
                    "noscan": True,
                    "custom1": "made-up-for-example-purposes",
                }
            }
        ]
    }

In the following sections some examples of the most common use cases are shown.

Wireless access point
~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary* represent one of the most
common wireless access point configuration:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "wlan0",
                "type": "wireless",
                "wireless": {
                    "radio": "radio0",
                    "mode": "access_point",
                    "ssid": "myWiFi",
                    "wmm": True,  # 802.11e
                    "isolate": True  # client isolation
                }
            }
        ]
    }

UCI output::

    package network

    config interface 'wlan0'
            option ifname 'wlan0'
            option proto 'none'

    package wireless

    config wifi-iface 'wifi_wlan0'
            option device 'radio0'
            option ifname 'wlan0'
            option isolate '1'
            option mode 'ap'
            option network 'wlan0'
            option ssid 'myWiFi'
            option wmm '1'

.. note::
   the ``network`` option of the ``wifi-iface`` directive is filled in automatically
   but can be overridden if needed by setting the ``network`` option in the ``wireless``
   section of the *configuration dictionary*. The next example shows how to do this.

.. _wireless_network_option:

Wireless attached to a different network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In some cases you might want to attach a wireless interface to a different network,
for example, you might want to attach a wireless interface to a bridge:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "eth0",
                "type": "ethernet"
            },
            {
                "name": "wlan0",
                "type": "wireless",
                "wireless": {
                    "radio": "radio0",
                    "mode": "access_point",
                    "ssid": "wifi service",
                    # the wireless interface will be attached to the "lan" network
                    "network": ["lan"]
                }
            },
            {
                "name": "lan",  # the bridge will be named br-lan by OpenWRT
                "type": "bridge",
                "bridge_members": [
                    "eth0",
                    "wlan0"
                ],
                "addresses": [
                    {
                        "address": "192.168.0.2",
                        "mask": 24,
                        "proto": "static",
                        "family": "ipv4"
                    }
                ]
            }
        ]
    }

Will be rendered as follows::

    package network

    config interface 'eth0'
            option ifname 'eth0'
            option proto 'none'

    config interface 'wlan0'
            option ifname 'wlan0'
            option proto 'none'

    config interface 'lan'
            option ifname 'eth0 wlan0'
            option ipaddr '192.168.0.2'
            option netmask '255.255.255.0'
            option proto 'static'
            option type 'bridge'

    package wireless

    config wifi-iface 'wifi_wlan0'
            option device 'radio0'
            option ifname 'wlan0'
            option mode 'ap'
            option network 'lan'
            option ssid 'wifi service'

Wireless access point with macfilter ACL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``OpenWrt`` backend supports a custom NetJSON extension for wireless access point
interfaces: ``macfilter`` (read more about ``macfilter`` and ``maclist`` on the
`OpenWRT documentation for Wireless configuration <https://wiki.openwrt.org/doc/uci/wireless#common_options>`_).

In the following example we ban two mac addresses from connecting to a wireless access point:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "wlan0",
                "type": "wireless",
                "wireless": {
                    "radio": "radio0",
                    "mode": "access_point",
                    "ssid": "MyWifiAP",
                    "macfilter": "deny",
                    "maclist": [
                        "E8:94:F6:33:8C:1D",
                        "42:6c:8f:95:0f:00"
                    ]
                }
            }
        ]
    }

UCI output::

    package network

    config interface 'wlan0'
            option ifname 'wlan0'
            option proto 'none'

    package wireless

    config wifi-iface 'wifi_wlan0'
            option device 'radio0'
            option ifname 'wlan0'
            option macfilter 'deny'
            list maclist 'E8:94:F6:33:8C:1D'
            list maclist '42:6c:8f:95:0f:00'
            option mode 'ap'
            option network 'wlan0'
            option ssid 'MyWifiAP'

Wireless mesh (802.11s) example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Setting up **802.11s** interfaces is fairly simple, in the following example we
bridge ``eth0`` with ``mesh0``, the latter being a layer2 802.11s
wireless interface.

.. note::
   in 802.11s mesh mode the ``ssid`` property is not required,
   while ``mesh_id`` is mandatory.

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "eth0",
                "type": "ethernet"
            },
            {
                "name": "mesh0",
                "type": "wireless",
                "wireless": {
                    "radio": "radio0",
                    "mode": "802.11s",
                    "mesh_id": "ninux",
                    "network": ["lan"]
                }
            },
            {
                "name": "lan",
                "type": "bridge",
                "bridge_members": ["eth0", "mesh0"],
                "addresses": [
                    {
                        "address": "192.168.0.1",
                        "mask": 24,
                        "proto": "static",
                        "family": "ipv4"
                    }
                ]
            }
        ]
    }

UCI output::

    package network

    config interface 'eth0'
            option ifname 'eth0'
            option proto 'none'

    config interface 'mesh0'
            option ifname 'mesh0'
            option proto 'none'

    config interface 'lan'
            option ifname 'eth0 mesh0'
            option ipaddr '192.168.0.1'
            option netmask '255.255.255.0'
            option proto 'static'
            option type 'bridge'

    package wireless

    config wifi-iface 'wifi_mesh0'
            option device 'radio0'
            option ifname 'mesh0'
            option mesh_id 'ninux'
            option mode 'mesh'
            option network 'lan'

Wireless mesh (adhoc) example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In wireless adhoc mode, the ``bssid`` property is required.

The following example:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "wlan0",
                "type": "wireless",
                "wireless": {
                    "radio": "radio0",
                    "ssid": "freifunk",
                    "mode": "adhoc",
                    "bssid": "02:b8:c0:00:00:00"
                }
            }
        ]
    }

Will result in::

    package network

    config interface 'wlan0'
            option ifname 'wlan0'
            option proto 'none'

    package wireless

    config wifi-iface 'wifi_wlan0'
            option bssid '02:b8:c0:00:00:00'
            option device 'radio0'
            option ifname 'wlan0'
            option mode 'adhoc'
            option network 'wlan0'
            option ssid 'freifunk'

WDS repeater example
~~~~~~~~~~~~~~~~~~~~

In the following example we show how to configure a WDS station and repeat the signal:

.. code-block:: python

    {
        "interfaces": [
            # client
            {
                "name": "wlan0",
                "type": "wireless",
                "wireless": {
                    "mode": "station",
                    "radio": "radio0",
                    "network": ["wds_bridge"],
                    "ssid": "FreeRomaWifi",
                    "bssid": "C0:4A:00:2D:05:FD",
                    "wds": True
                }
            },
            # repeater access point
            {
                "name": "wlan1",
                "type": "wireless",
                "wireless": {
                    "mode": "access_point",
                    "radio": "radio1",
                    "network": ["wds_bridge"],
                    "ssid": "FreeRomaWifi"
                }
            },
            # WDS bridge
            {
                "name": "br-wds",
                "network": "wds_bridge",
                "type": "bridge",
                "addresses": [
                    {
                        "proto": "dhcp",
                        "family": "ipv4"
                    }
                ],
                "bridge_members": [
                    "wlan0",
                    "wlan1",
                ]
            }
        ]
    }

Will result in::

    package network

    config interface 'wlan0'
            option ifname 'wlan0'
            option proto 'none'

    config interface 'wlan1'
            option ifname 'wlan1'
            option proto 'none'

    config interface 'br_wds'
            option ifname 'wlan0 wlan1'
            option network 'wds_bridge'
            option proto 'dhcp'
            option type 'bridge'

    package wireless

    config wifi-iface 'wifi_wlan0'
            option bssid 'C0:4A:00:2D:05:FD'
            option device 'radio0'
            option ifname 'wlan0'
            option mode 'sta'
            option network 'wds_bridge'
            option ssid 'FreeRomaWifi'
            option wds '1'

    config wifi-iface 'wifi_wlan1'
            option device 'radio1'
            option ifname 'wlan1'
            option mode 'ap'
            option network 'wds_bridge'
            option ssid 'FreeRomaWifi'

WPA2 Personal (Pre-Shared Key)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example shows a typical wireless access
point using *WPA2 Personal (Pre-Shared Key)* encryption:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "wlan0",
                "type": "wireless",
                "wireless": {
                    "radio": "radio0",
                    "mode": "access_point",
                    "ssid": "wpa2-personal",
                    "encryption": {
                        "protocol": "wpa2_personal",
                        # possible cipher values are:
                        #   "auto", "tkip", "ccmp", and "tkip+ccmp"
                        "cipher": "tkip+ccmp",
                        "key": "passphrase012345"
                    }
                }
            }
        ]
    }

UCI output::

    package network

    config interface 'wlan0'
            option ifname 'wlan0'
            option proto 'none'

    package wireless

    config wifi-iface 'wifi_wlan0'
            option device 'radio0'
            option encryption 'psk2+tkip+ccmp'
            option ifname 'wlan0'
            option key 'passphrase012345'
            option mode 'ap'
            option network 'wlan0'
            option ssid 'wpa2-personal'

WPA2 Enterprise (802.1x) ap
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example shows a typical wireless access
point using *WPA2 Enterprise (802.1x)* security on **OpenWRT**,
you can use this type of configuration for networks like
`eduroam <https://www.eduroam.org/>`_:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "wlan0",
                "type": "wireless",
                "wireless": {
                    "radio": "radio0",
                    "mode": "access_point",
                    "ssid": "eduroam",
                    "encryption": {
                        "protocol": "wpa2_enterprise",
                        "cipher": "auto",
                        "key": "radius_secret",
                        "server": "192.168.0.1",
                        "port": 1812,
                        "acct_server": "192.168.0.2",
                        "acct_port": 1813,
                        "nasid": "hostname"
                    }
                }
            }
        ]
    }

UCI Output::

    package network

    config interface 'wlan0'
            option ifname 'wlan0'
            option proto 'none'

    package wireless

    config wifi-iface 'wifi_wlan0'
            option acct_port '1813'
            option acct_server '192.168.0.2'
            option device 'radio0'
            option encryption 'wpa2'
            option ifname 'wlan0'
            option key 'radius_secret'
            option mode 'ap'
            option nasid 'hostname'
            option network 'wlan0'
            option port '1812'
            option server '192.168.0.1'
            option ssid 'eduroam'

WPA2 Enterprise (802.1x) client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*WPA2 Enterprise (802.1x)* client example:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "wlan0",
                "type": "wireless",
                "wireless": {
                    "radio": "radio0",
                    "mode": "station",
                    "ssid": "enterprise-client",
                    "bssid": "00:26:b9:20:5f:09",
                    "encryption": {
                        "protocol": "wpa2_enterprise",
                        "cipher": "auto",
                        "eap_type": "tls",
                        "identity": "test-identity",
                        "password": "test-password",
                    }
                }
            }
        ]
    }

UCI Output::

    package network

    config interface 'wlan0'
            option ifname 'wlan0'
            option proto 'none'

    package wireless

    config wifi-iface 'wifi_wlan0'
            option bssid '00:26:b9:20:5f:09'
            option device 'radio0'
            option eap_type 'tls'
            option encryption 'wpa2'
            option identity 'test-identity'
            option ifname 'wlan0'
            option mode 'sta'
            option network 'wlan0'
            option password 'test-password'
            option ssid 'enterprise-client'

Dialup settings
---------------

Interfaces of type ``dialup`` contain a few options that are specific to dialup connections.

The ``OpenWrt`` backend NetJSON extensions for dialup interfaces:

+--------------+---------+-----------+------------------------------------------------------------------------------------------------------------+
| key name     | type    | default   | allowed values                                                                                             |
+==============+=========+===========+============================================================================================================+
| ``proto``    | string  | ``pppoe`` | ``3g``, ``6in4``, ``aiccu``, ``l2tp``, ``ncm``, ``ppp``, ``pppoa``, ``pppoe``, ``pptp``, ``qmi``, ``wwan`` |
+--------------+---------+-----------+------------------------------------------------------------------------------------------------------------+
| ``password`` | string  | ``""``    |                                                                                                            |
+--------------+---------+-----------+------------------------------------------------------------------------------------------------------------+
| ``username`` | string  | ``""``    |                                                                                                            |
+--------------+---------+-----------+------------------------------------------------------------------------------------------------------------+

Dialup interface example
~~~~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "dsl0",
                "network": "xdsl",
                "proto": "pppoe",
                "password": "jf93nf82o023$",
                "username": "dsluser",
                "mtu": 1448
            }
        ]
    }

Will be rendered as follows::

    package network

    config interface 'xdsl'
            option ifname 'dsl0'
            option proto 'pppoe'
            option username 'dsluser'
            option password 'jf93nf82o023$'
            option mtu '1448'

Modem Manager settings
----------------------

Interfaces of type ``modem-manager`` contain a few options
that are specific to modem-manager interfaces (2G, 3G, 4G, LTE, etc).

These are the ``OpenWrt`` backend NetJSON extensions for Modem Manager interfaces:

+--------------+---------+-----------------+--------------------------------------------+
| key name     | type    | default         | allowed values                             |
+==============+=========+=================+============================================+
| ``proto``    | string  | ``modemanager`` | ``modemanager``                            |
+--------------+---------+-----------------+--------------------------------------------+
| ``apn``      | string  | empty           | APN, can be left blank                     |
+--------------+---------+-----------------+--------------------------------------------+
| ``pin``      | string  | empty           | PIN code, can be left blank                |
+--------------+---------+-----------------+--------------------------------------------+
| ``device``   | string  | empty           | path to device (see note below)            |
+--------------+---------+-----------------+--------------------------------------------+
| ``password`` | string  | empty           | password, can be left blank                |
+--------------+---------+-----------------+--------------------------------------------+
| ``username`` | string  | empty           | username, can be left blank                |
+--------------+---------+-----------------+--------------------------------------------+
| ``metric``   | integer | ``50``          | metric, can be left blank                  |
+--------------+---------+-----------------+--------------------------------------------+
| ``iptype``   | string  | ``ipv4``        | One of ``ipv4``, ``ipv6``, ``ipv4v6``      |
+--------------+---------+-----------------+--------------------------------------------+
| ``lowpower`` | boolean | ``False``       | low power mode                             |
+--------------+---------+-----------------+--------------------------------------------+

.. note::
    ``device`` is a required property but can be left empty so that
    the default value supplied by the hardware itself and already
    present on the device can be left untouched by merging the
    configuration generated with netjsonconfig
    (instead of fully overwriting it).

Modem Manager interface example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "interfaces": [
            {
                "type": "modem-manager",
                "apn": "apn.operator.com",
                "pin": "1234",
                "device": "/sys/devices/platform/ahb/1b000000.usb/usb1/1-1",
                "username": "user123",
                "password": "pwd123456",
                "metric": 50,
                "lowpower": False,
                "name": "modem0",
                "mtu": 1500
            }
        ]
    }

Will be rendered as follows::

    package network

    config interface 'modem0'
            option apn 'apn.operator.com'
            option device '/sys/devices/platform/ahb/1b000000.usb/usb1/1-1'
            option ifname 'wwan0'
            option lowpower '0'
            option metric '50'
            option mtu '1500'
            option password 'pwd123456'
            option pincode '1234'
            option proto 'modemmanager'
            option username 'user123'

Radio settings
--------------

The radio settings reside in the ``radio`` key of the *configuration dictionary*,
which must contain a list of `NetJSON radio objects <http://netjson.org/rfc.html#radios1>`_
(see the link for the detailed specification).

Radio object extensions
~~~~~~~~~~~~~~~~~~~~~~~

In addition to the default *NetJSON Radio object options*, the ``OpenWrt`` backend
also requires setting the following additional options for each radio in the list:

+--------------+---------+-----------------------------------------------+
| key name     | type    | allowed values                                |
+==============+=========+===============================================+
| ``driver``   | string  | mac80211, atheros, ath5k, ath9k, broadcom     |
+--------------+---------+-----------------------------------------------+
| ``protocol`` | string  | 802.11a, 802.11b, 802.11g, 802.11n, 802.11ac  |
+--------------+---------+-----------------------------------------------+

Radio example
~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "radios": [
            {
                "name": "radio0",
                "phy": "phy0",
                "driver": "mac80211",
                "protocol": "802.11n",
                "channel": 11,
                "channel_width": 20,
                "tx_power": 5,
                "country": "IT"
            },
            {
                "name": "radio1",
                "phy": "phy1",
                "driver": "mac80211",
                "protocol": "802.11n",
                "channel": 36,
                "channel_width": 20,
                "tx_power": 4,
                "country": "IT"
            }
        ]
    }

Will be rendered as follows::

    package wireless

    config wifi-device 'radio0'
            option channel '11'
            option country 'IT'
            option htmode 'HT20'
            option hwmode '11g'
            option phy 'phy0'
            option txpower '5'
            option type 'mac80211'

    config wifi-device 'radio1'
            option channel '36'
            option country 'IT'
            option disabled '0'
            option htmode 'HT20'
            option hwmode '11a'
            option phy 'phy1'
            option txpower '4'
            option type 'mac80211'

Automatic channel selection example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to use the "automatic channel selection" feature of OpenWRT, you must set
the channel to ``0`` and, unless you are using neither **802.11n** nor **802.11ac**,
you must set the ``hwmode`` property to tell OpenWRT which band to use
(11g for 2.4 Ghz, 11a for 5 GHz).

The following example sets "automatic channel selection" for two radios, the first radio uses
**802.11n** in the 2.4 GHz band, while the second uses **802.11ac** in the 5 GHz band.

.. code-block:: python

    {
        "radios": [
            {
                "name": "radio0",
                "phy": "phy0",
                "driver": "mac80211",
                "protocol": "802.11n",
                "channel": 0,  # 0 stands for auto
                "hwmode": "11g",  # must set this explicitly, 11g means 2.4 GHz band
                "channel_width": 20
            },
            {
                "name": "radio1",
                "phy": "phy1",
                "driver": "mac80211",
                "protocol": "802.11ac",
                "channel": 0,  # 0 stands for auto
                "hwmode": "11a",  # must set this explicitly, 11a means 5 GHz band
                "channel_width": 80
            }
        ]
    }

UCI output::

    package wireless

    config wifi-device 'radio0'
            option channel 'auto'
            option htmode 'HT20'
            option hwmode '11g'
            option phy 'phy0'
            option type 'mac80211'

    config wifi-device 'radio1'
            option channel 'auto'
            option htmode 'VHT80'
            option hwmode '11a'
            option phy 'phy1'
            option type 'mac80211'

802.11ac example
~~~~~~~~~~~~~~~~

In the following example we show how to configure an *802.11ac* capable radio:

.. code-block:: python

    {
        "radios": [
            {
                "name": "radio0",
                "phy": "phy0",
                "driver": "mac80211",
                "protocol": "802.11ac",
                "channel": 36,
                "channel_width": 80,
            }
        ]
    }

UCI output::

    package wireless

    config wifi-device 'radio0'
            option channel '36'
            option htmode 'VHT80'
            option hwmode '11a'
            option phy 'phy0'
            option type 'mac80211'

Static Routes
-------------

The static routes settings reside in the ``routes`` key of the *configuration dictionary*,
which must contain a list of `NetJSON Static Route objects <http://netjson.org/rfc.html#routes1>`_
(see the link for the detailed specification).

Static route object extensions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the default *NetJSON Route object options*, the ``OpenWrt`` backend
also allows to define the following optional settings:

+--------------+---------+-------------+---------------------------------------------------+
| key name     | type    | default     | description                                       |
+==============+=========+=============+===================================================+
| ``type``     | string  | ``unicast`` | unicast, local, broadcast, multicast, unreachable |
|              |         |             | prohibit, blackhole, anycast                      |
+--------------+---------+-------------+---------------------------------------------------+
| ``mtu``      | string  | ``None``    | MTU for route, only numbers are allowed           |
+--------------+---------+-------------+---------------------------------------------------+
| ``table``    | string  | ``None``    | Routing table id, only numbers are allowed        |
+--------------+---------+-------------+---------------------------------------------------+
| ``onlink``   | boolean |  ``False``  | When enabled, gateway is on link even if the      |
|              |         |             | gateway does not match any interface prefix       |
+--------------+---------+-------------+---------------------------------------------------+

Static route example
~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "routes": [
            {
                "device": "eth1",
                "destination": "192.168.4.1/24",
                "next": "192.168.2.2",
                "cost": 2,
                "source": "192.168.1.10",
                "table": "2",
                "onlink": True,
                "mtu": "1450"
            },
            {
                "device": "eth1",
                "destination": "fd89::1/128",
                "next": "fd88::1",
                "cost": 0,
            }
        ]
    }

Will be rendered as follows::

    package network

    config route 'route1'
            option gateway '192.168.2.2'
            option interface 'eth1'
            option metric '2'
            option mtu '1450'
            option netmask '255.255.255.0'
            option onlink '1'
            option source '192.168.1.10'
            option table '2'
            option target '192.168.4.1'

    config route6 'route2'
            option gateway 'fd88::1'
            option interface 'eth1'
            option metric '0'
            option target 'fd89::1/128'

Policy routing
--------------

The policy routing settings reside in the ``ip_rule`` key of the
*configuration dictionary*, which is a custom NetJSON extension not present in the
original NetJSON RFC.

The ``ip_rule`` key must contain a list of rules, each rule allows the following options:

+-------------------+---------+
| key name          | type    |
+===================+=========+
| ``in``            | string  |
+-------------------+---------+
| ``out``           | string  |
+-------------------+---------+
| ``src``           | string  |
+-------------------+---------+
| ``tos``           | string  |
+-------------------+---------+
| ``mark``          | string  |
+-------------------+---------+
| ``invert``        | boolean |
+-------------------+---------+
| ``lookup``        | string  |
+-------------------+---------+
| ``goto``          | integer |
+-------------------+---------+
| ``action``        | string  |
+-------------------+---------+

For the function and meaning of each key consult the relevant
`OpenWrt documentation about rule directives <https://wiki.openwrt.org/doc/uci/network#ip_rules>`_.

Policy routing example
~~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "ip_rules": [
            {
                "in": "eth0",
                "out": "eth1",
                "src": "192.168.1.0/24",
                "dest": "192.168.2.0/24",
                "tos": 2,
                "mark": "0x0/0x1",
                "invert": True,
                "lookup": "0",
                "action": "blackhole"
            },
            {
                "src": "192.168.1.0/24",
                "dest": "192.168.3.0/24",
                "goto": 0
            },
            {
                "in": "vpn",
                "dest": "fdca:1234::/64",
                "action": "prohibit"
            },
            {
                "in": "vpn",
                "src": "fdca:1235::/64",
                "action": "prohibit"
            }
        ]
    }

Will be rendered as follows::

    package network

    config rule 'rule1'
            option action 'blackhole'
            option dest '192.168.2.0/24'
            option in 'eth0'
            option invert '1'
            option lookup '0'
            option mark '0x0/0x1'
            option out 'eth1'
            option src '192.168.1.0/24'
            option tos '2'

    config rule 'rule2'
            option dest '192.168.3.0/24'
            option goto '0'
            option src '192.168.1.0/24'

    config rule6 'rule3'
            option action 'prohibit'
            option dest 'fdca:1234::/64'
            option in 'vpn'

    config rule6 'rule4'
            option action 'prohibit'
            option in 'vpn'
            option src 'fdca:1235::/64'

Programmable switch settings
----------------------------

The programmable switch settings reside in the ``switch`` key of the *configuration dictionary*,
which is a custom NetJSON extension not present in the original NetJSON RFC.

The ``switch`` key must contain a list of dictionaries, all the following keys are required:

+-------------------+---------+
| key name          | type    |
+===================+=========+
| ``name``          | string  |
+-------------------+---------+
| ``reset``         | boolean |
+-------------------+---------+
| ``enable_vlan``   | boolean |
+-------------------+---------+
| ``vlan``          | list    |
+-------------------+---------+

The elements of the ``vlan`` list must be dictionaries, all the following keys are required:

+-------------------+---------+
| key name          | type    |
+===================+=========+
| ``device``        | string  |
+-------------------+---------+
| ``reset``         | boolean |
+-------------------+---------+
| ``vlan``          | integer |
+-------------------+---------+
| ``ports``         | string  |
+-------------------+---------+

For the function and meaning of each key consult the relevant
`OpenWrt documentation about switch directives <https://wiki.openwrt.org/doc/uci/network#switch>`_.

Switch example
~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "switch": [
            {
                "name": "switch0",
                "reset": True,
                "enable_vlan": True,
                "vlan": [
                    {
                        "device": "switch0",
                        "vlan": 1,
                        "ports": "0t 2 3 4 5"
                    },
                    {
                        "device": "switch0",
                        "vlan": 2,
                        "ports": "0t 1"
                    }
                ]
            }
        ]
    }

Will be rendered as follows::

    package network

    config switch 'switch0'
            option enable_vlan '1'
            option name 'switch0'
            option reset '1'

    config switch_vlan 'switch0_vlan1'
            option device 'switch0'
            option ports '0t 2 3 4 5'
            option vid '1'
            option vlan '1'

    config switch_vlan 'switch0_vlan2'
            option device 'switch0'
            option ports '0t 1'
            option vid '2'
            option vlan '2'

Overriding or disabling ``vid`` UCI option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The OpenWRT/LEDE UCI ``vid`` option of ``switch_vlan`` sections is automatically inferred
from the ``vlan`` number, although it's possible to override it or disable it if needed:

.. code-block:: python

    {
        "switch": [
            {
                "name": "switch0",
                "reset": True,
                "enable_vlan": True,
                "vlan": [
                    {
                        "device": "switch0",
                        "vlan": 1,
                        "vid": 110,  # manual override
                        "ports": "0t 2 3 4 5"
                    },
                    {
                        "device": "switch0",
                        "vlan": 2,
                        # ``None`` or empty string will remove
                        # ``vid`` output from the UCI result
                        "vid": None,
                        "ports": "0t 1"
                    }
                ]
            }
        ]
    }

Will be rendered as follows::

    package network

    config switch 'switch0'
            option enable_vlan '1'
            option name 'switch0'
            option reset '1'

    config switch_vlan 'switch0_vlan1'
            option device 'switch0'
            option ports '0t 2 3 4 5'
            option vid '110'
            option vlan '1'

    config switch_vlan 'switch0_vlan2'
            option device 'switch0'
            option ports '0t 1'
            option vlan '2'

NTP settings
------------

The Network Time Protocol settings reside in the ``ntp`` key of the
*configuration dictionary*, which is a custom NetJSON extension not present in
the original NetJSON RFC.

The ``ntp`` key must contain a dictionary, the allowed options are:

+-------------------+---------+---------------------+
| key name          | type    | function            |
+===================+=========+=====================+
| ``enabled``       | boolean | ntp client enabled  |
+-------------------+---------+---------------------+
| ``enable_server`` | boolean | ntp server enabled  |
+-------------------+---------+---------------------+
| ``server``        | list    | list of ntp servers |
+-------------------+---------+---------------------+

NTP settings example
~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "ntp": {
        "enabled": True,
        "enable_server": False,
        "server": [
            "0.openwrt.pool.ntp.org",
            "1.openwrt.pool.ntp.org",
            "2.openwrt.pool.ntp.org",
            "3.openwrt.pool.ntp.org"
        ]
    }

Will be rendered as follows::

    package system

    config timeserver 'ntp'
            list server '0.openwrt.pool.ntp.org'
            list server '1.openwrt.pool.ntp.org'
            list server '2.openwrt.pool.ntp.org'
            list server '3.openwrt.pool.ntp.org'
            option enable_server '0'
            option enabled '1'

LED settings
------------

The led settings reside in the ``led`` key of the *configuration dictionary*,
which is a custom NetJSON extension not present in the original NetJSON RFC.

The ``led`` key must contain a list of dictionaries, the allowed options are:

+-------------------+---------+
| key name          | type    |
+===================+=========+
| ``name``          | string  |
+-------------------+---------+
| ``default``       | boolean |
+-------------------+---------+
| ``dev``           | string  |
+-------------------+---------+
| ``sysfs``         | string  |
+-------------------+---------+
| ``trigger``       | string  |
+-------------------+---------+
| ``delayoff``      | integer |
+-------------------+---------+
| ``delayon``       | integer |
+-------------------+---------+
| ``interval``      | integer |
+-------------------+---------+
| ``message``       | string  |
+-------------------+---------+
| ``mode``          | string  |
+-------------------+---------+

The required keys are:

* ``name``
* ``sysfs``
* ``trigger``

For the function and meaning of each key consult the relevant
`OpenWrt documentation about led directives <https://wiki.openwrt.org/doc/uci/system#leds>`_.

LED settings example
~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "led": [
            {
                "name": "USB1",
                "sysfs": "tp-link:green:usb1",
                "trigger": "usbdev",
                "dev": "1-1.1",
                "interval": 50
            },
            {
                "name": "USB2",
                "sysfs": "tp-link:green:usb2",
                "trigger": "usbdev",
                "dev": "1-1.2",
                "interval": 50
            },
            {
                "name": "WLAN2G",
                "sysfs": "tp-link:blue:wlan2g",
                "trigger": "phy0tpt"
            }
        ]
    }

Will be rendered as follows::

    package system

    config led 'led_usb1'
            option dev '1-1.1'
            option interval '50'
            option name 'USB1'
            option sysfs 'tp-link:green:usb1'
            option trigger 'usbdev'

    config led 'led_usb2'
            option dev '1-1.2'
            option interval '50'
            option name 'USB2'
            option sysfs 'tp-link:green:usb2'
            option trigger 'usbdev'

    config led 'led_wlan2g'
            option name 'WLAN2G'
            option sysfs 'tp-link:blue:wlan2g'
            option trigger 'phy0tpt'

Including custom options
------------------------

It is very easy to add configuration options that are not explicitly
defined in the schema of the ``OpenWrt`` backend.

For example, in some cases you may need to define a "ppp" interface,
which can use quite a few properties that are not defined in the schema:

.. code-block:: python

    from netjsonconfig import OpenWrt

    o = OpenWrt({
        "interfaces": [
            {
                "name": "ppp0",
                "type": "other",
                "proto": "ppp",
                "device": "/dev/usb/modem1",
                "username": "user1",
                "password": "pwd0123",
                "keepalive": 3,
                "ipv6": True
            }
        ]
    })
    print(o.render())

UCI output::

    package network

    config interface 'ppp0'
            option device '/dev/usb/modem1'
            option ifname 'ppp0'
            option ipv6 '1'
            option keepalive '3'
            option password 'pwd0123'
            option proto 'ppp'
            option username 'user1'

Including custom lists
----------------------

Under specific circumstances, OpenWRT allows adding configuration options in the form of lists.
Many of these UCI options are not defined in the *JSON-Schema* of the ``OpenWrt`` backend,
but the schema allows adding custom properties.

The ``OpenWrt`` backend recognizes list options for the following sections:

 * interface settings
 * ip address settings
 * wireless settings
 * radio settings

Interface list setting example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example shows how to set a list of ``ip6class`` options:

.. code-block:: python

    o = OpenWrt({
        "interfaces": [
            {
                "name": "eth0",
                "type": "ethernet",
                "ip6class": ["wan6", "backbone"]
            }
        ]
    })
    print(o.render())

UCI Output::

    package network

    config interface 'eth0'
            option ifname 'eth0'
            list ip6class 'wan6'
            list ip6class 'backbone'
            option proto 'none'

Address list setting example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example shows how to set a list of dhcp ``reqopts`` settings:

.. code-block:: python

    o = OpenWrt({
        "interfaces": [
            {
                "name": "eth0",
                "type": "ethernet",
                "addresses": [
                    {
                        "proto": "dhcp",
                        "family": "ipv4",
                        "reqopts": ["43", "54"]
                    }
                ]
            }
        ]
    })
    print(o.render())

UCI Output::

    package network

    config interface 'eth0'
            option ifname 'eth0'
            option proto 'dhcp'
            list reqopts '43'
            list reqopts '54'

Radio list setting example
~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example shows how to set a list of advanced capabilities supported
by the radio using ``ht_capab``:

.. code-block:: python

    o = OpenWrt({
        "radios": [
            {
                "name": "radio0",
                "phy": "phy0",
                "driver": "mac80211",
                "protocol": "802.11n",
                "channel": 1,
                "channel_width": 20,
                "ht_capab": ["SMPS-STATIC", "SHORT-GI-20"]
            }
        ]
    })
    print(o.render())

UCI output::

    package wireless

    config wifi-device 'radio0'
            option channel '1'
            list ht_capab 'SMPS-STATIC'
            list ht_capab 'SHORT-GI-20'
            option htmode 'HT20'
            option hwmode '11g'
            option phy 'phy0'
            option type 'mac80211'

Wireless list setting example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example shows how to set the supported basic rates of a
wireless interface using ``basic_rate``:

.. code-block:: python

    o = OpenWrt({
        "interfaces": [
            {
                "name": "wlan0",
                "type": "wireless",
                "wireless": {
                    "radio": "radio0",
                    "mode": "access_point",
                    "ssid": "open",
                    "basic_rate": ["6000", "9000"]
                }
            }
        ]
    })
    print(o.render())

UCI output::

    package network

    config interface 'wlan0'
            option ifname 'wlan0'
            option proto 'none'

    package wireless

    config wifi-iface 'wifi_wlan0'
            list basic_rate '6000'
            list basic_rate '9000'
            option device 'radio0'
            option ifname 'wlan0'
            option mode 'ap'
            option network 'wlan0'
            option ssid 'open'

Including additional files
--------------------------

The ``OpenWrt`` backend supports inclusion of arbitrary plain text files through
the ``files`` key of the *configuration dictionary*. The value of the ``files``
key must be a list in which each item is a dictionary representing a file, each
dictionary is structured as follows:

+-------------------+----------------+----------+----------------------------------------------------------+
| key name          | type           | required |function                                                  |
+===================+================+==========+==========================================================+
| ``path``          | string         | yes      | filesystem path, will be encoded in the tar.gz archive   |
+-------------------+----------------+----------+----------------------------------------------------------+
| ``contents``      | string         | yes      | plain text contents of the file, new lines must be       |
|                   |                |          | encoded as ``\n``                                        |
+-------------------+----------------+----------+----------------------------------------------------------+
| ``mode``          | string         | yes      | filesystem permissions, defaults to ``0644``             |
+-------------------+----------------+----------+----------------------------------------------------------+

The ``files`` key of the *configuration dictionary* is a custom NetJSON extension not
present in the original NetJSON RFC.

.. warning::
    The files are included in the output of the ``render`` method unless you pass
    ``files=False``, eg: ``openwrt.render(files=False)``

Plain file example
~~~~~~~~~~~~~~~~~~

The following example code will generate an archive with one file in ``/etc/crontabs/root``:

.. code-block:: python

    from netjsonconfig import OpenWrt

    o = OpenWrt({
        "files": [
            {
                "path": "/etc/crontabs/root",
                "mode": "0644",
                # new lines must be escaped with ``\n``
                "contents": '* * * * * echo "test" > /etc/testfile\n'
                            '* * * * * echo "test2" > /etc/testfile2'
            }
        ]
    })
    o.generate()

Executable script file example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example will create an executable shell script:

.. code-block:: python

    o = OpenWrt({
        "files": [
            {
                "path": "/bin/hello_world",
                "mode": "0755",
                "contents": "#!/bin/sh\n"
                            "echo 'Hello world'"
            }
        ]
    })
    o.generate()

OpenVPN
-------

This backend includes the schema of the ``OpenVpn`` backend, inheriting its features.

For details regarding the OpenVPN schema please see :ref:`openvpn_backend_schema`.

Schema additions
~~~~~~~~~~~~~~~~

The ``OpenWrt`` backend adds a few properties to the OpenVPN schema, see below.

+--------------------------+---------+--------------+-------------------------------------------------------------+
| key name                 | type    | default      | allowed values                                              |
+==========================+=========+==============+=============================================================+
| ``disabled``             | boolean | ``False``    |                                                             |
+--------------------------+---------+--------------+-------------------------------------------------------------+

OpenVPN example
~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "openvpn": [
            {
                "ca": "ca.pem",
                "cert": "cert.pem",
                "dev": "tap0",
                "dev_type": "tap",
                "dh": "dh.pem",
                "disabled": False,
                "key": "key.pem",
                "mode": "server",
                "name": "test-vpn-server",
                "proto": "udp",
                "tls_server": True
            }
        ]
    }

Will be rendered as follows::

    package openvpn

    config openvpn 'test_vpn_server'
            option ca 'ca.pem'
            option cert 'cert.pem'
            option dev 'tap0'
            option dev_type 'tap'
            option dh 'dh.pem'
            option enabled '1'
            option key 'key.pem'
            option mode 'server'
            option proto 'udp'
            option tls_server '1'

WireGuard
---------

This backend includes the schema of the ``Wireguard`` backend, inheriting its features.

For details regarding the **WireGuard** schema please see :ref:`wireguard_backend_schema`.

Schema additions
~~~~~~~~~~~~~~~~

The ``OpenWrt`` backend adds a few properties to the WireGuard schema, see below.

+-----------------+---------+--------------+-------------------------------------------------------------+
| key name        | type    | default      | description                                                 |
+=================+=========+==============+=============================================================+
| ``network``     | string  | ``None``     | logical interface name (UCI specific),                      |
|                 |         |              |                                                             |
|                 |         |              | 2 to 15 alphanumeric characters, dashes and underscores     |
+-----------------+---------+--------------+-------------------------------------------------------------+
| ``nohostroute`` | boolean | ``False``    | do not add routes to ensure the tunnel endpoints are routed |
|                 |         |              | via non-tunnel device                                       |
+-----------------+---------+--------------+-------------------------------------------------------------+
| ``fwmark``      | string  | ``None``     | firewall mark to apply to tunnel endpoint packets           |
+-----------------+---------+--------------+-------------------------------------------------------------+
| ``ip6prefix``   | list    | ``[]``       | IPv6 prefixes to delegate to other interfaces               |
+-----------------+---------+--------------+-------------------------------------------------------------+
| ``addresses``   | list    | ``[]``       | list of unique IPv4 or IPv6 addresses                       |
+-----------------+---------+--------------+-------------------------------------------------------------+

The ``OpenWrt`` backend also adds ``wireguard_peers`` option for sepecifying a list of
WireGuard Peers. It add the following properties to the ``wireguard_peers`` property of
WireGuard schema.

+-----------------------+---------+-----------+------------------------------------------------------------------------+
| key name              | type    | default   | description                                                            |
+=======================+=========+===========+========================================================================+
| ``interface``         | string  | ``None``  | name of the wireguard interface,                                       |
|                       |         |           |                                                                        |
|                       |         |           | 2 to 15 alphanumeric characters, dashes and underscores                |
+-----------------------+---------+-----------+------------------------------------------------------------------------+
| ``route_allowed_ips`` | boolean | ``False`` | automatically create a route for each of the Allowed IPs for this peer |
+-----------------------+---------+-----------+------------------------------------------------------------------------+

WireGuard example
~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "wg",
                "type": "wireguard",
                "private_key": "QFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=",
                "port": 51820,
                "mtu": 1420,
                "nohostroute": False,
                "fwmark": "",
                "ip6prefix": [],
                "addresses": [
                    {
                        "proto": "static",
                        "family": "ipv4",
                        "address": "10.0.0.5/32",
                        "mask": 32,
                    }
                ],
                "network": "",
            }
        ],
        "wireguard_peers": [
            {
                "interface": "wg",
                "public_key": "94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE=",
                "allowed_ips": ["10.0.0.1/32"],
                "endpoint_host": "wireguard.test.com",
                "endpoint_port": 51820,
                "preshared_key": "",
                "persistent_keepalive": 60,
                "route_allowed_ips": True,
            }
        ]
    }

Will be rendered as follows:

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

VXLAN
-----

``OpenWrt`` backend includes the schema requied for generating VXLAN
interface configouration. This is useful of setting up layer 2 tunnels.


VXLAN Settings
~~~~~~~~~~~~~~

+-------------+-------------------+--------------+-------------------------------------------------------------+
| key name    | type              | default      | description                                                 |
+=============+===================+==============+=============================================================+
| ``network`` | string            |  ``None``    | name of interface,                                          |
|             |                   |              |                                                             |
|             |                   |              | 2 to 15 alphanumeric characters, dashes and underscores     |
+-------------+-------------------+--------------+-------------------------------------------------------------+
| ``vtep``    | string            | ``False``    | VXLAN tunnel endpoint                                       |
+-------------+-------------------+--------------+-------------------------------------------------------------+
| ``port``    | integer           | ``4789``     | port for VXLAN connection                                   |
+-------------+-------------------+--------------+-------------------------------------------------------------+
| ``vni``     | integer or string |  ``None``    | VXLAN Network Identifier                                    |
+-------------+-------------------+--------------+-------------------------------------------------------------+
| ``tunlink`` | list              | ``[]``       | interface to which the VXLAN tunnel will be bound           |
+-------------+-------------------+--------------+-------------------------------------------------------------+
| ``rxcsum``  | boolean           | ``True``     | use checksum validation in RX direction                     |
+-------------+-------------------+--------------+-------------------------------------------------------------+
| ``txcsum``  | boolean           | ``True``     | use checksum validation in TX direction                     |
+-------------+-------------------+--------------+-------------------------------------------------------------+
| ``mtu``     | integer           | ``1280``     | MTU for route, only numbers are allowed                     |
+-------------+-------------------+--------------+-------------------------------------------------------------+
| ``ttl``     | integer           | ``64``       | TTL of the encapsulation packets                            |
+-------------+-------------------+--------------+-------------------------------------------------------------+

VXLAN example
~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "vxlan",
                "type": "vxlan",
                "vtep": "10.0.0.1",
                "port": 4789,
                "vni": 1,
                "tunlink": "",
                "rxcsum": True,
                "txcsum": True,
                "mtu": 1280,
                "ttl": 64,
                "mac": "",
                "disabled": False,
                "network": "",
            },
        ]
    }

Will be rendered as follows:

.. code-block:: text

    package network

    config interface 'vxlan'
            option enabled '0'
            option ifname 'vxlan'
            option mtu '1280'
            option peeraddr '10.0.0.1'
            option port '4789'
            option proto 'vxlan'
            option rxcsum '1'
            option ttl '64'
            option txcsum '1'
            option vid '1'

VXLAN over WireGuard example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since a layer 2 tunnel can be encapsulated in a layer 3 tunnel, here is an
example configuration for setting up a VXLAN tunnel over WireGuard.

The following *configuration dictionary*:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "wgvxlan",
                "type": "wireguard",
                "private_key": "QFdbnuYr7rrF4eONCAs7FhZwP7BXX/jD/jq2LXCpaXI=",
                "port": 51820,
                "mtu": 1420,
                "nohostroute": False,
                "fwmark": "",
                "ip6prefix": [],
                "addresses": [
                    {
                        "proto": "static",
                        "family": "ipv4",
                        "address": "10.0.0.5/32",
                        "mask": 32,
                    }
                ],
                "network": "",
            },
            {
                "name": "vxlan",
                "type": "vxlan",
                "vtep": "10.0.0.1",
                "port": 4789,
                "vni": 1,
                "tunlink": "wgvxlan",
                "rxcsum": True,
                "txcsum": True,
                "mtu": 1280,
                "ttl": 64,
                "mac": "",
                "disabled": False,
                "network": "",
            },
        ],
        "wireguard_peers": [
            {
                "interface": "wgvxlan",
                "public_key": "94a+MnZSdzHCzOy5y2K+0+Xe7lQzaa4v7lEiBZ7elVE=",
                "allowed_ips": ["10.0.0.1/32"],
                "endpoint_host": "wireguard.test.com",
                "endpoint_port": 51820,
                "preshared_key": "",
                "persistent_keepalive": 60,
                "route_allowed_ips": True,
            }
        ]
    }

Will be rendered as follows:

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

All the other settings
----------------------

Do you need to include some configuration directives that are not defined in
the NetJSON spec nor in the schema of the ``OpenWrt`` backend? **Don't panic!**

Because netjsonconfig aims to be very flexible, it ships code that will try
to render extra parts of the *configuration dictionary* into meaningful UCI output.

In order to accomplish this, you must add extra keys to the *configuration dictionary*
which have to meet the following requirements:

* the name of the key must be the name of the package that needs to be configured
* the value of the key must be a ``list``
* each element in the list must be a ``dict``
* each ``dict`` MUST contain a key named ``config_name``
* each ``dict`` MAY contain a key named ``config_value``

This feature is best explained with a few examples.

Dropbear example
~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "dropbear": [
            {
                "config_name": "dropbear",
                "config_value": "dropbear_1",
                "PasswordAuth": "on",
                "RootPasswordAuth": "on",
                "Port": 22
            }
        ]
    }

Will be rendered as follows::

    package dropbear

    config dropbear 'dropbear_1'
            option PasswordAuth 'on'
            option Port '22'
            option RootPasswordAuth 'on'

OLSRd2 example
~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "olsrd2": [
            {
                "config_name": "global",
                "config_value": "global",
                "pidfile": "/var/run/olsrd2.pid",
                "lockfile": "/var/lock/olsrd2"
            },
            {
                "config_name": "log",
                "config_value": "log",
                "syslog": "true",
                "stderr": "true",
                "file": "/var/log/olsrd2.log"
            },
            {
                "config_name": "interface",
                "config_value": "olsr2_common",
                "ifname": [
                    "loopback",
                    "wlan0",
                    "wlan1"
                ]
            }
        ]
    }

Will be rendered as follows::

    package olsrd2

    config global 'global'
        option lockfile '/var/lock/olsrd2'
        option pidfile '/var/run/olsrd2.pid'

    config log 'log'
        option file '/var/log/olsrd2.log'
        option stderr 'true'
        option syslog 'true'

    config interface 'olsr2_common'
        list ifname 'loopback'
        list ifname 'wlan0'
        list ifname 'wlan1'
