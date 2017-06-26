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


