====================
Command line utility
====================

netjsonconfig ships a command line utility that can be
used from the interactive shell, bash scripts or even other programming
languages (via system calls).

Check out the available options yourself with::

    $ netjsonconfig --help
    usage: netjsonconfig [-h] [--config CONFIG]
                         [--templates [TEMPLATES [TEMPLATES ...]]]
                         [--backend {openwrt,openwisp}]
                         [--method {render,generate}] [--verbose] [--version]

    Converts a NetJSON DeviceConfiguration object to native router configurations.

    optional arguments:
      -h, --help            show this help message and exit

    input:
      --config CONFIG, -c CONFIG
                            config file or string, must be valid NetJSON
                            DeviceConfiguration
      --templates [TEMPLATES [TEMPLATES ...]], -t [TEMPLATES [TEMPLATES ...]]
                            list of template config files or strings separated by
                            space

    output:
      --backend {openwrt,openwisp}, -b {openwrt,openwisp}
                            Configuration backend: openwrt or openwisp
      --method {render,generate}, -m {render,generate}
                            Backend method to use. "render" returns the
                            configuration in text format"generate" returns a
                            tar.gz archive as output;

    debug:
      --verbose             verbose output
      --version, -v         show program's version number and exit

Here's the common use cases explained::

   # generate tar.gz from a NetJSON DeviceConfiguration object and save it to a file
   netjsonconfig --config config.json --backend openwrt --method generate > config.tar.gz

   # see output of OpenWrt render method
   netjsonconfig --config config.json --backend openwrt --method render

   # abbreviated options
   netjsonconfig -c config.json -b openwrt -m render

   # passing a JSON string instead of a file path
   netjsonconfig -c '{"general": { "hostname": "example" }}' -b openwrt -m render

Using templates::

    netjsonconfig -c config.json -t template1.json template2.json -b openwrt -m render
