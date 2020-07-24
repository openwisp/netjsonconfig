============
Contributing
============

.. include:: ../_github.rst

Thank you for taking the time to contribute to netjsonconfig.

Follow these guidelines to speed up the process.

.. contents:: **Table of Contents**:
   :backlinks: none
   :depth: 3

Reach out before you start
--------------------------

Before opening a new issue, try the following steps:

- look if somebody else has already started working on the same issue
  by looking in the `github issues <https://github.com/openwisp/netjsonconfig/issues>`_
  and `pull requests <https://github.com/openwisp/netjsonconfig/pulls>`_
- look also in the `OpenWISP mailing list <https://groups.google.com/d/forum/openwisp/join>`_
- announce your intentions by opening a new issue
- present yourself on the mailing list

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

Follow style conventions (PEP8, isort)
--------------------------------------

First of all, install the test requirements:

.. code-block:: shell

    workon netjsonconfig  # activate virtualenv
    pip install -r requirements-test.txt

Before committing your work check that your changes are not breaking the style conventions with:

.. code-block:: shell

    flake8
    isort --check-only --recursive .

For more information, please see:

- `PEP8: Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008/>`_
- `isort: a python utility / library to sort imports <https://github.com/timothycrosley/isort>`_

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
