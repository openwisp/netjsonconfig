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

------------

Netjsonconfig is part of the `OpenWISP project <http://openwrt.org>`_.

.. image:: http://netjsonconfig.openwisp.org/en/latest/_images/openwisp.org.svg
  :target: http://openwisp.org

**netjsonconfig** is a python library that converts `NetJSON <http://netjson.org>`_
*DeviceConfiguration* objects into real router configurations that can be installed
on systems like `OpenWRT <http://openwrt.org>`_, `LEDE <https://www.lede-project.org/>`_
or `OpenWisp Firmware <https://github.com/openwisp/OpenWISP-Firmware>`_.

Its main features are:

* `OpenWRT <http://openwrt.org>`_ / `LEDE <https://www.lede-project.org/>`_ support
* `OpenWisp Firmware <https://github.com/openwisp/OpenWISP-Firmware>`_ support
* `OpenVPN <https://openvpn.net>`_ support
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
`Mailing List <https://groups.google.com/d/forum/openwisp>`_ |
`Issue Tracker <https://github.com/openwisp/netjsonconfig/issues>`_ |
`License <https://github.com/openwisp/netjsonconfig/blob/master/LICENSE>`_
