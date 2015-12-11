====================
Command line utility
====================

netjsonconfig ships a command line utility that can be
used from the interactive shell, bash scripts or even other programming
languages (via system calls).

Check out the available options yourself with::

    $ netjsonconfig --help
    usage: netjsonconfig [-h] --config CONFIG
                         [--templates [TEMPLATES [TEMPLATES ...]]] --backend
                         {openwrt,openwisp} --method {render,generate,write}
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

    output:
      --backend {openwrt,openwisp}, -b {openwrt,openwisp}
                            Configuration backend: openwrt or openwisp
      --method {render,generate,write}, -m {render,generate,write}
                            Backend method to use. "render" returns the
                            configuration in text format"generate" returns a
                            tar.gz archive as output; "write" is like generate but
                            writes to disk;
      --args [ARGS [ARGS ...]], -a [ARGS [ARGS ...]]
                            Optional arguments that can be passed to methods

    debug:
      --verbose             verbose output
      --version, -v         show program's version number and exit


Here's the common use cases explained::

   # generate tar.gz from a NetJSON DeviceConfiguration object and save its output to a file
   netjsonconfig --config config.json --backend openwrt --method generate > config.tar.gz

   # use write configuration archive to disk in /tmp/routerA.tar.gz
   netjsonconfig --config config.json --backend openwrt --method write --args name=routerA path=/tmp/

   # see output of OpenWrt render method
   netjsonconfig --config config.json --backend openwrt --method render

   # same as previous but exclude additional files
   netjsonconfig --config config.json --backend openwrt --method render --args files=0

   # abbreviated options
   netjsonconfig -c config.json -b openwrt -m render -a files=0

   # passing a JSON string instead of a file path
   netjsonconfig -c '{"general": { "hostname": "example" }}' -b openwrt -m render

Using templates::

    netjsonconfig -c config.json -t template1.json template2.json -b openwrt -m render
