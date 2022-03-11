Change log
==========

Version 0.9.1 [2020-02-15]
--------------------------

- [fix] Removed ``mtu_disc`` from ``auto_client`` method because it causes
  issues on most OpenWRT systems
- [fix] Avoided maxLength on PIN property to allow configuration variables
- [change] Add missing TLS ciphers to OpenVPN

Version 0.9.0 [2020-11-18]
--------------------------

- [change] **Potentially backward incompatible**:
  added support for dialup interfaces (ppp, pppoe, pppoa,
  3g, qmi, ncm, wwan, pptp, 6in4, aiccu or l2tp) to openwrt backend.
  This change is backward incompatible if the same type of configuration
  was achieved using a workaround, in these cases the configuration
  will have to be upgraded to use the new format.
- [feature] Added support for modem manager interfaces

Version 0.8.2 [2020-08-17]
--------------------------

- [fix] Fixed bug in OpenWRT backend validation for ip_rules/src

Version 0.8.1 [2020-05-28]
--------------------------

- Fixed bug that prevented overriding the contents of a file present
  in a template and caused the file to be duplicated instead of overwritten
- Fixed bug affecting backward conversion of switch VLAN on OpenWRT

Version 0.8.0 [2020-04-03]
--------------------------

- Changed default file mode for certificate files generated with
  from ``0644`` to ``0600``

Version 0.7.0 [2020-01-14]
--------------------------

- Dropped support for python 2.7
- Updated github buttons in documentation which were causing an unintended redirect
- Updated the jsonschema library to version 3.x

Version 0.6.4 [2019-12-09]
--------------------------

- `#113 <https://github.com/openwisp/netjsonconfig/issues/113>`_:
  [bugfix] Made "encryption none" explicit in OpenWRT
- `5ddc201 <https://github.com/openwisp/netjsonconfig/commit/5ddc201>`_:
  [bugfix] Fixed invalid UCI name bug in default OpenWRT renderer
- `#118 <https://github.com/openwisp/netjsonconfig/issues/118>`_:
  [bugfix] Fixed ``TypeError: can only concatenate list (not "str") to list``
- `#137 <https://github.com/openwisp/netjsonconfig/issues/137>`_:
  [tests] Migrated tests to nose2

Version 0.6.3 [2018-07-09]
--------------------------

- `#106 <https://github.com/openwisp/netjsonconfig/pull/106>`_
  [extensions] Query backends from installed packages
  (thanks to `@EdoPut <https://github.com/EdoPut>`_)
- `#109 <https://github.com/openwisp/netjsonconfig/pull/109>`_
  [doc] Added reference to plugin interface
  (thanks to `@EdoPut <https://github.com/EdoPut>`_)
- `#99 <https://github.com/openwisp/netjsonconfig/pull/99>`_
  [cli] print traceback fully if the verbose flag is passed
  (thanks to `@EdoPut <https://github.com/EdoPut>`_)
- `#108 <https://github.com/openwisp/netjsonconfig/pull/108>`_
  [openvpn] Added more options to the OpenVPN backend
  (thanks to `@okraits <https://github.com/okraits>`_)

Version 0.6.2 [2017-08-29]
--------------------------

- `#78 <https://github.com/openwisp/netjsonconfig/issues/78>`_
  [base] Added support for multiple renderers
- `#94 <https://github.com/openwisp/netjsonconfig/issues/94>`_
  [schema] Made ``bssid`` not required for wireless stations
- `#97 <https://github.com/openwisp/netjsonconfig/issues/97>`_
  [python2] Fixed ``py2-ipaddress`` related unicode bug

Version 0.6.1 [2017-07-05]
--------------------------

- `5ddc201 <https://github.com/openwisp/netjsonconfig/commit/5ddc201>`_:
  [general] Avoid default mutable arguments
- `dde3c9b <https://github.com/openwisp/netjsonconfig/commit/dde3c9b>`_:
  [openvpn] Added explicit ``list_identifiers`` attribute
- `8c26cd6 <https://github.com/openwisp/netjsonconfig/commit/8c26cd6>`_:
  [docs] Updated outdated OpenWRT rendering examples
- `5f8483e <https://github.com/openwisp/netjsonconfig/commit/5f8483e>`_:
  [openwrt] Fixed repeated bridge gateway case
- `#84 <https://github.com/openwisp/netjsonconfig/pull/84>`_
  [exceptions] Improved validation errors
  (thanks to `@EdoPut <https://github.com/EdoPut>`_)
- `#85 <https://github.com/openwisp/netjsonconfig/issues/85>`_
  [openwrt] Added "vid" option in "switch"
- `#86 <https://github.com/openwisp/netjsonconfig/issues/86>`_
  [openwrt] Added support for "ip6gw" option
- `#70 <https://github.com/openwisp/netjsonconfig/pull/70>`_
  [feature] Backward conversion
- `#87 <https://github.com/openwisp/netjsonconfig/issues/87>`_
  [openwrt] Removed automatic timezone

Version 0.6.0 [2017-06-01]
--------------------------

- `#70 <https://github.com/openwisp/netjsonconfig/pull/70>`_
  [general] Preliminary work for backward conversion, more info in the `OpenWISP Mailing List
  <https://groups.google.com/d/msg/openwisp/9FOhrfykwTY/tyRjqUoFAwAJ>`_
- `#58 <https://github.com/openwisp/netjsonconfig/pull/58>`_:
  [openwrt] Dropped obsolete code in ``OpenVpn`` converter
- `#59 <https://github.com/openwisp/netjsonconfig/pull/59>`_:
  [openwrt] Improved multiple ip address output

Version 0.5.6 [2017-05-24]
--------------------------

- `#69 <https://github.com/openwisp/netjsonconfig/pull/69>`_:
  [docs] Improved contributing guidelines
  (thanks to `@EdoPut <https://github.com/EdoPut>`_)
- `#71 <https://github.com/openwisp/netjsonconfig/pull/71>`_:
  [bin] Added ``validate`` to available methods of command line tool
  (thanks to `@EdoPut <https://github.com/EdoPut>`_)
- `845ed83 <https://github.com/openwisp/netjsonconfig/commit/845ed83>`_:
  [version] Improved get_version to follow PEP440
- `#73 <https://github.com/openwisp/netjsonconfig/pull/73>`_:
  [netjson] Fixed compatibility with `NetJSON <http://netjson.org>`_ specification

Version 0.5.5.post1 [2017-04-18]
--------------------------------

- `d481781 <https://github.com/openwisp/netjsonconfig/commit/d481781>`_:
  [docs] Added OpenWRT PPPoE example
- `beb435b <https://github.com/openwisp/netjsonconfig/commit/beb435b>`_:
  [docs] Fixed Basic Concepts summary

Version 0.5.5 [2017-03-15]
--------------------------

- `#65 <https://github.com/openwisp/netjsonconfig/pull/65>`_: [openwrt] Added missing zonename attribute

Version 0.5.4.post1 [2017-03-07]
--------------------------------

- `4aaecae <https://github.com/openwisp/netjsonconfig/commit/4aaecae>`_:
  [docs] Added documentation regarding template overrides

Version 0.5.4 [2017-02-14]
--------------------------

- `6f712d1 <https://github.com/openwisp/netjsonconfig/commit/6f712d1>`_:
  [utils] Implemented identifiers as parameters in ``utils.merge_list``
- `fcae96c <https://github.com/openwisp/netjsonconfig/commit/fcae96c>`_:
  [openwrt] Added ``config_value`` identifier in ``utils.merge_list``
- `eaa04de <https://github.com/openwisp/netjsonconfig/commit/eaa04de>`_:
  [docs] Improved `"All the other settings"
  <http://netjsonconfig.openwisp.org/en/stable/backends/openwrt.html#all-the-other-settings>`_
  section in ``OpenWrt`` backend
- `#60 <https://github.com/openwisp/netjsonconfig/issues/60>`_ [openvpn] Fixed ``resolv_retry`` bug;
  **minor backward incompatible change**: handled in `django-netjsonconfig with a migration
  <https://github.com/openwisp/django-netjsonconfig/commit/f16768d3e9031197a71cd988c0643f88a4badbd7>`_
- `f25e77e <https://github.com/openwisp/netjsonconfig/commit/f25e77e>`_:
  [openvpn] Added ``topology`` attribute to schema
- `c4aa07a <https://github.com/openwisp/netjsonconfig/commit/c4aa07a>`_:
  [openvpn] Allow to omit seconds in status attribute

Version 0.5.3 [2017-01-17]
--------------------------

- `#56 <https://github.com/openwisp/netjsonconfig/issues/56>`_: [general] Implemented smarter merge mechanism
- `#57 <https://github.com/openwisp/netjsonconfig/issues/57>`_: [openwrt] Fixed interface ``enabled`` bug
- `7a152a3 <https://github.com/openwisp/netjsonconfig/commit/7a152a3>`_: [openwrt] Renamed ``enabled`` to ``disabled`` in OpenVPN section (for consistency)

Version 0.5.2 [2016-12-29]
--------------------------

- `#55 <https://github.com/openwisp/netjsonconfig/issues/55>`_: [vars] Fixed broken evaluation of multiple variables

Version 0.5.1 [2016-09-22]
--------------------------

- `b486c4d <https://github.com/openwisp/netjsonconfig/commit/b486c4d>`_: [openvpn] corrected wrong ``client`` mode, renamed to ``p2p``
- `c7e51c6 <https://github.com/openwisp/netjsonconfig/commit/c7e51c6>`_: [openvpn] added ``pull`` option for clients
- `dde3128 <https://github.com/openwisp/netjsonconfig/commit/dde3128>`_: [openvpn] differentiate server between manual, routed and bridged

Version 0.5.0 [2016-09-19]
--------------------------

- added ``OpenVpn`` backend
- `afbc3a3 <https://github.com/openwisp/netjsonconfig/commit/afbc3a3>`_: [openwisp] fixed openvpn integration (partially backward incompatible)
- `1234c34 <https://github.com/openwisp/netjsonconfig/commit/1234c34>`_: [context] improved flexibility of configuration variables
- `#54 <https://github.com/openwisp/netjsonconfig/issues/54>`_: [openwrt] fixed netmask issue on ipv4

Version 0.4.5 [2016-09-05]
--------------------------

- `#53 <https://github.com/openwisp/netjsonconfig/issues/53>`_: [docs] avoid ambiguity on dashes in context
- `#52 <https://github.com/openwisp/netjsonconfig/pull/52>`_: [schema] added countries list as ``enum``
  for radios (thanks to `@zachantre <https://github.com/zachantre>`_)

Version 0.4.4 [2016-06-27]
--------------------------

- `#50 <https://github.com/openwisp/netjsonconfig/issues/50>`_: [openwrt] add logical name to all generated configuration items

Version 0.4.3 [2016-04-23]
--------------------------

- `c588e5d <https://github.com/openwisp/netjsonconfig/commit/c588e5d>`_: [openwrt] avoid adding ``dns`` and ``dns_search`` if ``proto`` is ``none``

Version 0.4.2 [2016-04-11]
--------------------------

- `92f9a43 <https://github.com/openwisp/netjsonconfig/commit/92f9a43>`_: [schema] added human readable values for mode ``access_point`` and ``802.11s``
- `#47 <https://github.com/openwisp/netjsonconfig/issues/47>`_: [openwrt] improved encryption support
- `1a4c493 <https://github.com/openwisp/netjsonconfig/commit/1a4c493>`_: [openwrt] ``igmp_snooping`` now correctlt defaults to ``True``
- `#49 <https://github.com/openwisp/netjsonconfig/issues/49>`_: [schema] added descriptions and titles

Version 0.4.1 [2016-04-04]
--------------------------

- `b903c6f <https://github.com/openwisp/netjsonconfig/commit/b903c6f>`_: [schema] corrected wrong ipv4 minLength and maxLength
- `de98ae6 <https://github.com/openwisp/netjsonconfig/commit/de98ae6>`_: [schema] fixed interface minLength attribute
- `4679282 <https://github.com/openwisp/netjsonconfig/commit/4679282>`_: [schema] added regexp pattern for interface mac address (can be empty)
- `067b471 <https://github.com/openwisp/netjsonconfig/commit/067b471>`_: [schema] switched order between MTU and MAC address properties
- `26b62dd <https://github.com/openwisp/netjsonconfig/commit/26b62dd>`_: [schema] added pattern for wireless BSSID attribute
- `11da509 <https://github.com/openwisp/netjsonconfig/commit/11da509>`_: [openwrt] added regexp pattern to ``maclist`` elements
- `b061ee4 <https://github.com/openwisp/netjsonconfig/commit/b061ee4>`_: [openwrt] fixed empty output bug if addresses is empty list
- `7f74209 <https://github.com/openwisp/netjsonconfig/commit/7f74209>`_: [openwrt] removed support for ``chanbw`` for types ``ath5k`` and ``ath9k`` (**backward incompatible change**)
- `#46 <https://github.com/openwisp/netjsonconfig/issues/46>`_: [schema] introduced different profiles for radio settings
- `6ab9d5b <https://github.com/openwisp/netjsonconfig/compare/e8895c...6ab9d5b>`_ [openwrt] added support for "Automatic Channel Selection"
- `#48 <https://github.com/openwisp/netjsonconfig/issues/48>`_: [openwrt] improved support for config lists
- `9f93776 <https://github.com/openwisp/netjsonconfig/commit/9f93776>`_: [openwrt] simplified definition of custom interface "proto" options
- `a5f63f0 <https://github.com/openwisp/netjsonconfig/commit/a5f63f0>`_: [openwrt] allow to override general dns and dns_search settings
- `1b58f97 <https://github.com/openwisp/netjsonconfig/commit/1b58f97>`_: [schema] added ``stp`` (spanning tree protocol) property on bridge interfaces
- `bfbf23d <https://github.com/openwisp/netjsonconfig/commit/bfbf23d>`_: [openwrt] added ``igmp_snooping`` property on bridge interfaces
- `269c7bf <https://github.com/openwisp/netjsonconfig/commit/269c7bf>`_: [openwrt] added ``isolate`` property on wireless access points
- `2cbc242 <https://github.com/openwisp/netjsonconfig/commit/2cbc242>`_: [openwrt] fixed ``autostart`` when ``False``
- `85bd7dc <https://github.com/openwisp/netjsonconfig/commit/85bd7dc>`_: [openwrt] fixed mac address override on interfaces
- `45159e8 <https://github.com/openwisp/netjsonconfig/commit/45159e8>`_: [openwrt] allow overriding ``htmode`` option
- `b218f7d <https://github.com/openwisp/netjsonconfig/commit/b218f7d>`_: [schema] added ``enum_titles`` in ``encryption`` protocols
- `ef8c296 <https://github.com/openwisp/netjsonconfig/commit/ef8c296>`_: [schema] validate general hostname format
- `2f23cfd <https://github.com/openwisp/netjsonconfig/commit/2f23cfd>`_: [schema] validate interface ipv4 address format
- `612959e <https://github.com/openwisp/netjsonconfig/commit/612959e>`_: [openwrt] validate ntp server hostname format
- `f1116f0 <https://github.com/openwisp/netjsonconfig/commit/f1116f0>`_: [schema] validate ``dns_search`` hostname format #42
- `372d634 <https://github.com/openwisp/netjsonconfig/compare/3b0c356...372d634>`_ [openwrt] do not set dns to dhcp interfaces

Version 0.4.0 [2016-03-22]
--------------------------

- `#40 <https://github.com/openwisp/netjsonconfig/issues/40>`_: [openwrt] added support for ULA prefix
- `#44 <https://github.com/openwisp/netjsonconfig/issues/44>`_: [schema] added ``none`` to encryption choices
- `#45 <https://github.com/openwisp/netjsonconfig/issues/45>`_: [schema] improved address definition
- `#43 <https://github.com/openwisp/netjsonconfig/issues/43>`_: [openwrt] improved static routes
- `#41 <https://github.com/openwisp/netjsonconfig/issues/41>`_: [schema] added ``wds`` property & removed ``wds`` mode
- `#36 <https://github.com/openwisp/netjsonconfig/issues/36>`_: [schema] added specific settings for 802.11s (mesh) mode
- `3f6d2c6 <https://github.com/openwisp/netjsonconfig/commit/3f6d2c6>`_: [schema] removed NetJSON ``type`` from schema
- `04c6058 <https://github.com/openwisp/netjsonconfig/commit/04c6058>`_: [openwrt] made file ``mode`` property required (**backward incompatible change**)
- `00e784e <https://github.com/openwisp/netjsonconfig/commit/00e784e>`_: [openwrt] added default switch settings
- `dd708cb <https://github.com/openwisp/netjsonconfig/commit/dd708cb>`_: [openwrt] added NTP default settings
- `f4148e4 <https://github.com/openwisp/netjsonconfig/commit/f4148e4>`_: [schema] removed ``txqueuelen`` from interface definition
- `574a48d <https://github.com/openwisp/netjsonconfig/commit/574a48d>`_: [schema] added ``title`` and ``type`` to ``bridge_members``
- `c6276f2 <https://github.com/openwisp/netjsonconfig/commit/c6276f2>`_: [schema] MTU title and minimum value
- `d8ab0e0 <https://github.com/openwisp/netjsonconfig/commit/d8ab0e0>`_: [schema] added ``minLength`` to interface name
- `67a0916 <https://github.com/openwisp/netjsonconfig/commit/67a0916>`_: [schema] added ``minLength`` to radio name
- `258892e <https://github.com/openwisp/netjsonconfig/commit/258892e>`_: [schema] added possible ``ciphers``
- `2751fe3 <https://github.com/openwisp/netjsonconfig/commit/2751fe3>`_: [schema] improved definition of wireless interface fields
- `478ef16 <https://github.com/openwisp/netjsonconfig/commit/478ef16>`_: [openwrt] added ``wmm`` property for wireless access points
- `b9a14f3 <https://github.com/openwisp/netjsonconfig/commit/b9a14f3>`_: [schema] added ``minLength`` and ``maxLength`` to interface ``mac`` property
- `526c2d1 <https://github.com/openwisp/netjsonconfig/commit/526c2d1>`_: [schema] added ``minLength`` and maxLength to wireless ``bssid`` property
- `c8c95d6 <https://github.com/openwisp/netjsonconfig/commit/c8c95d6>`_: [schema] improved ordering and titles of wireless properties
- `a226e90 <https://github.com/openwisp/netjsonconfig/commit/a226e90>`_: [openwrt] ignore advanced wifi options if zero
- `e008ef6 <https://github.com/openwisp/netjsonconfig/commit/e008ef6>`_: [openwrt] added ``macfilter`` to wireless access points
- `c70ab76 <https://github.com/openwisp/netjsonconfig/commit/c70ab76>`_: [openwrt] fixed empty dns and dns-search bug
- `778615a <https://github.com/openwisp/netjsonconfig/commit/778615a>`_: [openwrt] increased network ``maxLength``

Version 0.3.7 [2016-02-19]
--------------------------

- `007da6e <https://github.com/openwisp/netjsonconfig/commit/007da6e>`_:
  renamed "Coordinated Universal Time" to "UTC"
- `2c1e72e <https://github.com/openwisp/netjsonconfig/commit/2c1e72e>`_:
  fixed 'tx_power' ``KeyError``, introduced in `71b083e <https://github.com/openwisp/netjsonconfig/commit/71b083e>`_
- `aa8b485 <https://github.com/openwisp/netjsonconfig/commit/aa8b485>`_:
  added ``utils.evaluate_vars`` function
- `7323491 <https://github.com/openwisp/netjsonconfig/commit/7323491>`_:
  simplified implementation of *configuration variables*

Version 0.3.6 [2016-02-17]
--------------------------

- fixed ``flake8`` and ``isort`` warnings
- added ``flake8`` and ``isort`` checks to travis build
- `6ec5ce8 <https://github.com/openwisp/netjsonconfig/commit/6ec5ce8>`_:
  minor regexp optimization for generate method
- `#39 <https://github.com/openwisp/netjsonconfig/issues/39>`_:
  added `configuration variables <http://netjsonconfig.openwisp.org/en/latest/general/basics.html#context-configuration-variables>`_ feature
- `a3486d2 <https://github.com/openwisp/netjsonconfig/commit/a3486d2>`_:
  the shell utility can now use environment variables in ``config`` and ``templates``,
  `read relevant docs <http://netjsonconfig.openwisp.org/en/latest/general/commandline_utility.html#environment-variables>`_

Version 0.3.5 [2016-02-10]
--------------------------

- `18ecf28 <https://github.com/openwisp/netjsonconfig/commit/18ecf28>`_:
  removed ``hardware`` and ``operating_system`` sections
- `75c259d <https://github.com/openwisp/netjsonconfig/commit/75c259d>`_:
  reordered schema sections
- `010ca98 <https://github.com/openwisp/netjsonconfig/commit/010ca98>`_:
  file contents can now be only strings (**backward incompatible change**)
- `e2bb3b2 <https://github.com/openwisp/netjsonconfig/commit/e2bb3b2>`_:
  added non-standard ``propertyOrder`` attributes to schemas to facilitate UI ordering
- `#37 <https://github.com/openwisp/netjsonconfig/issues/37>`_:
  [schema] radio ``tx_power`` not required anymore
- `#38 <https://github.com/openwisp/netjsonconfig/issues/38>`_:
  [openwrt schema] hardened file mode contraints
- `c2cc3fc <https://github.com/openwisp/netjsonconfig/commit/c2cc3fc>`_:
  [schema] added minlength and maxlength to hostname

Version 0.3.4 [2016-01-14]
--------------------------

- `#35 <https://github.com/openwisp/netjsonconfig/issues/35>`_ wifi inherits ``disabled`` from interface

Version 0.3.3 [2015-12-18]
--------------------------

- `219f638 <https://github.com/openwisp/netjsonconfig/commit/219f638>`_ [cli] fixed binary standard output for ``generate`` method
- `a0b1373 <https://github.com/openwisp/netjsonconfig/compare/219f638...a0b1373>`_ removed
  timestamp from generated configuration archive to ensure reliable checksums

Version 0.3.2 [2015-12-11]
--------------------------

- `#31 <https://github.com/openwisp/netjsonconfig/issues/31>`_ added files in ``render`` output
- `#32 <https://github.com/openwisp/netjsonconfig/issues/32>`_ ``generate`` now returns an in-memory file object
- `badf292 <https://github.com/openwisp/netjsonconfig/commit/badf292>`_ updated command line utility script and examples
- `#33 <https://github.com/openwisp/netjsonconfig/issues/33>`_ added ``write`` method
- `5ff7360 <https://github.com/openwisp/netjsonconfig/commit/5ff7360>`_ [cli] positional ``config`` param is now ``--config`` or ``-c``
- `28de4a5 <https://github.com/openwisp/netjsonconfig/commit/28de4a5>`_ [cli] marked required arguments: ``--config``, ``--backend`` and ``--method``
- `f55cc4a <https://github.com/openwisp/netjsonconfig/commit/f55cc4a>`_ [cli] added ``--arg`` option to pass arguments to methods

Version 0.3.1 [2015-12-02]
--------------------------

- `69197ed <https://github.com/openwisp/netjsonconfig/commit/69197ed>`_ added "details" attribute to ``ValidationError``
- `0005186 <https://github.com/openwisp/netjsonconfig/commit/0005186>`_ avoid modifying original ``config`` argument

Version 0.3 [2015-11-30]
------------------------

- `#18 <https://github.com/openwisp/netjsonconfig/issues/18>`_ added ``OpenWisp`` backend
- `66ee96 <https://github.com/openwisp/netjsonconfig/commit/66ee96>`_ added file permission feature
- `#19 <https://github.com/openwisp/netjsonconfig/issues/19>`_ added sphinx documentation
  (published at `netjsonconfig.openwisp.org <http://netjsonconfig.openwisp.org>`_)
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
