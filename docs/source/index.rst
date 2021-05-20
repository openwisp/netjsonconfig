=============
netjsonconfig
=============

.. image:: https://travis-ci.org/openwisp/netjsonconfig.svg
  :target: https://travis-ci.org/openwisp/netjsonconfig

.. image:: https://coveralls.io/repos/openwisp/netjsonconfig/badge.svg
 :target: https://coveralls.io/r/openwisp/netjsonconfig

.. image:: https://requires.io/github/openwisp/netjsonconfig/requirements.svg?branch=master
  :target: https://requires.io/github/openwisp/netjsonconfig/requirements/?branch=master
  :alt: Requirements Status

.. image:: https://badge.fury.io/py/netjsonconfig.svg
  :target: http://badge.fury.io/py/netjsonconfig

.. image:: https://img.shields.io/gitter/room/nwjs/nw.js.svg?style=flat-square
  :target: https://gitter.im/openwisp/general

Netjsonconfig is part of the `OpenWISP project <http://openwrt.org>`_ and it's the official
configuration engine of `OpenWISP 2 <https://github.com/openwisp/ansible-openwisp2>`_.

.. image:: ./images/openwisp.org.svg
  :target: http://openwisp.org

.. include:: _github.rst

**netjsonconfig** is a python library that converts `NetJSON <http://netjson.org>`_
*DeviceConfiguration* objects into real router configurations that can be installed
on systems like `OpenWRT <http://openwrt.org>`_, `LEDE <https://www.lede-project.org/>`_
or `OpenWisp Firmware <https://github.com/openwisp/OpenWISP-Firmware>`_.

Its main features are:

    * `OpenWRT <http://openwrt.org>`_ / `LEDE <https://www.lede-project.org/>`_ support
    * `OpenWisp Firmware <https://github.com/openwisp/OpenWISP-Firmware>`_ support
    * `OpenVPN <https://openvpn.net>`_ support
    * `Wireguard <https://www.wireguard.com/>`_ support
    * Plugin interface for external backends, support more firmwares with an external package

      * :doc:`Create your backend </backends/create_your_backend>` as a plugin
      * Experimental `AirOS support <https://github.com/edoput/netjsonconfig-airos>`_ as a plugin

    * Based on the `NetJSON RFC <http://netjson.org/rfc.html>`_
    * **Validation** based on `JSON-Schema <http://json-schema.org/>`_
    * **Templates**: store common configurations in templates
    * **Multiple template inheritance**: reduce repetition to the minimum
    * **File inclusion**: easy inclusion of arbitrary files in configuration packages
    * **Variables**: reference variables in the configuration
    * **Command line utility**: easy to use from shell scripts or from other programming languages

Contents:

.. toctree::
   :maxdepth: 2

   /general/setup
   /general/basics
   /backends/openwrt
   /backends/openwisp
   /backends/vpn
   /backends/create_your_backend
   /general/commandline_utility
   /general/running_tests
   /general/contributing
   /general/goals
   /general/changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
