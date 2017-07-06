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

    config: /etc/network/interfaces
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

General settings
----------------

The general settings reside in the ``general`` key of the
*configuration dictionary*, which follows the
`NetJSON General object <http://netjson.org/rfc.html#general1>`_ definition
(see the link for the detailed specification).

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

    config: /etc/hostname
    routerA

    run commands:
    $ timedatectl set-timezone UTC

After modifying the config files run the following command to change the
hostname::

    $ /etc/init.d/hostname.sh start

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

    config: /etc/network/interfaces
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

    config: /etc/network/interfaces
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

    config: /etc/network/interfaces
    auto eth0
    iface eth0 inet static
        address 192.168.1.1
        netmask 255.255.255.0

    auto eth1
    iface eth1 inet dhcp

    config: /etc/resolv.conf
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

    config: /etc/network/interfaces
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

    config: /etc/network/interfaces
    auto lan_bridge
    iface lan_bridge inet static
        address 172.17.0.2
        netmask 255.255.255.0
        bridge_ports eth0:0 eth0:1


Wireless Settings
-----------------

To use a Raspberry Pi as various we need first install the required packages.
You can install it using this command::

    $ sudo apt-get install hostapd dnsmasq

* **hostapd** - The package allows you to use the wireless interface in various
  modes
* **dnsmasq** - The package converts the Raspberry Pi into a DHCP and DNS server

Configure your interface
~~~~~~~~~~~~~~~~~~~~~~~~

Let us say that ``wlan0`` is our wireless interface which we will be using.
First we need to setup a static IP for our wireless interface. Edit the
``wlan0`` section in interface configuration file ``/etc/network/interfaces``::
    auto wlan0
    iface wlan0 inet static
        address 172.128.1.1
        netmask 255.255.255.0
        network 172.128.1.0
        broadcast 172.128.1.255

Reload ``wlan0`` interface with ``sudo ifdown wlan0; sudo ifup wlan0``

Configure hostapd
~~~~~~~~~~~~~~~~~

Create a new configuration file ``/etc/hostapd/hostapd.conf``. The contents of this
configuration will be generated by the render method using NetJSON DeviceConfiguration.

You can check if your wireless service is working by running ``/usr/sbin/hostapd /etc/hostapd/hostapd.conf``.
At this point you should be able to see your wireless network. If you try to connect
to this network, it will authenticate but will not recieve any IP address until
dnsmasq is setup. Use **Ctrl+C** to stop it.
If you want the wireless service to start automatically at boot, find the line::
    #DAEMON_CONF=""

in ``/etc/default/hostapd`` and replace it with::

    DAEMON_CONF="/etc/hostapd/hostapd.conf"

Configure dnsmasq
~~~~~~~~~~~~~~~~~

By default ``/etc/dnsmasq.conf`` contains the complete documentation for how the
file needs to be used. It is advisable to create a copy of the original ``dnsmasq.conf``.
After creating the backup, delete the original file and create a new file ``/etc/dnsmasq.conf``
Setup your DNS and DHCP server. Below is an example configuration file::
    # User interface wlan0
    interface=wlan0
    # Specify the address to listen on
    listen-address=172.128.1.1
    # Bind only the interfaces it is listening on
    bind-interfaces
    # Forward DNS requests to Google DNS
    server=8.8.8.8
    # Never forward plain names (without a dot or domain part)
    domain-needed
    # Never forward addresses in the non-routed address spaces
    bogus-priv
    # Assign IP addresses between 172.128.1.50 and 172.128.1.150 with a 12 hour lease time
    dhcp-range=172.128.1.50,172.128.1.150,12h

Setup IPv4 Forwarding
~~~~~~~~~~~~~~~~~~~~~

We need to enable packet forwarding. Open ``/etc/sysctl.conf`` and uncomment the
following line::

    #net.ipv4.ip_forward=1

This will enable on the next reboot. Incase you want to activate it immediately::

    sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"

Let us assume we have internet connection on ``eth0``. We will need to configure
a NAT between the ``wlan0`` and ``eth0`` interface. It can be done using the followin
commands::

    sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
    sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

These rules need to be applied every time the Raspberry Pi is rebooted. Run ::

    sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

Now open the `/etc/rc.local` file and just above the line ``exit 0``, add the following line::

    iptables-restore < /etc/iptables.ipv4.nat

Now we just need to start our services::

    sudo service hostapd start
    sudo service dnsmasq start

You should now be able to connect to your wireless network setup on the Raspberry Pi

Wireless access point
~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary* represent one of the most
common wireless access point configuration:

.. code-block:: python

    {
        "radios": [
              {
                  "name": "radio0",
                  "phy": "phy0",
                  "driver": "mac80211",
                  "protocol": "802.11n",
                  "channel": 3,
                  "channel_width": 20,
                  "tx_power": 3
              },
          ],
        "interfaces": [
            {
                "name": "wlan0",
                "type": "wireless",
                "wireless": {
                    "radio": "radio0",
                    "mode": "access_point",
                    "ssid": "myWiFi"
                }
            }
        ]
    }

Will be rendered as follows::

    config: /etc/hostapd/hostapd.conf
    interface=wlan0
    driver=nl80211
    hw_mode=g
    channel=3
    ieee80211n=1
    ssid=myWiFi

Wireless AdHoc Mode
~~~~~~~~~~~~~~~~~~~

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

    config: /etc/network/interfaces
    auto wireless
    iface wireless inet static
        address 172.128.1.1
        netmask 255.255.255.0
        wireless-channel 1
        wireless-essid freifunk
        wireless-mode ad-hoc


WPA2 Personal (Pre-Shared Key)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example shows a typical wireless access
point using *WPA2 Personal (Pre-Shared Key)* encryption:

.. code-block:: python

    {
        "radios": [
            {
                "name": "radio0",
                "phy": "phy0",
                "driver": "mac80211",
                "protocol": "802.11n",
                "channel": 3,
                "channel_width": 20,
                "tx_power": 3
            }
        ],
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
                        "cipher": "tkip+ccmp",
                        "key": "passphrase012345"
                    }
                }
            }
        ]
    }

Will be rendered as follows::

    config: /etc/hostapd/hostapd.conf
    interface=wlan0
    driver=nl80211
    hw_mode=g
    channel=3
    ieee80211n=1
    ssid=wpa2-personal
    auth_algs=1
    wpa=2
    wpa_key_mgmt=WPA-PSK
    wpa_passphrase=passphrase012345
    wpa_pairwise=TKIP CCMP

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

The following *configuration dictionary* :

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

    config: /etc/ntp.conf
    server 0.openwrt.pool.ntp.org
    server 1.openwrt.pool.ntp.org
    server 2.openwrt.pool.ntp.org
    server 3.openwrt.pool.ntp.org
