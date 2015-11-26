===============
OpenWRT Backend
===============

Render method
-------------

The ``render`` method will convert the NetJSON configuration object into
the native OpenWRT UCI format, eg:

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

Will print::

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

The ``OpenWrt`` backend has a ``generate`` method which generates a
tar.gz archive containing an `OpenWRT <http://openwrt.org>`_ configuration:

.. code-block:: python

    o.generate({
        "interfaces": [
            {
                "name": "eth0",
                "type": "ethernet",
                "addresses": [
                    {
                        "proto": "dhcp",
                        "family": "ipv4"
                    }
                ]
            }
        ]
    })

Will generate an archive named ``openwrt-config.tar.gz`` with the
following file structure::

    /etc/
    /etc/config/
    /etc/config/network

Including additional files
--------------------------

netjsonconfig supports adding arbitrary text files to the generated configuration archive.

.. warning::
    The files won't be included in the output of the ``render`` method because
    doing so would make the UCI output invalid.

The following example code will generate an archive with one file in ``/etc/crontabs/root``:

.. code-block:: python

    from netjsonconfig import OpenWrt

    o = OpenWrt({
        "files": [
            {
                "path": "/etc/crontabs/root",
                "contents": '* * * * * echo "test" > /etc/testfile'
            }
        ]
    })
    o.generate()

New lines must be escaped using ``\n``, or alternatively, the ``contents`` key can be
a list of lines:

.. code-block:: python

    o = OpenWrt({
        "files": [
            {
                "path": "/etc/crontabs/root",
                "contents": [
                    '* * * * * echo "test" > /etc/testfile',
                    '* * * * * echo "test2" > /etc/testfile2'
                ]
            }
        ]
    })
    o.generate()
