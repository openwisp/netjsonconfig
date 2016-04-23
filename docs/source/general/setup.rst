=====
Setup
=====

.. raw:: html

    <p>
        <iframe src="https://nodeshot.org/github-btn.html?user=openwisp&amp;repo=netjsonconfig&amp;type=watch&amp;count=true&amp;size=large" frameborder="0" scrolling="0" width="120" height="33"></iframe>
        <iframe src="https://nodeshot.org/github-btn.html?user=openwisp&amp;repo=netjsonconfig&amp;type=fork&amp;count=true&amp;size=large" frameborder="0" scrolling="0" width="120" height="33"></iframe>
    </p>

Install stable version from pypi
--------------------------------

The easiest way to install *netjsonconfig* is via the `python package index <https://pypi.python.org/>`_:

.. code-block:: shell

    pip install netjsonconfig

Install development version
---------------------------

If you need to test the latest development version you can do it in two ways;

The first option is to install a tarball:

.. code-block:: shell

    pip install https://github.com/openwisp/netjsonconfig/tarball/master

The second option is to install via pip using git
(this will automatically clone the repo and store it on your hard dirve):

.. code-block:: shell

    pip install -e git+git://github.com/openwisp/netjsonconfig#egg=netjsonconfig

.. _install_git_fork_for_contributing:

Install git fork for contributing
---------------------------------

If you want to contribute, we suggest to install your cloned fork:

.. code-block:: shell

    git clone git@github.com:<your_fork>/netjsonconfig.git
    cd netjsonconfig
    python setup.py develop
