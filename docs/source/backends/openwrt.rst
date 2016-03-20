===============
OpenWRT Backend
===============

The ``OpenWrt`` backend is the base backend of the library.

Initialization
--------------

.. automethod:: netjsonconfig.OpenWrt.__init__

Initialization example:

.. code-block:: python

    from netjsonconfig import OpenWrt

    router = OpenWrt({
        "general": {
            "hostname": "HomeRouter"
        }
    })

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
    print(o.render())

Will return the following output::

    package network

    config interface 'eth0_1'
            option ifname 'eth0.1'
            option proto 'static'
            option ipaddr '192.168.1.1/24'

    config interface 'eth0_1_2'
            option ifname 'eth0.1'
            option proto 'static'
            option ipaddr '192.168.2.1/24'

    config interface 'eth0_1_3'
            option ifname 'eth0.1'
            option proto 'static'
            option ip6addr 'fd87::1/128'

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

Including additional files
--------------------------

The ``OpenWrt`` backend supports inclusion of arbitrary plain text files through
the ``files`` key of the *configuration dictionary*. The value of the ``files``
key must be a list in which each item is a dictionary representing a file, each
dictionary is structured as follows:

+-------------------+----------------+----------+----------------------------------------------------------+
| key name          | type           | required |function                                                  |
+===================+================+==========+==========================================================+
| ``path``          | string         | yes      | path of the file in the tar.gz archive                   |
+-------------------+----------------+----------+----------------------------------------------------------+
| ``contents``      | string         | yes      | plain text contents of the file, new lines must be       |
|                   |                |          | encoded as `\n`                                          |
+-------------------+----------------+----------+----------------------------------------------------------+
| ``mode``          | string         | no       | permissions, if omitted will default to ``0644``         |
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

Including arbitrary options
---------------------------

It is very easy to add arbitrary UCI options in the resulting configuration **as long as
the configuration dictionary does not violate the schema**.

.. note::
   This feature is a deliberate design choice aimed at providing maximum flexibility.
   We want to avoid unnecessary limitations.

In the following example we will add two arbitrary options: ``custom`` and ``fancy``.

.. code-block:: python

    from netjsonconfig import OpenWrt

    o = OpenWrt({
        "interfaces": [
            {
                "name": "eth0",
                "type": "ethernet",
                "custom": "custom_value",
                "fancy": True
            }
        ]
    })
    print(o.render())

Will return the following output::

    package network

    config interface 'eth0'
            option ifname 'eth0'
            option custom 'custom_value'
            option fancy '1'
            option proto 'none'

.. note::
   The hypotetical ``custom`` and ``fancy`` options would not be recognized by OpenWRT
   and they would be therefore ignored by the UCI parser.

   We are using them here just to demonstrate how to add complex configuration options that
   are not defined in the NetJSON spec or in the schema of the ``OpenWrt`` backend.

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

    config system
            option hostname 'routerA'
            option timezone 'UTC'

    package network

    config globals 'globals'
            option ula_prefix 'fd8e:f40a:6701::/48'

Network interfaces
------------------

The network interface settings reside in the ``interfaces`` key of the
*configuration dictionary*, which must contain a list of
`NetJSON interface objects <http://netjson.org/rfc.html#interfaces1>`_
(see the link for the detailed specification).

Interface object extensions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the default *NetJSON Interface object options*, the ``OpenWrt`` backend
also supports the following custom options:

* each interface item can specify a ``network`` option which allows to manually set the
  logical interface name
* the ``proto`` key of each item in the ``addresses`` list allows all the UCI proto
  options officially supported by OpenWRT, eg: dhcpv6, ppp, 3g, gre and others
* the ``wireless`` dictionary (valid only for wireless interfaces) can also specify a
  ``network`` key which allows to list on or more networks to which the wireless interface
  will be attached to (see the :ref:`relevant example <wireless_network_option>`)

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
            option ipaddr '127.0.0.1/8'
            option proto 'static'

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

Bridge interface
~~~~~~~~~~~~~~~~

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
            option ipaddr '172.17.0.2/24'
            option proto 'static'
            option type 'bridge'

Wireless interface
~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

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
                        "enabled": True,
                        "protocol": "wpa2_personal",
                        "ciphers": [
                            "tkip",
                            "ccmp"
                        ],
                        "key": "passphrase012345"
                    }
                }
            }
        ]
    }

Will be rendered as follows::

    package network

    config interface 'wlan0'
            option ifname 'wlan0'
            option proto 'none'

    package wireless

    config wifi-iface
            option device 'radio0'
            option encryption 'psk2+tkip+ccmp'
            option ifname 'wlan0'
            option key 'passphrase012345'
            option mode 'ap'
            option network 'wlan0'
            option ssid 'wpa2-personal'

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
            option ipaddr '192.168.0.2/24'
            option proto 'static'
            option type 'bridge'

    package wireless

    config wifi-iface
            option device 'radio0'
            option ifname 'wlan0'
            option mode 'ap'
            option network 'lan'
            option ssid 'wifi service'

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
| ``driver``   | string  | mac80211, madwifi, ath5k, ath9k, broadcom     |
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
| ``mtu``      | string  | ````        | MTU for route, only numbers are allowed           |
+--------------+---------+-------------+---------------------------------------------------+
| ``table``    | string  | ``False``   | Routing table id, only numbers are allowed        |
+--------------+---------+-------------+---------------------------------------------------+
| ``onlink``   | boolean |  ````       | When enabled, gateway is on link even if the      |
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

    config route6
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

    config rule
            option action 'blackhole'
            option dest '192.168.2.0/24'
            option in 'eth0'
            option invert '1'
            option lookup '0'
            option mark '0x0/0x1'
            option out 'eth1'
            option src '192.168.1.0/24'
            option tos '2'

    config rule
            option dest '192.168.3.0/24'
            option goto '0'
            option src '192.168.1.0/24'

    config rule6
            option action 'prohibit'
            option dest 'fdca:1234::/64'
            option in 'vpn'

    config rule6
            option action 'prohibit'
            option in 'vpn'
            option src 'fdca:1235::/64'

Switch settings
---------------

The switch settings reside in the ``switch`` key of the *configuration dictionary*,
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

    config switch
            option enable_vlan '1'
            option name 'switch0'
            option reset '1'

    config switch_vlan
            option device 'switch0'
            option ports '0t 2 3 4 5'
            option vlan '1'

    config switch_vlan
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

All the other settings
----------------------

Do you need to include some configuration directives that are not defined in the NetJSON
spec nor in the schema of the ``OpenWrt`` backend? **Don't panic!**

Netjsonconfig aims to be very flexible, that's why the ``OpenWrt`` backend ships
a ``DefaultRenderer``, which will try to parse any unrecognized key of the
*configuration dictionary* and render meaningful UCI output.

To supply configuration options to the ``DefaultRenderer`` a few prerequisites must be met:

* the name of the key must be the name of the package that needs to be configured
* the value of the key must be of type ``list``
* each element in the list must be of type ``dict``
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
                "PasswordAuth": "on",
                "RootPasswordAuth": "on",
                "Port": 22
            }
        ]
    }

Will be rendered as follows::

    package dropbear

    config dropbear
            option PasswordAuth 'on'
            option Port '22'
            option RootPasswordAuth 'on'

OpenVPN example
~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "openvpn": [
            {
                "config_name": "openvpn",
                "config_value": "client_tun_0",
                "enabled": True,
                "client": True,
                "dev": "tun",
                "proto": "tcp",
                "resolv_retry": "infinite",
                "nobind": True,
                "persist_tun": True,
                "persist_key": True,
                "ca": "/etc/openvpn/ca.crt",
                "cert": "/etc/openvpn/client.crt",
                "key": "/etc/openvpn/client.crt",
                "cipher": "BF-CBC",
                "comp_lzo": "yes",
                "remote": "vpn.myserver.com 1194",
                "enable": True,
                "tls_auth": "/etc/openvpn/ta.key 1",
                "verb": 5,
                "log": "/tmp/openvpn.log"
            }
        ]
    }

Will be rendered as follows::

    package openvpn

    config openvpn 'client_tun_0'
            option ca '/etc/openvpn/ca.crt'
            option cert '/etc/openvpn/client.crt'
            option cipher 'BF-CBC'
            option client '1'
            option comp_lzo 'yes'
            option dev 'tun'
            option enable '1'
            option enabled '1'
            option key '/etc/openvpn/client.crt'
            option log '/tmp/openvpn.log'
            option nobind '1'
            option persist_key '1'
            option persist_tun '1'
            option proto 'tcp'
            option remote 'owm.provinciawifi.it 1194'
            option resolv_retry 'infinite'
            option tls_auth '/etc/openvpn/ta.key 1'
            option verb '5'
