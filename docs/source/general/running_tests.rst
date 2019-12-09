=============
Running tests
=============

.. include:: ../_github.rst

Running the test suite is really straightforward!

Using runtests.py
-----------------

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

Using nose2
-----------

Alternatively, you can use the ``nose2`` tool (which has a ton of available options):

.. code-block:: shell

    nose2

See test coverage with:

.. code-block:: shell

    coverage run --source=netjsonconfig runtests.py && coverage report
