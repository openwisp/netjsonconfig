.. _airos-configuration-upgrade:

Tools
-----

AirOS is shipped with proprietary tools that can parse the configuration file and upgrade the antenna.

cfgmtd
^^^^^^

This tool can write and read data to the memory that persist between reboots.

ubntcfg
^^^^^^^

This tool can parse the configuration and creates the init scripts that configure the device

rc scripts
^^^^^^^^^^

This are not commands but a collection of scripts that orchestrate the configuration process. As they are stored on the antenna they can be modified to obtain different behaviours.

* update scripts are stored in `/usr/local/rc.d`
* module list is stored in `/etc/startup.list`

The update process is orchestrated by the `/usr/local/rc.d/rc.do.softrestart` script. 

Process
-------

AirOS mantains the device configuration in two files, both can be found in `/tmp`.

* `/tmp/system.cfg` the target configuration
* `/tmp/running.cfg` the running configuration

If we want to upgrade the device configuration with our file we can overwrite the target configuration and runt the commands `cfgmtd -w` and `/usr/local/rc.d/rc.do.softrestart save`


Full transcript of the update processs

.. code-block:: bash

    cp /path/to/my/config.cfg /tmp/system.cfg
    # writes the configuration to the persistent memory
    cfgmtd -w /tmp/system.cfg
    # initiate the configuration update
    /usr/local/rc.d/rc.do.softrestart save
