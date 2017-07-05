====================
Command line utility
====================

.. include:: ../_github.rst

netjsonconfig ships a command line utility that can be
used from the interactive shell, bash scripts or other programming
languages.

Check out the available options yourself with::

    $ netjsonconfig --help
    usage: netjsonconfig [-h] [--config CONFIG]
                     [--templates [TEMPLATES [TEMPLATES ...]]]
                     [--native NATIVE] --backend {openwrt,openwisp,openvpn}
                     --method {render,generate,write,validate,json}
                     [--args [ARGS [ARGS ...]]] [--verbose] [--version]

    Converts a NetJSON DeviceConfiguration object to native router configurations.
    Exhaustive documentation is available at: http://netjsonconfig.openwisp.org/

    optional arguments:
      -h, --help            show this help message and exit

    input:
      --config CONFIG, -c CONFIG
                            config file or string, must be valid NetJSON
                            DeviceConfiguration
      --templates [TEMPLATES [TEMPLATES ...]], -t [TEMPLATES [TEMPLATES ...]]
                            list of template config files or strings separated by
                            space
      --native NATIVE, -n NATIVE
                            path to native configuration file or archive

    output:
      --backend {openwrt,openwisp,openvpn}, -b {openwrt,openwisp,openvpn}
                            Configuration backend
      --method {render,generate,write,validate,json}, -m {render,generate,write,validate,json}
                            Backend method to use. "render" returns the
                            configuration in text format; "generate" returns a
                            tar.gz archive as output; "write" is like generate but
                            writes to disk; "validate" validates the combination
                            of config and templates passed in input;
                            "json" returns NetJSON output:
      --args [ARGS [ARGS ...]], -a [ARGS [ARGS ...]]
                            Optional arguments that can be passed to methods

    debug:
      --verbose             verbose output
      --version, -v         show program's version number and exit

Here's the common use cases explained::

   # generate tar.gz from a NetJSON DeviceConfiguration object and save its output to a file
   netjsonconfig --config config.json --backend openwrt --method generate > config.tar.gz

   # convert an OpenWRT tar.gz to NetJSON and print to standard output (with 4 space indentation)
   netjsonconfig --native config.tar.gz --backend openwrt --method json -a indent="    "

   # use write configuration archive to disk in /tmp/routerA.tar.gz
   netjsonconfig --config config.json --backend openwrt --method write --args name=routerA path=/tmp/

   # see output of OpenWrt render method
   netjsonconfig --config config.json --backend openwrt --method render

   # same as previous but exclude additional files
   netjsonconfig --config config.json --backend openwrt --method render --args files=0

   # validate the config.json file against the openwrt backend
   netjsonconfig --config config.json --backend openwrt --method validate

   # abbreviated options
   netjsonconfig -c config.json -b openwrt -m render -a files=0

   # passing a JSON string instead of a file path
   netjsonconfig -c '{"general": { "hostname": "example" }}' -b openwrt -m render

Using templates::

    netjsonconfig -c config.json -t template1.json template2.json -b openwrt -m render

    # validate the result of merging config.json, template1.json and template2.json
    # against the openwrt backend schema
    netjsonconfig -c config.json -t template1.json template2.json -b openwrt -m validate

Environment variables
---------------------

*Environment variables* are automatically passed to the ``context`` argument (if you don't
know what this argument does please read ":ref:`context`"), therefore
you can reference environment variables inside *configurations* and *templates*::

    export HOSTNAME=freedom
    netjsonconfig -c '{"general": { "hostname": "{{ HOSTNAME }}" }}' -b openwrt -m render

You can also avoid using ``export`` and write everything in a one line command::

    PORT=2009; netjsonconfig -c config.json -t template1.json -b openwrt -m render
