Change log
==========

Version 0.3 [unreleased]
------------------------

- `#18 <https://github.com/openwisp/netjsonconfig/issues/18>`_ added ``OpenWisp`` backend
- `66ee96 <https://github.com/openwisp/netjsonconfig/commit/66ee96>`_ added file permission feature
- `#19 <https://github.com/openwisp/netjsonconfig/issues/19>`_ added sphinx documentation
  (published at `netjsonconfig.openwisp.org <http://netjsonconfig.openwisp.org>`_
- `30348e <https://github.com/openwisp/netjsonconfig/commit/30348e>`_ hardened ntp server option schema for ``OpenWrt`` backend
- `c31375 <https://github.com/openwisp/netjsonconfig/commit/c31375>`_ added madwifi to the allowed drivers in schema ``OpenWrt`` backend
- `#30 <https://github.com/openwisp/netjsonconfig/issues/30>`_ updated schema according to latest `NetJSON <http://netjson.org>`_ spec

Version 0.2 [2015-11-23]
------------------------

- `#20 <https://github.com/openwisp/netjsonconfig/issues/20>`_ added support for array of lines in files
- `#21 <https://github.com/openwisp/netjsonconfig/issues/21>`_ date is now correctly set in tar.gz files
- `82cc5e <https://github.com/openwisp/netjsonconfig/commit/82cc5e>`_ configuration archive is now compatible with ``sysupgrade -r``
- `#22 <https://github.com/openwisp/netjsonconfig/issues/22>`_ improved and simplified bridging
- `#23 <https://github.com/openwisp/netjsonconfig/issues/23>`_ do not ignore interfaces with no addresses
- `#24 <https://github.com/openwisp/netjsonconfig/issues/24>`_ restricted schema for interface names
- `#25 <https://github.com/openwisp/netjsonconfig/issues/25>`_ added support for logical interface names
- `#26 <https://github.com/openwisp/netjsonconfig/issues/26>`_ ``merge_dict`` now returns a copy of all the elements
- `d22d59 <https://github.com/openwisp/netjsonconfig/commit/d22d59>`_ restricted SSID to 32 characters
- `#27 <https://github.com/openwisp/netjsonconfig/issues/27>`_ improved wireless definition
- `#28 <https://github.com/openwisp/netjsonconfig/issues/28>`_ removed "enabled" in favour of "disabled"

Version 0.1 [2015-10-20]
------------------------

- Added ``OpenWrt`` Backend
- Added command line utility ``netjsonconfig``
- Added multiple templating feature
- Added file inclusion feature
