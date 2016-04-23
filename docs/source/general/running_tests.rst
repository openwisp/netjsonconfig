=============
Running tests
=============

.. raw:: html

    <p>
        <iframe src="https://nodeshot.org/github-btn.html?user=openwisp&amp;repo=netjsonconfig&amp;type=watch&amp;count=true&amp;size=large" frameborder="0" scrolling="0" width="120" height="33"></iframe>
        <iframe src="https://nodeshot.org/github-btn.html?user=openwisp&amp;repo=netjsonconfig&amp;type=fork&amp;count=true&amp;size=large" frameborder="0" scrolling="0" width="120" height="33"></iframe>
    </p>

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

Using nose
----------

Alternatively, you can use the ``nose`` tool (which has a ton of available options):

.. code-block:: shell

    nosetests

See test coverage with:

.. code-block:: shell

    coverage run --source=netjsonconfig runtests.py && coverage report
