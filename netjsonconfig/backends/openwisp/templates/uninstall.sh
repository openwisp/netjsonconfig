#!/bin/sh

PROGDIR=$(cd -P -- "$(dirname $0)" && pwd -P)

# Undo changes
# L2TCs
echo "Removing l2 tc configuration"
$PROGDIR/l2tc_script.sh stop

# VPNs
echo "Stopping l2 vpn and removing their configuration"
uci changes openvpn | grep "=openvpn" | cut -d'.' -f2 | cut -d'=' -f1 | awk '{print "/var/run/openvpn-"$1".pid"}' | xargs cat | xargs kill
uci changes openvpn | grep "=openvpn" | cut -d'.' -f2 | cut -d'=' -f1 | awk '{"rm /var/run/openvpn-"$1".pid"|getline;print}'
uci revert openvpn

{% for vpn in l2vpn %}
echo "Removing tap {{ vpn.name }}"
openvpn --rmtun --dev {{ vpn.name }} --dev-type tap
{% endfor %}

uci revert wireless
uci revert network

echo "Restoring original wifi and network configurations"
/etc/init.d/network restart
wifi

echo "Configuration un-installed"
