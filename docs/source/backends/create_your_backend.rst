===================
Create your backend
===================

.. include:: ../_github.rst

Every backend is based on the common ground of some elements provided by the 
netjsonconfig library. The ``BaseBackend``, ``BaseConverter``, ``BaseParser`` and
``BaseRenderer`` are a battle proven set of tools that can be extended when
creating you backend.

But the netjsonconfig package is not a playground to experiment, your contributions
to a new backend should start elsewhere, a different package, where you are in control
and can make errors and experiment more.

Netjsonconfig can now discover packages that provides a custom backend using
a feature available in the Python packaging ecosystem which is called `entry_points`.

To create a new backend start from scratch with a new folder and add this file to your
project root directory.

.. code-block:: python

    # example_backend/setup.py
    from setuptools import setup, find_packages
    
    setup(
        name='example_backend',
        version='0.0.0',
        description='an example to illustrate a netjsonconfig backend as an external module',
        install_requires=['netjsonconfig>=0.6.3'],
        packages=find_packages(),
        entry_points={
            'netjsonconfig.backends': [
                'example=example_backend.__init__:ExampleBackend',
            ]
        }
    )

this file can be used to create a package that can be installed using pip or other tools
in the python ecosystem. You can find more information about Python packaging
`at packaging.python.org <https://packaging.python.org/>`_
and `at the hitchhikers guide to packaging <https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/>`_.

The most important part is to give your package a good name, a well thought description and
to add the ``entry_points`` keyword argument with the following code

..  code-block:: python

        {
                # this is used by netjsonconfig
                # to find your backend
                'netjsonconfig.backends': [
                        ...
                ]
        }

Now your package will be in the list of backends that netjsonconfig can use!

But we still have to give us a name to be unique! Netjsonconfig already
defined the names ``openwisp``, ``openwrt`` and ``openvpn`` but you can choose
whatever you like most.

The name ``netjsonconfig.backends`` will be associated with a list of classes
from your package that will be presented to netjconfig at runtime. To specify
which classes you want to expose write the triple ``name``, ``path`` and ``class_name``
using the format ``name=path:class_name`` as in the example below.

The ``path`` part is simply the path to the file that contains the class
you want to expose and the ``class_name`` is the name of the class.

..  code-block:: python

        {
                'netjsonconfig.backends': [
                        # name=path:class_name
                        'example=example_backend.__init__:ExampleBackend',
                ]
        }

The previous example can be used with the following class definition

.. code-block:: python

        # example_backend/example_backend/__init__.py
        from netjsonconfig.backends.base.backend import BaseBackend
        from netjsonconfig.backends.base.renderer import BaseRenderer
        from netjsonconfig.backends.base.parser import BaseParser
        
        from netjsonconfig.schema import schema as default_schema
        
        class ExampleBackend(BaseBackend):
            schema = default_schema
            converter = []
            parser = BaseParser
            renderer = BaseRenderer

Once you have your python package configured with the correct entry points
you should have a directory tree that looks like this.

.. code-block:: bash

    $ tree example_backend
    example_backend
    ├── example_backend
    │   └── __init__.py
    └── setup.py

And now you can install your package using ``pip install -e ./example_backend``
or ``python setup.py install``.

As ``netjsonconfig`` is a dependency for ``example_backend`` you can use your backend
directly from the command line, e.g.

.. code-block:: bash

    $ netjsonconfig
    usage: netjsonconfig [-h] [--config CONFIG]
                     [--templates [TEMPLATES [TEMPLATES ...]]]
                     [--native NATIVE] --backend
                     {openwrt,openwisp,openvpn,example} --method
                     {render,generate,write,validate,json}
                     [--args [ARGS [ARGS ...]]] [--verbose] [--version]
    netjsonconfig: error: the following arguments are required: --backend/-b, --method/-m

Notice the *example* in ``{openwrt,openwisp,openvpn,example}``? That's your backend!

The name exposed is the one chosen in the *name*, *path*, *class* triple
from before

.. code-block:: python

        # name=path:class
        'example=example_backend.__init__:ExampleBackend',
