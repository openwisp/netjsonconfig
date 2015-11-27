==============
Basic concepts
==============

Before starting, let's quickly introduce the main concepts used in netjsonconfig:

* **configuration dictionary**: python dictionary representing the configuration of a router
* **backend**: python class used to process the configuration and generate the final
  router configuration
* **schema**: each backend has a `JSON-Schema <http://json-schema.org>`_ which
  defines the useful configuration options that the backend is able to process
* **validation**: the configuration is validated against its JSON-Schema before
  being processed by the backend
* **template**: common configuration options shared among routers (eg: VPNs, SSID)
  which can be passed to backends

Configuration format: NetJSON
-----------------------------

Netjsonconfig is an implementation of the `NetJSON <http://netjson.org>`_ format,
more specifically the ``DeviceConfiguration`` object, therefore to understand the
configuration format that the library uses to generate the final router configurations
it is essential to read at least the relevant `DeviceConfiguration section in the
NetJSON RFC <http://netjson.org/rfc.html#rfc.section.5>`_.

Here it is a simple NetJSON DeviceConfiguration object:

.. code-block:: python

    {
        "type": "DeviceConfiguration",
        "general": {
            "hostname": "RouterA"
        },
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
            }
        ]
    }

The previous example describes a device named ``RouterA`` which has a single
network interface named ``eth0`` with a statically assigned ip address ``192.168.1.1/24``
(CIDR notation).

Because netjsonconfig deals only with ``DeviceConfiguration`` objects, the ``type``
attribute can be omitted, the library will add the correct type automatically.

The previous configuration object therefore can be shortened to:

.. code-block:: python

    {
        "general": {
            "hostname": "RouterA"
        },
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
            }
        ]
    }

From now on we will use the term *configuration dictionary* to refer to
NetJSON DeviceConfiguration objects.

Backends
--------

A backend is a python class used to process the *configuration dictionary* and
generate the final router configuration, each supported firmware or opearting system
will have its own backend and third parties can write their own custom backends.

The current implemented backends are:

 * :doc:`OpenWrt </backends/openwrt>`
 * :doc:`OpenWisp </backends/openwisp>` (based on the ``OpenWrt`` backend)

Example initialization of ``OpenWrt`` backend:

.. code-block:: python

    from netjsonconfig import OpenWrt

    ipv6_router = OpenWrt({
        "type": "DeviceConfiguration",
        "interfaces": [
            {
                "name": "eth0.1",
                "type": "ethernet",
                "addresses": [
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

Schema
------

Each backend has a JSON-Schema, all the backends have a schema which is derived
from the same parent schema, defined in ``netjsonconfig.backends.schema``
(`view source <https://github.com/openwisp/netjsonconfig/blob/master/netjsonconfig/schema.py>`_).

Since different backends may support different features each backend may extend its
schema by adding custom definitions.

Validation
----------

All the backends have a ``validate`` method which is called automatically before
trying to process the configuration.

If the passed configuration violates the schema the ``validate`` method will raise
a ``ValidationError``.

You may call the ``validate`` method in your application arbitrarily, eg: before
trying to save the *configuration dictionary* into a database.

Templates
---------

If you have devices with very similar *configuration dictionaries* you can store the shared
blocks in one or more reusable templates which will be used as a base to build
the final configuration.

Let's illustrate this with a practical example, we have two devices:

 * Router1
 * Router2

Both devices have an ``eth0`` interface in DHCP mode; *Router2* additionally has
an ``eth1`` interface with a statically assigned ipv4 address.

The two routers can be represented with the following code:

.. code-block:: python

    from netjsonconfig import OpenWrt

    router1 = OpenWrt({
        "general": {"hostname": "Router1"}
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

    router2 = OpenWrt({
        "general": {"hostname": "Router2"},
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
            },
            {
                "name": "eth1",
                "type": "ethernet",
                "addresses": [
                    {
                        "address": "192.168.1.1",
                        "mask": 24,
                        "proto": "static",
                        "family": "ipv4"
                    }
                ]
            }
        ]
    })

The two *configuration dictionaries* share the same settings for the ``eth0``
interface, therefore we can make the ``eth0`` settings our template and
refactor the previous code as follows:

.. code-block:: python

    dhcp_template = {
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
    }

    router1 = OpenWrt(config={"general": {"hostname": "Router1"}},
                      templates=[dhcp_template])

    router2_config = {
        "general": {"hostname": "Router2"},
        "interfaces": [
            {
                "name": "eth1",
                "type": "ethernet",
                "addresses": [
                    {
                        "address": "192.168.1.1",
                        "mask": 24,
                        "proto": "static",
                        "family": "ipv4"
                    }
                ]
            }
        ]
    }
    router2 = OpenWrt(router2_config, templates=[dhcp_template])

The function used under the hood to merge dictionaries and lists
is ``netjsonconfig.utils.merge_config``:

.. literalinclude:: /../../netjsonconfig/utils.py
   :lines: 2-22
   :caption: merge_config
   :name: merge_config

Multiple template inheritance
-----------------------------

You might have noticed that the ``templates`` argument is a list; that's because
it's possible to pass multiple templates that will be added one on top of the
other to build the resulting *configuration dictionary*, allowing to reduce or
even eliminate repetitions.
