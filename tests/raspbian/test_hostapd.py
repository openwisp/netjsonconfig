import unittest

from netjsonconfig import Raspbian
from netjsonconfig.utils import _TabsMixin


class TestHostapd(unittest.TestCase, _TabsMixin):

    def test_wpa2_personal(self):
        o = Raspbian({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                },
            ],
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "wpa2-personal",
                        "encryption": {
                            "protocol": "wpa2_personal",
                            "cipher": "tkip+ccmp",
                            "key": "passphrase012345"
                        }
                    }
                }
            ]
        })

        expected = """# config: /etc/hostapd/hostapd.conf

interface=wlan0
driver=nl80211
hw_mode=g
channel=3
ieee80211n=1
ssid=wpa2-personal
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_passphrase=passphrase012345
rsn_pairwise=TKIP CCMP

# config: /etc/network/interfaces

auto wlan0
iface wlan0 inet manual

# script: /scripts/ipv4_forwarding.sh

sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

"""
        self.assertEqual(o.render(), expected)

    def test_wpa_personal(self):
        o = Raspbian({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                },
            ],
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "wpa-personal",
                        "encryption": {
                            "protocol": "wpa_personal",
                            "cipher": "auto",
                            "key": "passphrase012345"
                        }
                    }
                }
            ]
        })

        expected = """# config: /etc/hostapd/hostapd.conf

interface=wlan0
driver=nl80211
hw_mode=g
channel=3
ieee80211n=1
ssid=wpa-personal
auth_algs=1
wpa=1
wpa_key_mgmt=WPA-PSK
wpa_passphrase=passphrase012345

# config: /etc/network/interfaces

auto wlan0
iface wlan0 inet manual

# script: /scripts/ipv4_forwarding.sh

sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

"""
        self.assertEqual(o.render(), expected)

    def test_wpa2_enterprise_ap(self):
        o = Raspbian({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                },
            ],
            "interfaces": [
                {
                    "type": "wireless",
                    "name": "wlan0",
                    "mac": "de:9f:db:30:c9:c5",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "ap-ssid-example",
                        "encryption": {
                            "protocol": "wpa2_enterprise",
                            "server": "radius.example.com",
                            "key": "the-shared-key",
                        },
                    },
                }
            ]
        })

        expected = """# config: /etc/hostapd/hostapd.conf

interface=wlan0
driver=nl80211
hw_mode=g
channel=3
ieee80211n=1
ssid=ap-ssid-example
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-EAP
ieee8021x=1
eap_server=1
eapol_version=1
auth_server_addr=radius.example.com
auth_server_port=1812
auth_server_shared_secret=the-shared-key

# config: /etc/network/interfaces

auto wlan0
iface wlan0 inet manual

# script: /scripts/ipv4_forwarding.sh

sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

"""

        self.assertEqual(o.render(), expected)

    def test_wep_open(self):
        o = Raspbian({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                },
            ],
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "wep",
                        "encryption": {
                            "protocol": "wep_open",
                            "key": "wepkey1234567"
                        }
                    }
                }
            ]
        })

        expected = """# config: /etc/hostapd/hostapd.conf

interface=wlan0
driver=nl80211
hw_mode=g
channel=3
ieee80211n=1
ssid=wep
auth_algs=1
wep_default_key=0
wep_key0=wepkey1234567

# config: /etc/network/interfaces

auto wlan0
iface wlan0 inet manual

# script: /scripts/ipv4_forwarding.sh

sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

"""
        self.assertEqual(o.render(), expected)

    def test_wep_shared(self):
        o = Raspbian({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                },
            ],
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "wep",
                        "encryption": {
                            "protocol": "wep_shared",
                            "key": "wepkey1234567"
                        }
                    }
                }
            ]
        })

        expected = """# config: /etc/hostapd/hostapd.conf

interface=wlan0
driver=nl80211
hw_mode=g
channel=3
ieee80211n=1
ssid=wep
auth_algs=2
wep_default_key=0
wep_key0=wepkey1234567

# config: /etc/network/interfaces

auto wlan0
iface wlan0 inet manual

# script: /scripts/ipv4_forwarding.sh

sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

"""
        self.assertEqual(o.render(), expected)

    def test_encryption_disabled(self):
        o = Raspbian({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                },
            ],
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "MyNetwork",
                        "encryption": {
                            "disabled": True,
                            "protocol": "wpa2_personal",
                            "cipher": "tkip+ccmp",
                            "key": "passphrase012345"
                        }
                    }
                }
            ]
        })

        expected = """# config: /etc/hostapd/hostapd.conf

interface=wlan0
driver=nl80211
hw_mode=g
channel=3
ieee80211n=1
ssid=MyNetwork

# config: /etc/network/interfaces

auto wlan0
iface wlan0 inet manual

# script: /scripts/ipv4_forwarding.sh

sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

"""
        self.assertEqual(o.render(), expected)

    def test_no_encryption(self):
        o = Raspbian({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                },
            ],
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "open",
                        "encryption": {"protocol": "none"}
                    }
                }
            ]
        })

        expected = """# config: /etc/hostapd/hostapd.conf

interface=wlan0
driver=nl80211
hw_mode=g
channel=3
ieee80211n=1
ssid=open

# config: /etc/network/interfaces

auto wlan0
iface wlan0 inet manual

# script: /scripts/ipv4_forwarding.sh

sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

"""
        self.assertEqual(o.render(), expected)

    def test_macaddracl_accept(self):
        o = Raspbian({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                },
            ],
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "MyWifiAP",
                        "macfilter": "accept",
                        "maclist": [
                            "E8:94:F6:33:8C:1D",
                            "42:6c:8f:95:0f:00"
                        ]
                    }
                }
            ]
        })

        expected = """# config: /etc/hostapd/hostapd.conf

interface=wlan0
driver=nl80211
hw_mode=g
channel=3
ieee80211n=1
ssid=MyWifiAP
macaddr_acl=1
accept_mac_file=/etc/hostapd.accept

# config: /etc/hostapd.accept

E8:94:F6:33:8C:1D
42:6c:8f:95:0f:00

# config: /etc/network/interfaces

auto wlan0
iface wlan0 inet manual

# script: /scripts/ipv4_forwarding.sh

sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

"""
        self.assertEqual(o.render(), expected)

    def test_macaddracl_deny(self):
        o = Raspbian({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                },
            ],
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "MyWifiAP",
                        "macfilter": "deny",
                        "maclist": [
                            "E8:94:F6:33:8C:1D",
                            "42:6c:8f:95:0f:00"
                        ]
                    }
                }
            ]
        })

        expected = """# config: /etc/hostapd/hostapd.conf

interface=wlan0
driver=nl80211
hw_mode=g
channel=3
ieee80211n=1
ssid=MyWifiAP
macaddr_acl=0
deny_mac_file=/etc/hostapd.deny

# config: /etc/hostapd.deny

E8:94:F6:33:8C:1D
42:6c:8f:95:0f:00

# config: /etc/network/interfaces

auto wlan0
iface wlan0 inet manual

# script: /scripts/ipv4_forwarding.sh

sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

"""
        self.assertEqual(o.render(), expected)
