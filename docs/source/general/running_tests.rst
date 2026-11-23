Running tests
=============

Running the test suite is really straightforward!

Using runtests
--------------

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

    ./runtests

Using nose2
-----------

Alternatively, you can use the ``nose2`` tool (which has a ton of
available options):

.. code-block:: shell

    nose2

Run specific test files:

.. code-block:: shell

    # runs tests.openwrt.test_network
    nose2 -s tests/openwrt/ -v test_network

    # alternative way
    ./runtests tests.openwrt.test_backend.TestBackend

The entry point accepts test module, class, and method labels under
``tests``. The supported flags are ``-v``, ``-q``, ``-F``, ``--verbose``,
``--quiet``, and ``--fail-fast``. Argument validation does not sandbox the
test code or project configuration.

See test coverage with:

.. code-block:: shell

    coverage run --source=netjsonconfig ./runtests && coverage report
