============
Contributing
============

.. include:: ../_github.rst

Thank you for taking the time to contribute to netjsonconfig.

Follow these guidelines to speed up the process.

.. contents:: **Table of Contents**:
   :backlinks: none
   :depth: 3

General contributing guidelines of OpenWISP
-------------------------------------------

We highly recommend reading the general
`OpenWISP Contributing Guidelines <https://openwisp.io/docs/developer/contributing.html>`_
to find out the conventions we use to maintain consistency and quality standards
across the different OpenWISP modules.

Create a virtual environment
----------------------------

Please use a `python virtual environment <https://docs.python.org/3/library/venv.html>`_ while
developing your feature, it keeps everybody on the same page and it helps reproducing bugs
and resolving problems.

We suggest you to use `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io>`_ for this task
(consult install instructions in the virtualenvwrapper docs).

.. code-block:: shell

    mkvirtualenv netjsonconfig  # create virtualenv

.. _install_fork:

Fork repo and install your fork
-------------------------------

Once you have forked this repository to your own github account or organization,
install your own fork in your development environment:

.. code-block:: shell

    git clone git@github.com:<your_fork>/netjsonconfig.git
    cd netjsonconfig
    workon netjsonconfig  # activate virtualenv
    python setup.py develop

Ensure test coverage does not decrease
--------------------------------------

First of all, install the test requirements:

.. code-block:: shell

    workon netjsonconfig  # activate virtualenv
    pip install -r requirements-test.txt

When you introduce changes, ensure test coverage is not decreased with:

.. code-block:: shell

    nose2 --with-coverage --coverage netjsonconfig

Follow the coding style conventions and run the QA checks
---------------------------------------------------------

First of all, install the test requirements:

.. code-block:: shell

    workon netjsonconfig  # activate virtualenv
    pip install -r requirements-test.txt

Before committing your work, run ``openwisp-qa-format`` to format the code according
to our `python code conventions <https://openwisp.io/docs/developer/contributing.html#python-code-conventions>`_:

.. code-block:: shell

    openwisp-qa-format

Then, you can run the QA checks with:

.. code-block:: shell

    ./run-qa-checks

Update the documentation
------------------------

If you introduce new features or change existing documented behavior,
please remember to update the documentation!

The documentation is located in the ``/docs`` directory
of the repository.

To do work on the docs, proceed with the following steps:

.. code-block:: shell

    workon netjsonconfig  # activate virtualenv
    pip install sphinx
    cd docs
    make html

Send pull request
-----------------

Now is time to push your changes to github and open a `pull request
<https://github.com/openwisp/netjsonconfig/pulls>`_!
