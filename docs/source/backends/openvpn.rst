===================
OpenVPN 2.3 Backend
===================

.. include:: ../_github.rst

The ``OpenVpn`` backend allows to generate OpenVPN 2.3.x compatible configurations.

Its schema is limited to a subset of the features available in OpenVPN and it doesn't recognize
interfaces, radios, wireless settings and so on.

The main methods work just like the :doc:`OpenWRT backend </backends/openwrt>`:

 * ``__init__``
 * ``render``
 * ``generate``
 * ``write``
 * ``json``

The main differences are in the resulting configuration and in its schema.

See an example of initialization and rendering below:

.. code-block:: python

    from netjsonconfig import OpenVpn

    config = OpenVpn({
        "openvpn": [
            {
                "ca": "ca.pem",
                "cert": "cert.pem",
                "dev": "tap0",
                "dev_type": "tap",
                "dh": "dh.pem",
                "key": "key.pem",
                "mode": "server",
                "name": "example-vpn",
                "proto": "udp",
                "tls_server": True
            }
        ]
    })
    print(config.render())

Will return the following output::

    # openvpn config: test-no-status

    ca ca.pem
    cert cert.pem
    dev tap0
    dev-type tap
    dh dh.pem
    key key.pem
    mode server
    proto udp
    tls-server

.. _openvpn_backend_schema:

OpenVPN backend schema
----------------------

The ``OpenVpn`` backend schema is limited, it only recognizes an ``openvpn`` key with
a list of dictionaries representing vpn instances. The structure of these dictionaries
is described below.

Alternatively you may also want to take a look at the `OpenVPN JSON-Schema source code
<https://github.com/openwisp/netjsonconfig/blob/master/netjsonconfig/backends/openvpn/schema.py>`_.

According to the `NetJSON <http://netjson.org>`_ spec, any unrecognized property will be ignored.

General settings (valid both for client and server)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Required properties:

* name
* mode
* proto
* dev

+--------------------------+---------+--------------+-------------------------------------------------------------+
| key name                 | type    | default      | allowed values                                              |
+==========================+=========+==============+=============================================================+
| ``name``                 | string  |              | 2 to 24 alphanumeric characters, dashes and underscores     |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``mode``                 | string  |              | ``p2p`` or ``server``                                       |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``proto``                | string  |              | ``udp``, ``tcp-client``, ``tcp-server``                     |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``port``                 | integer | ``1194``     | integers                                                    |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``dev_type``             | string  |              | ``tun``, ``tap``                                            |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``dev``                  | string  |              | any non-whitespace character (max length: 15)               |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``local``                | string  |              | any string                                                  |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``comp_lzo``             | string  | ``adaptive`` | ``yes``, ``no`` or ``adaptive``                             |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``auth``                 | string  | ``SHA1``     | see `auth property source code`_                            |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``cipher``               | string  | ``BF-CBC``   | see `cipher property source code`_                          |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``engine``               | string  |              | ``bsd``, ``rsax``, ``dynamic`` or empty string              |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``ca``                   | string  |              | any non whitespace character                                |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``cert``                 | string  |              | any non whitespace character                                |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``key``                  | string  |              | any non whitespace character                                |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``pkcs12``               | string  |              | any non whitespace character                                |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``ns_cert_type``         | string  |              | ``client``, ``server`` or empty string                      |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``mtu_disc``             | string  | ``no``       | ``no``, ``maybe`` or ``yes``                                |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``mtu_test``             | boolean | ``False``    |                                                             |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``fragment``             | integer | ``0``        | any positive integer                                        |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``mssfix``               | integer | ``1450``     | any positive integer                                        |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``keepalive``            | string  |              | two numbers separated by one space                          |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``persist_tun``          | boolean | ``False``    |                                                             |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``persist_key``          | boolean | ``False``    |                                                             |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``up``                   | string  |              | any non whitespace character                                |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``up_delay``             | integer | ``0``        | any positive integer                                        |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``down``                 | string  |              | any non whitespace character                                |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``script_security``      | integer | ``1``        | ``0``, ``1``, ``2``, ``3``                                  |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``user``                 | string  |              | any string                                                  |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``group``                | string  |              | any string                                                  |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``mute``                 | integer | ``0``        | any positive integer                                        |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``status``               | string  |              | string and number separated by space, eg:                   |
|                          |         |              | ``/var/log/openvpn.status 10``                              |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``status_version``       | integer | ``1``        | ``1``, ``2``, ``3``                                         |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``mute_replay_warnings`` | boolean | ``False``    |                                                             |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``secret``               | string  |              | any non whitespace character                                |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``reneg_sec``            | integer | ``3600``     | any positive integer                                        |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``tls_timeout``          | integer | ``2``        | any positive integer                                        |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``tls_cipher``           | string  |              | any string                                                  |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``remote_cert_tls``      | string  |              | ``client``, ``server`` or empty string                      |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``float``                | boolean | ``False``    |                                                             |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``fast_io``              | boolean | ``False``    |                                                             |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``log``                  | string  |              | filesystem path                                             |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``verb``                 | integer | ``1``        | from ``0`` (disabled) to ``11`` (very verbose)              |
+--------------------------+---------+--------------+-------------------------------------------------------------+

Client specific settings
~~~~~~~~~~~~~~~~~~~~~~~~

Required properties:

* remote

+--------------------------+---------+--------------+-------------------------------------------------------------+
| key name                 | type    | default      | allowed values                                              |
+==========================+=========+==============+=============================================================+
| ``remote``               | list    | ``[]``       | list of dictionaries containing ``host`` (str) and ``port`` |
|                          |         |              | (str). Must contain at least one element                    |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``nobind``               | boolean | ``True``     |                                                             |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``resolv_retry``         | boolean | ``True``     |                                                             |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``tls_client``           | boolean | ``True``     |                                                             |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``pull``                 | boolean | ``True``     |                                                             |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``remote_random``        | boolean | ``False``    |                                                             |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``auth_user_pass``       | string  |              | any non whitespace character                                |
+--------------------------+---------+--------------+-------------------------------------------------------------+
| ``auth_retry``           | string  | ``none``     | ``none``, ``nointeract`` or ``interact``                    |
+--------------------------+---------+--------------+-------------------------------------------------------------+

Server specific settings
~~~~~~~~~~~~~~~~~~~~~~~~

+------------------------------+---------+--------------+-------------------------------------------------------------+
| key name                     | type    | default      | allowed values                                              |
+==============================+=========+==============+=============================================================+
| ``tls_server``               | boolean | ``True``     |                                                             |
+------------------------------+---------+--------------+-------------------------------------------------------------+
| ``dh``                       | string  |              | any non whitespace character                                |
+------------------------------+---------+--------------+-------------------------------------------------------------+
| ``crl_verify``               | string  |              | any non whitespace character                                |
+------------------------------+---------+--------------+-------------------------------------------------------------+
| ``duplicate_cn``             | boolean | ``False``    |                                                             |
+------------------------------+---------+--------------+-------------------------------------------------------------+
| ``client_to_client``         | boolean | ``False``    |                                                             |
+------------------------------+---------+--------------+-------------------------------------------------------------+
| ``client_cert_not_required`` | boolean | ``False``    |                                                             |
+------------------------------+---------+--------------+-------------------------------------------------------------+
| ``username_as_common_name``  | boolean | ``False``    |                                                             |
+------------------------------+---------+--------------+-------------------------------------------------------------+
| ``auth_user_pass_verify``    | string  |              | any non whitespace character                                |
+------------------------------+---------+--------------+-------------------------------------------------------------+

Working around schema limitations
---------------------------------

The schema does not include all the possible OpenVPN settings, but it can render appropiately
any property not included in the schema as long as its type is one the following:

* boolean
* integer
* strings
* lists

For a list of all the OpenVPN configuration settings, refer to the `OpenVPN 2.3 manual
<https://community.openvpn.net/openvpn/wiki/Openvpn23ManPage>`_.

.. _auth property source code: https://github.com/openwisp/netjsonconfig/blob/master/netjsonconfig/backends/openvpn/schema.py#L79-L89
.. _cipher property source code: https://github.com/openwisp/netjsonconfig/blob/master/netjsonconfig/backends/openvpn/schema.py#L90-L103

Automatic generation of clients
-------------------------------

.. automethod:: netjsonconfig.OpenVpn.auto_client

Example:

.. code-block:: python

    from netjsonconfig import OpenVpn

    server_config = {
        "ca": "ca.pem",
        "cert": "cert.pem",
        "dev": "tap0",
        "dev_type": "tap",
        "dh": "dh.pem",
        "key": "key.pem",
        "mode": "server",
        "name": "example-vpn",
        "proto": "udp",
        "tls_server": True
    }
    dummy_contents = '------ EXAMPLE ------'
    client_config = OpenVpn.auto_client('vpn1.test.com',
                                        server=server_config,
                                        ca_path='ca.pem',
                                        ca_contents=dummy_contents,
                                        cert_path='cert.pem',
                                        cert_contents=dummy_contents,
                                        key_path='key.pem',
                                        key_contents=dummy_contents)
    client = OpenVpn(client_config)
    print(client.render())

Will be rendered as::

    # openvpn config: example-vpn

    ca ca.pem
    cert cert.pem
    dev tap0
    dev-type tap
    key key.pem
    mode p2p
    nobind
    proto udp
    remote vpn1.test.com 1195
    resolv-retry
    tls-client

    # ---------- files ---------- #

    # path: ca.pem
    # mode: 0644

    ------ EXAMPLE ------

    # path: cert.pem
    # mode: 0644

    ------ EXAMPLE ------

    # path: key.pem
    # mode: 0644

    ------ EXAMPLE ------
