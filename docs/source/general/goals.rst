Motivations and Goals
=====================

.. include:: ../_github.rst

In this page we explain the goals of this project and the motivations
that led us on this path.

Motivations
-----------

Federico Capoano (`@nemesisdesign <https://twitter.com/nemesisdesign>`_) has written
in detail the motivations that brought us here in a blog post:
`netjsonconfig: convert NetJSON to OpenWRT UCI
<http://nemesisdesign.net/blog/coding/netjsonconfig-convert-netjson-to-openwrt-uci/>`_.

Goals
-----

The main goal of this library is to replace the configuration generation feature
that is shipped in `OpenWISP Manager <https://github.com/openwisp/OpenWISP-Manager>`_.

We have learned a lot from *OpenWISP Manager*, one of the most important lessons we learned
is that the configuration generation feature must be a library decoupled from web framework
specific code (eg Rails, Django), this brings many advantages:

 * the project can evolve indipendently from the rest of the OpenWISP modules
 * easier to use and integrate in other projects
 * more people can use it and contribute
 * easier maintainance
 * easier to document

Another important goal is to build a tool which is **flexible** and **powerful**.
We do not want to limit our system to OpenWISP Firmware only, we want to be able
to control vanilla OpenWRT devices or other OpenWRT based devices too.

We did this by starting out with the :doc:`OpenWrt backend <../backends/openwrt>` first,
only afterwards we built the :doc:`OpenWisp backend <../backends/openwisp>` on top of it.

To summarize, our goals are:

 * build a reusable library to generate router configurations from
   `NetJSON <http://netjson.org>`_ objects
 * support the widely used router specific unix/linux distributions
 * provide good and extensive documentation
 * keep it simple stupid
 * avoid complexity unless extremely necessary
 * provide ways to add custom configuration options easily
 * provide ways to extend the library
 * :doc:`encourage contributions <./contributing>`
