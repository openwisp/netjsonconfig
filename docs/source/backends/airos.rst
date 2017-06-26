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
