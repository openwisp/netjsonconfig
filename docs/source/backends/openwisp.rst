====================
OpenWISP 1.x Backend
====================

.. include:: ../_github.rst

The OpenWISP 1.x Backend is based on the OpenWRT backend, therefore it inherits all
its features with some differences that are explained in this page.

Generate method
---------------

The ``generate`` method of the ``OpenWisp`` backend differs from the ``OpenWrt`` backend
in a few ways.

1. the generated tar.gz archive is not designed to be installed with ``sysupgrade -r``
2. the ``generate`` method will automatically add a few additional executable scripts:

 * ``install.sh`` to install the configuration
 * ``uninstall.sh`` to uninstall the configuration
 * ``tc_script.sh`` to start/stop traffic control settings
 * one "up" script for each tap VPN configured
 * one "down" script for each tap VPN configured

3. the openvpn certificates are expected to be located the following path: ``/openvpn/x509/``
4. the crontabs are expected in to be located at the following path: ``/crontabs/``

General settings
----------------

The ``hostname`` attribute in the ``general`` key is **required**.

Traffic Control
---------------

For backward compatibility with `OpenWISP Manager <https://github.com/openwisp/OpenWISP-Manager>`_
the schema of the ``OpenWisp`` backend allows to define a ``tc_options`` section that will
be used to generate ``tc_script.sh``.

The ``tc_options`` key must be a list, each element of the list must be a dictionary which
allows the following keys:

+----------------------+---------+----------------------------------------------------------------------+
| key name             | type    | function                                                             |
+======================+=========+======================================================================+
| ``name``             | string  | **required**, name of the network interface that needs to be limited |
+----------------------+---------+----------------------------------------------------------------------+
| ``input_bandwidth``  | integer | maximum input bandwidth in kbps                                      |
+----------------------+---------+----------------------------------------------------------------------+
| ``output_bandwidth`` | integer | maximum output bandwidth in kbps                                     |
+----------------------+---------+----------------------------------------------------------------------+

Traffic control example
~~~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "tc_options": [
            {
                "name": "tap0",
                "input_bandwidth": 2048,
                "output_bandwidth": 1024
            }
        ]
    }

Will generate the following ``tc_script.sh``:

.. code-block:: shell

    #!/bin/sh /etc/rc.common

    KERNEL_VERSION=`uname -r`
    KERNEL_MODULES="sch_htb sch_prio sch_sfq cls_fw sch_dsmark sch_ingress sch_tbf sch_red sch_hfsc act_police cls_tcindex cls_flow cls_route cls_u32"
    KERNEL_MPATH=/lib/modules/$KERNEL_VERSION/

    TC_COMMAND=/usr/sbin/tc

    check_prereq() {
        echo "Checking prerequisites..."

        echo "Checking kernel modules..."
        for kmod in $KERNEL_MODULES; do
        if [ ! -f $KERNEL_MPATH/$kmod.ko ]; then
            echo "Prerequisite error: can't find kernel module '$kmod' in '$KERNEL_MPATH'"
            exit 1
        fi
        done

        echo "Checking tc tool..."
        if [ ! -x $TC_COMMAND ]; then
            echo "Prerequisite error: can't find traffic control tool ($TC_COMMAND)"
            exit 1
        fi

        echo "Prerequisites satisfied."
    }

    load_modules() {
        for kmod in $KERNEL_MODULES; do
            insmod $KERNEL_MPATH/$kmod.ko  >/dev/null 2>&1
        done
    }

    unload_modules() {
        for kmod in $KERNEL_MODULES; do
            rmmod $kmod  >/dev/null 2>&1
        done
    }


    stop() {

        tc qdisc del dev tap0 root


        tc qdisc del dev tap0 ingress


        unload_modules
    }

    start() {
        check_prereq
        load_modules


        # shaping output traffic for tap0
        # creating parent qdisc for root
        tc qdisc add dev tap0 root handle 1: htb default 2

        # aggregated traffic shaping parent class

        tc class add dev tap0 parent 1 classid 1:1 htb rate 1024kbit burst 191k


        # default traffic shaping class
        tc class add dev tap0 parent 1:1 classid 1:2 htb rate 512kbit ceil 1024kbit


        # policing input traffic for tap0
        # creating parent qdisc for ingress
        tc qdisc add dev tap0 ingress


        # default policer with lowest preference (last checked)
        tc filter add dev tap0 parent ffff: preference 0 u32 match u32 0x0 0x0 police rate 2048kbit burst 383k drop flowid :1

    }

    boot() {
        start
    }

    restart() {
        stop
        start
    }

Full OpenWISP configuration example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example shows a full working *configuration dictionary* for the
``OpenWisp`` backend.

.. code-block:: python

    {
        "general": {
            "hostname": "OpenWISP"
        },
        "interfaces": [
            {
                "name": "tap0",
                "type": "virtual"
            },
            {
                "network": "service",
                "name": "br-service",
                "type": "bridge",
                "bridge_members": [
                    "tap0"
                ]
            },
            {
                "name": "wlan0",
                "type": "wireless",
                "wireless": {
                    "radio": "radio0",
                    "mode": "access_point",
                    "ssid": "provinciawifi",
                    "isolate": True,
                    "network": ["service"]
                }
            }
        ],
        "radios": [
            {
                "name": "radio0",
                "phy": "phy0",
                "driver": "mac80211",
                "protocol": "802.11g",
                "channel": 11,
                "channel_width": 20,
                "tx_power": 10,
                "country": "IT"
            }
        ],
        "openvpn": [
            {
                "name": "2693",
                "cipher": "AES-128-CBC",
                "ca": "/tmp/owispmanager/openvpn/x509/ca_1_service.pem",
                "mute_replay_warnings": True,
                "script_security": 1,
                "proto": "tcp-client",
                "mute": 10,
                "up_delay": 1,
                "cert": "/tmp/owispmanager/openvpn/x509/l2vpn_client_2693.pem",
                "up": "/tmp/owispmanager/openvpn/vpn_2693_script_up.sh",
                "log": "/tmp/openvpn_2693.log",
                "verb": 1,
                "dev_type": "tap",
                "persist_tun": True,
                "keepalive": "5 40",
                "key": "/tmp/owispmanager/openvpn/x509/l2vpn_client_2693.pem",
                "ns_cert_type": "server",
                "mode": "p2p",
                "pull": True,
                "enabled": True,
                "comp_lzo": "yes",
                "down": "/tmp/owispmanager/openvpn/vpn_2693_script_down.sh",
                "dev": "tap0",
                "nobind": True,
                "remote": [
                    {
                        "host": "vpn.openwisp.org",
                        "port": 12128
                    }
                ],
                "tls_client": True,
                "resolv_retry": True,
                "up_restart": True
            }
        ],
        "tc_options": [
            {
                "name": "tap0",
                "input_bandwidth": 2048,
                "output_bandwidth": 1024
            }
        ],
        "files": [
            {
                "path": "/openvpn/x509/ca.pem",
                "mode": "0644",
                "contents": "-----BEGIN CERTIFICATE-----\nstripped_down\n-----END CERTIFICATE-----\n"
            },
            {
                "path": "/openvpn/x509/l2vpn_client_1_2325_2693.pem",
                "mode": "0644",
                "contents": "-----BEGIN CERTIFICATE-----\nstripped_down\n-----END CERTIFICATE-----\n-----BEGIN RSA PRIVATE KEY-----\nstripped_down\n-----END RSA PRIVATE KEY-----\n"
            },
            {
                "path": "/crontabs/root",
                "mode": "0644",
                "contents": "* * * * * echo 'test' > /tmp/test-cron"
            }
        ]
    }
