netjsonconfig
=============

.. image:: https://travis-ci.org/openwisp/netjsonconfig.svg
   :target: https://travis-ci.org/openwisp/netjsonconfig

.. image:: https://coveralls.io/repos/openwisp/netjsonconfig/badge.svg
  :target: https://coveralls.io/r/openwisp/netjsonconfig

.. image:: https://requires.io/github/openwisp/netjsonconfig/requirements.svg?branch=master
   :target: https://requires.io/github/openwisp/netjsonconfig/requirements/?branch=master
   :alt: Requirements Status

.. image:: https://badge.fury.io/py/netjsonconfig.svg
   :target: http://badge.fury.io/py/netjsonconfig

.. image:: https://img.shields.io/pypi/dm/netjsonconfig.svg
   :target: https://pypi.python.org/pypi/netjsonconfig

------------

Converts `NetJSON <http://netjson.org>`__ DeviceConfiguration objects to real router configurations.

**Currently we are working only on OpenWrt support**.

**Work in progress**.

Install stable version from pypi
--------------------------------

Install from pypi:

.. code-block:: shell

    pip install netjsonconfig

Install development version
---------------------------

Install tarball:

.. code-block:: shell

    pip install https://github.com/openwisp/netjsonconfig/tarball/master

Alternatively you can install via pip using git:

.. code-block:: shell

    pip install -e git+git://github.com/openwisp/netjsonconfig#egg=netjsonconfig

If you want to contribute, install your cloned fork:

.. code-block:: shell

    git clone git@github.com:<your_fork>/netjsonconfig.git
    cd netjsonconfig
    python setup.py develop

Basic Usage Example
-------------------

.. code-block:: python

    from netjsonconfig import OpenWrt

    o = OpenWrt({
        "type": "DeviceConfiguration",
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

Command line utility
--------------------

netjsonconfig ships a command line utility that can be
used from the interactive shell or in bash scripts::

   netjsonconfig --help

A few common use scenarios::

   # generate tar.gz from a NetJSON DeviceConfiguration object
   netjsonconfig --backend openwrt config.json

   # see output of OpenWrt render method
   netjsonconfig --backend openwrt --method render config.json
   
   # abbreviated options
   netjsonconfig -b openwrt -m render config.json

Running tests
-------------

Install your forked repo:

.. code-block:: shell

    git clone git://github.com/<your_fork>/netjsonconfig
    cd netjsonconfig/
    python setup.py develop

Install test requirements:

.. code-block:: shell

    pip install -r requirements-test.txt

Run tests with:

.. code-block:: shell

    ./runtests.py

Alternatively, you can use the ``nose`` command (which has a ton of available options):

.. code-block:: shell

    nosetests

See test coverage with:

.. code-block:: shell

    coverage run --source=netjsonconfig runtests.py && coverage report

Contributing
------------

1. Announce your intentions in the `issue tracker <https://github.com/openwisp/netjsonconfig/issues>`__
2. Fork this repo and install it
3. Follow `PEP8, Style Guide for Python Code`_
4. Write code
5. Write tests for your code
6. Ensure all tests pass
7. Ensure test coverage is not under 90%
8. Document your changes
9. Send pull request

.. _PEP8, Style Guide for Python Code: http://www.python.org/dev/peps/pep-0008/
.. _ninux-dev mailing list: http://ml.ninux.org/mailman/listinfo/ninux-dev
