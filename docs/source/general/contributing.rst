============
Contributing
============

We welcome contributions and feedback!

If you intend to contribute in any way please keep the following guidelines in mind:

1. Announce your intentions in the `OpenWISP Mailing List <https://groups.google.com/d/forum/openwisp>`_
2. :ref:`install_git_fork_for_contributing`
3. Follow `PEP8, Style Guide for Python Code <http://www.python.org/dev/peps/pep-0008/>`_
4. Write code
5. Write tests for your code
6. Ensure all tests pass
7. Ensure test coverage does not decrease
8. Document your changes
9. Send pull request


Virtual Environment
-------------------

Please use a virtual environment while developing your feature, it keeps everybody on the same page and it helps reproducing bugs and resolving problems.

.. code-block:: shell

    virtualenv env
    source env/bin/activate
    python setup.py develop

.. note::

    Another choice is using ``virtualenvwrapper``, they are equivalent tools but ``virtualenvwrapper`` is nicer to use

Style guide enforcement
-----------------------

Install ``flake8`` and ``isort`` to check for common pitfalls that may have your contribution stopped, they are listed in ``requirements-test.txt`` with the other testing requirements

.. code-block:: shell

    source env/bin/activate
    pip install -r requirements-test.txt

Before committing your work and opening a pull request run this to check

.. code-block:: shell

    ./runflake8 && ./runisort

.. note::
    To speed things up you can add your virtual environment directory to the list of the excluded directories in the ``runflake8`` script

Building documentation
----------------------

To build the documentation for this project please install sphinx inside the virtual environment

.. code-block:: shell

    source env/bin/activate
    pip install sphinx
    cd doc && make html

.. raw:: html

    <p>
        <iframe src="https://nodeshot.org/github-btn.html?user=openwisp&amp;repo=netjsonconfig&amp;type=watch&amp;count=true&amp;size=large" frameborder="0" scrolling="0" width="120" height="33"></iframe>
        <iframe src="https://nodeshot.org/github-btn.html?user=openwisp&amp;repo=netjsonconfig&amp;type=fork&amp;count=true&amp;size=large" frameborder="0" scrolling="0" width="120" height="33"></iframe>
    </p>
