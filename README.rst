netconfig-gen
=============

.. image:: https://travis-ci.org/openwisp/netconfig-gen.png
   :target: https://travis-ci.org/openwisp/netconfig-gen

.. image:: https://coveralls.io/repos/openwisp/netconfig-gen/badge.png
  :target: https://coveralls.io/r/openwisp/netconfig-gen

.. image:: https://landscape.io/github/openwisp/netconfig-gen/master/landscape.png
   :target: https://landscape.io/github/openwisp/netconfig-gen/master
   :alt: Code Health

.. image:: https://requires.io/github/openwisp/netconfig-gen/requirements.png?branch=master
   :target: https://requires.io/github/openwisp/netconfig-gen/requirements/?branch=master
   :alt: Requirements Status

.. image:: https://badge.fury.io/py/netconfig-gen.png
   :target: http://badge.fury.io/py/netconfig-gen

.. image:: https://img.shields.io/pypi/dm/netconfig-gen.svg
   :target: https://pypi.python.org/pypi/netconfig-gen

------------

TODO

Install stable version from pypi
--------------------------------

Install from pypi:

.. code-block:: shell

    pip install netconfig-gen

Install development version
---------------------------

Install tarball:

.. code-block:: shell

    pip install https://github.com/openwisp/netconfig-gen/tarball/master

Alternatively you can install via pip using git:

.. code-block:: shell

    pip install -e git+git://github.com/openwisp/netconfig-gen#egg=netconfig_gen

If you want to contribute, install your cloned fork:

.. code-block:: shell

    git clone git@github.com:<your_fork>/netconfig-gen.git
    cd netconfig-gen
    python setup.py develop

Basic Usage Example
-------------------

TODO

.. code-block:: python

    from netconfig_gen import TODO

Running tests
-------------

Install your forked repo:

.. code-block:: shell

    git clone git://github.com/<your_fork>/netconfig-gen
    cd netconfig-gen/
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

    coverage run --source=netconfig_gen runtests.py && coverage report

Contributing
------------

1. Join the `ninux-dev mailing list`_
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
