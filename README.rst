netjsonconfig
=============

.. image:: https://travis-ci.org/openwisp/netjsonconfig.png
   :target: https://travis-ci.org/openwisp/netjsonconfig

.. image:: https://coveralls.io/repos/openwisp/netjsonconfig/badge.png
  :target: https://coveralls.io/r/openwisp/netjsonconfig

.. image:: https://landscape.io/github/openwisp/netjsonconfig/master/landscape.png
   :target: https://landscape.io/github/openwisp/netjsonconfig/master
   :alt: Code Health

.. image:: https://requires.io/github/openwisp/netjsonconfig/requirements.png?branch=master
   :target: https://requires.io/github/openwisp/netjsonconfig/requirements/?branch=master
   :alt: Requirements Status

.. image:: https://badge.fury.io/py/netjsonconfig.png
   :target: http://badge.fury.io/py/netjsonconfig

.. image:: https://img.shields.io/pypi/dm/netjsonconfig.svg
   :target: https://pypi.python.org/pypi/netjsonconfig

------------

TODO

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

TODO

.. code-block:: python

    from netjsonconfig import TODO

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
