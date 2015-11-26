====================
Command line utility
====================

netjsonconfig ships a command line utility that can be
used from the interactive shell, bash scripts or even other programming
languages (via system calls).

Check out the available options yourself with::

   netjsonconfig --help

Here's the common use cases explained::

   # generate tar.gz from a NetJSON DeviceConfiguration object
   netjsonconfig --backend openwrt config.json

   # see output of OpenWrt render method
   netjsonconfig --backend openwrt --method render config.json

   # abbreviated options
   netjsonconfig -b openwrt -m render config.json

   # passing a JSON string instead of a file path
   netjsonconfig -b openwrt -m render '{"general": { "hostname": "example" }}'

Using templates::

    netjsonconfig config.json -t template1.json template2.json -b openwrt -m render
