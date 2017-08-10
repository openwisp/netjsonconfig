=============
AirOS Backend
=============

.. include:: ../_github.rst

The ``AirOs`` backend allows to generate AirOS v8.3 compatible configurations.

Initialization
--------------

.. automethod:: netjsonconfig.AirOs.__init__

Initialization example:

.. code-block:: python

    from netjsonconfig import AirOs

    router = AirOs({
        "general": {
            "hostname": "MasterAntenna"
        }
    })

If you are unsure about the meaning of the initalization parameters,
read about the following basic concepts:

    * :ref:`configuration_dictionary`
    * :ref:`template`
    * :ref:`context`

Render method
-------------

.. automethod:: netjsonconfig.AirOs.render

Generate method
---------------

.. automethod:: netjsonconfig.AirOs.generate


Write method
------------

.. automethod:: netjsonconfig.AirOs.write


JSON method
-----------

.. automethod:: netjsonconfig.AirOs.json


General settings
----------------

From the ``general`` key we can configure the contact and the location for a device using the ``contact`` and ``location`` properties.

The following snippet specify both contact and location:

.. code-block:: json

    {
        "type": "DeviceConfiguration",
        "general": {
            "contact": "user@example.com",
            "location": "Up in the roof"
        }
    }

Network interface
-----------------

From the ``interfaces`` key we can configure the device network interfaces.

AirOS supports the following types of interfaces

* **network interfaces**: may be of type ``ethernet``
* **wirelesss interfaces**: must be of type ``wireless``
* **bridge interfaces**: must be of type ``bridge``

A network interface can be designed to be the management interfaces by setting the ``managed`` key to ``True`` on the address chosen.

As an example here is a snippet that set the vlan ``eth0.2`` to be the management interface on the address ``192.168.1.20``

.. code-block:: json

   {
       "interfaces": [
           {
               "name": "eth0.2",
               "type": "ethernet",
               "addresses": [
                   {
                       "address": "192.168.1.20",
                       "family": "ipv4",
                       "managed": true,
                       "mask": 24,
                       "proto": "static"
                   }
               ]
           }
       ]
   }

Ethernet
========

The ``ethernet`` interface can be configured to allow auto-negotiation and flow control with the properties ``autoneg`` and ``flowcontrol``

As an example here is a snippet that enables both auto-negotiation and flow control

.. code-block:: json

    {
        "interfaces": [
            {
                "type": "ethernet",
                "name": "eth0",
                "autoneg": true,
                "flowcontrol": true
           }
       ]
   }


DNS servers
-----------


GUI
---

As an extension to `NetJSON <http://netjson.org/rfc.html>` you can use the ``gui`` key to set the language of the interface 

The default values for this key are as reported below

.. code-block:: json

    {
        "type": "DeviceConfiguration",
        "gui": {
            "language": "en_US",
        }
    }

Netmode
-------

AirOS v8.3 can operate in ``bridge`` and ``router`` mode (but defaults to ``bridge``) and this can be specified with the ``netmode`` property.

.. code-block:: json

    {
        "type": "DeviceConfiguration",
        "netmode": "bridge"
    }

NTP servers
-----------

This is an extension to the `NetJSON` specification.

By setting the key ``ntp`` property in your input you can provide the configuration for the ntp client running on the device.

.. code-block:: json

    {
        "type": "DeviceConfiguration",
        "ntp": {
            "enabled": true,
            "server": [
                "0.ubnt.pool.ntp.org"
            ]
        }
    }

For the lazy one we provide these defaults

.. code-block:: json

    {
        "type": "DeviceConfiguration",
        "ntp": {
            "enabled": true,
            "server": [
                "0.pool.ntp.org",
                "1.pool.ntp.org",
                "2.pool.ntp.org",
                "3.pool.ntp.org"
            ]
        }
    }

Users
-----

We can specify the user password as a blob divided into ``salt`` and ``hash``.

From the antenna configuration take the user section.

.. code-block:: ini

    users.status=enabled
    users.1.status=enabled
    users.1.name=ubnt
    users.1.password=$1$yRo1tmtC$EcdoRX.JnD4VaEYgghgWg1

In the line ``users.1.password=$1$yRo1tmtC$EcdoRX.JnD4VaEYgghgWg1`` there are both the salt and the password hash in the format ``$ algorithm $ salt $ hash $``, e.g in the previous block ``algorithm=1``, ``salt=yRo1tmtC`` and ``hash=EcdoRX.JnD4VaEYgghgWg1``.

To specify the password in NetJSON use the ``user`` property.

.. code-block:: json

    {
        "type": "DeviceConfiguration",
        "user": {
            "name": "ubnt",
            "passsword": "EcdoRX.JnD4VaEYgghgWg1",
            "salt": "yRo1tmtC"
        }
    }


WPA2
----

AirOS v8.3 supports both WPA2 personal (PSK+CCMP) and WPA2 enterprise (EAP+CCMP) as an authentication protocol. The only ciphers available is CCMP.

As an antenna only has one wireless network available only the first wireless interface will be used during the generation.

As an example here is a snippet that set the authentication protocol to WPA2 personal

.. code-block:: json

    {
        "interfaces": [
            {
                "name": "wlan0",
                "type": "wireless",
                "wireless": {
                    "mode": "station",
                    "radio": "ath0",
                    "ssid": "ap-ssid-example",
                    "encryption": {
                        "protocol": "wpa2_personal",
                        "key": "changeme"
                    }
                }
            }
        ]
    }

And another that set the authentication protocol to WPA2 enterprise

.. code-block:: json

    {
        "interfaces": [
            {
                "name": "wlan0",
                "type": "wireless",
                "wireless": {
                    "mode": "station",
                    "radio": "ath0",
                    "ssid": "ap-ssid-example",
                    "encryption": {
                        "protocol": "wpa2_enterprise",
                        "identity": "my-identity",
                        "password": "changeme",
                    }
                }
            }
        ]
    
