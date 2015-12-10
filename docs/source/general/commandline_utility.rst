====================
Command line utility
====================

netjsonconfig ships a command line utility that can be
used from the interactive shell, bash scripts or even other programming
languages (via system calls).

Check out the available options yourself with::

    $ netjsonconfig --help
    usage: netjsonconfig [-h] [--templates [TEMPLATES [TEMPLATES ...]]]
                         [--backend {openwrt,openwisp}]
                         [--method {generate,render}] [--verbose] [--version]
                         config

    Converts a NetJSON DeviceConfiguration objectto working router configurations.

    positional arguments:
      config                config file or string, must be valid NetJSON
                            DeviceConfiguration

    optional arguments:
      -h, --help            show this help message and exit
      --templates [TEMPLATES [TEMPLATES ...]], -t [TEMPLATES [TEMPLATES ...]]
                            list of template config files or strings separated by
                            space
      --backend {openwrt,openwisp}, -b {openwrt,openwisp}
                            Configuration backend: openwrt or openwisp
      --method {generate,render}, -m {generate,render}
                            Backend method to use. "generate" returns a tar.gz
                            archive as output; "render" returns the configuration
                            in text format
      --verbose             verbose output
      --version, -v         show program's version number and exit

Here's the common use cases explained::

   # generate tar.gz from a NetJSON DeviceConfiguration object and save it to a file
   netjsonconfig --backend openwrt --method generate config.json > config.tar.gz

   # see output of OpenWrt render method
   netjsonconfig --backend openwrt --method render config.json

   # abbreviated options
   netjsonconfig -b openwrt -m render config.json

   # passing a JSON string instead of a file path
   netjsonconfig -b openwrt -m render '{"general": { "hostname": "example" }}'

Using templates::

    netjsonconfig config.json -t template1.json template2.json -b openwrt -m render
