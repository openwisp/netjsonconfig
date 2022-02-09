netjsonconfig
=============

.. image:: https://github.com/openwisp/netjsonconfig/workflows/Netjsonconfig%20CI%20Build/badge.svg?branch=master
   :target: https://github.com/openwisp/netjsonconfig/actions?query=workflow%3A%22Netjsonconfig+CI+Build%22

.. image:: https://coveralls.io/repos/openwisp/netjsonconfig/badge.svg
  :target: https://coveralls.io/r/openwisp/netjsonconfig

.. image:: https://img.shields.io/librariesio/release/github/openwisp/netjsonconfig
   :target: https://libraries.io/github/openwisp/netjsonconfig#repository_dependencies
   :alt: Dependency monitoring 

.. image:: https://img.shields.io/gitter/room/nwjs/nw.js.svg?style=flat-square
   :target: https://gitter.im/openwisp/general

.. image:: https://badge.fury.io/py/netjsonconfig.svg
   :target: http://badge.fury.io/py/netjsonconfig

.. image:: https://pepy.tech/badge/netjsonconfig
   :target: https://pepy.tech/project/netjsonconfig
   :alt: downloads

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://pypi.org/project/black/
   :alt: code style: black

------------

Netjsonconfig is a part of the `OpenWISP project <http://openwisp.org>`_ and it's the official
configuration engine of `OpenWISP 2 <https://github.com/openwisp/ansible-openwisp2>`_.

.. image:: http://netjsonconfig.openwisp.org/en/latest/_images/openwisp.org.svg
  :target: http://openwisp.org

**netjsonconfig** is a python library that converts `NetJSON <http://netjson.org>`_
*DeviceConfiguration* objects into real router configurations that can be installed
on systems like `OpenWRT <http://openwrt.org>`_, `LEDE <https://www.lede-project.org/>`_
or `OpenWisp Firmware <https://github.com/openwisp/OpenWISP-Firmware>`_.

Its main features are listed below for your reference:

* `OpenWRT <http://openwrt.org>`_ / `LEDE <https://www.lede-project.org/>`_ support
* `OpenWisp Firmware <https://github.com/openwisp/OpenWISP-Firmware>`_ support
* `OpenVPN <https://openvpn.net>`_ support
* `WireGuard <https://www.wireguard.com/>`_ support
* Possibility to support more firmwares via custom backends
* Based on the `NetJSON RFC <http://netjson.org/rfc.html>`_
* **Validation** based on `JSON-Schema <http://json-schema.org/>`_
* **Templates**: store common configurations in templates
* **Multiple template inheritance**: reduce repetition to the minimum
* **File inclusion**: easy inclusion of arbitrary files in configuration packages
* **Variables**: reference variables in the configuration
* **Command line utility**: easy to use from shell scripts or from other programming languages

`Documentation <http://netjsonconfig.openwisp.org/>`_ |
`Change log <https://github.com/openwisp/netjsonconfig/blob/master/CHANGES.rst>`_ |
`Support channels <http://openwisp.org/support.html>`_ |
`Issue Tracker <https://github.com/openwisp/netjsonconfig/issues>`_ |
`License <https://github.com/openwisp/netjsonconfig/blob/master/LICENSE>`_
