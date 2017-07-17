=============
AirOS Backend
=============

.. include:: ../_github.rst

The ``AirOS`` backend allows to generate AirOS v8.3 compatible configurations.

Initialization
--------------

.. automethod:: netjsonconfig.AirOS.__init__

Initialization example:

.. code-block:: python

    from netjsonconfig import AirOS

    router = AirOS({
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

.. automethod:: netjsonconfig.AirOS.render

Generate method
---------------

.. automethod:: netjsonconfig.AirOS.generate


Write method
------------

.. automethod:: netjsonconfig.AirOS.write


JSON method
-----------

.. automethod:: netjsonconfig.AirOS.json


General settings
----------------

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

DNS servers
-----------


GUI
---

As an extension to `NetJSON <http://netjson.org/rfc.html>` you can use the ``gui`` key to set the language of the interface and show the advanced network configuration option.

The default values for this key are as reported below

.. code-block:: json

    {
        "gui": {
            "language": "en_US",
            "advanced": true
        }
    }

Netmode
-------

AirOS v8.3 can operate in ``bridge`` and ``router`` mode (but defaults to ``bridge``) and this can be specified with the ``netmode`` property

.. code-block:: json

    {
        "netmode": "bridge"
    }

NTP servers
-----------

This is an extension to the `NetJSON` specification.

By setting the key ``ntp_servers`` in your input you can provide a list of ntp servers to use.

.. code-block:: json

    {
        "type": "DeviceConfiguration",
        ...
        "ntp_servers": [
            "0.ubnt.pool.ntp.org"
        ]
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

I the line ``users.1.password=$1$yRo1tmtC$EcdoRX.JnD4VaEYgghgWg1`` there are both the salt and the password hash in the format ``$ algorithm $ salt $ hash $``, e.g in the previous block ``algorithm=1``, ``salt=yRo1tmtC`` and ``hash=EcdoRX.JnD4VaEYgghgWg1``.

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
                "encryption": {
                    "protocol": "wpa2_personal",
                    "key": "changeme"
                }
            }
        ]
    }

And another that set the authentication protocol to WPA2 enterprise, but this is still not supported by netjsonconfig

.. code-block:: json

    {
        "interfaces": [
            {
                "name": "wlan0",
                "type": "wireless",
                "encryption": {
                    "protocol": "wpa2_enterprise",
                    "key": "changeme"
                }
            }
        ]
    }

Leaving the `NetJSON Encryption object <http://netjson.org/rfc.html#rfc.section.5.4.2.1>` empty defaults to no encryption at all.
