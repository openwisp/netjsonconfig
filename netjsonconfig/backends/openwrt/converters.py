import json
from copy import deepcopy

from ipaddress import ip_interface, ip_network

from ...utils import get_copy, sorted_dict
from ..base.converter import BaseConverter
from ..openvpn.converters import OpenVpn as BaseOpenVpn
from .schema import default_radio_driver
from .timezones import timezones


def logical_name(name):
    return name.replace('.', '_').replace('-', '_')


class General(BaseConverter):
    def to_intermediate(self):
        general = get_copy(self.netjson, 'general')
        network = self.__get_ula(general)
        system = self.__get_system(general)
        return (
            ('system', system),
            ('network', network)
        )

    def __get_system(self, general):
        if not general:
            return None
        timezone_human = general.get('timezone', 'UTC')
        timezone_value = timezones[timezone_human]
        general.update({
            '.type': 'system',
            '.name': 'system',
            'hostname': general.get('hostname', 'OpenWRT'),
            'timezone': timezone_value,
            'zonename': timezone_human,
        })
        return [sorted_dict(general)]

    def __get_ula(self, general):
        if 'ula_prefix' in general:
            ula = {
                '.type': 'globals',
                '.name': 'globals',
                'ula_prefix': general.pop('ula_prefix')
            }
            return [sorted_dict(ula)]
        return None


class Ntp(BaseConverter):
    def to_intermediate(self):
        ntp = get_copy(self.netjson, 'ntp')
        result = None
        if ntp:
            ntp.update({
                '.type': 'timeserver',
                '.name': 'ntp',
            })
            result = [sorted_dict(ntp)]
        return (('system', result),)


class Led(BaseConverter):
    def to_intermediate(self):
        result = []
        for led in get_copy(self.netjson, 'led'):
            led.update({
                '.type': 'led',
                '.name': 'led_{0}'.format(led['name'].lower()),
            })
            result.append(sorted_dict(led))
        return (('system', result),)


class Interfaces(BaseConverter):
    def to_intermediate(self):
        result = []
        for interface in get_copy(self.netjson, 'interfaces'):
            i = 1
            uci_name = self.__get_uci_name(interface)
            address_list = self.__get_addresses(interface)
            interface = self.__get_interface(interface, uci_name)
            # create one or more "config interface" UCI blocks
            for address in address_list:
                uci_interface = deepcopy(interface)
                # add suffix to logical name when
                # there is more than one interface
                if i > 1:
                    uci_interface['.name'] = '{name}_{i}'.format(name=uci_name, i=i)
                uci_interface.update({
                    'dns': self.__get_dns_servers(uci_interface, address),
                    'dns_search': self.__get_dns_search(uci_interface, address),
                    'proto': self.__get_proto(uci_interface, address),
                })
                uci_interface = self.__get_bridge(uci_interface, i)
                if address:
                    uci_interface.update(address)
                result.append(sorted_dict(uci_interface))
                i += 1
        return (('network', result),)

    def __get_uci_name(self, interface):
        """
        determines uci logical interface name
        """
        name = interface.get('network') or interface['name']
        return logical_name(name)

    def __get_addresses(self, interface):
        """
        converts NetJSON address to
        UCI intermediate data structure
        """
        address_list = get_copy(interface, 'addresses')
        # do not ignore interfaces if they do not contain any address
        if not address_list:
            return [{'proto': 'none'}]
        result = []
        static = {}
        dhcp = []
        for address in address_list:
            family = address.get('family')
            # dhcp
            if address['proto'] == 'dhcp':
                address['proto'] = 'dhcp' if family == 'ipv4' else 'dhcpv6'
                dhcp.append(self.__del_address_keys(address))
                continue
            # static
            address_key = 'ipaddr' if family == 'ipv4' else 'ip6addr'
            static.setdefault(address_key, [])
            static[address_key].append('{address}/{mask}'.format(**address))
            static.update(self.__del_address_keys(address))
        if static:
            # do not use CIDR notation when using a single ipv4
            # see https://github.com/openwisp/netjsonconfig/issues/54
            if len(static.get('ipaddr', [])) == 1:
                network = ip_interface(static['ipaddr'][0])
                static['ipaddr'] = str(network.ip)
                static['netmask'] = str(network.netmask)
            # do not use lists when using a single ipv6 address
            # (avoids to change output of existing configuration)
            if len(static.get('ip6addr', [])) == 1:
                static['ip6addr'] = static['ip6addr'][0]
            result.append(static)
        if dhcp:
            result += dhcp
        return result

    def __get_interface(self, interface, uci_name):
        """
        converts NetJSON interface to
        UCI intermediate data structure
        """
        interface.update({
            '.type': 'interface',
            '.name': uci_name,
            'ifname': interface.pop('name')
        })
        if 'network' in interface:
            del interface['network']
        if 'mac' in interface:
            # mac address of wireless interface must
            # be set in /etc/config/wireless, therfore
            # we can skip this in /etc/config/network
            if interface.get('type') != 'wireless':
                interface['macaddr'] = interface['mac']
            del interface['mac']
        if 'autostart' in interface:
            interface['auto'] = interface['autostart']
            del interface['autostart']
        if 'disabled' in interface:
            interface['enabled'] = not interface['disabled']
            del interface['disabled']
        if 'wireless' in interface:
            del interface['wireless']
        if 'addresses' in interface:
            del interface['addresses']
        return interface

    _address_keys = ['address', 'mask', 'family']

    def __del_address_keys(self, address):
        """
        deletes NetJSON address keys
        """
        for key in self._address_keys:
            if key in address:
                del address[key]
        return address

    def __get_bridge(self, interface, i):
        """
        converts NetJSON bridge to
        UCI intermediate data structure
        """
        # ensure type "bridge" is only given to one logical interface
        if interface['type'] == 'bridge' and i < 2:
            bridge_members = ' '.join(interface.pop('bridge_members'))
            # put bridge members in ifname attribute
            if bridge_members:
                interface['ifname'] = bridge_members
            # if no members, this is an empty bridge
            else:
                interface['bridge_empty'] = True
                del interface['ifname']
        # bridge has already been defined
        # but we need to add more references to it
        elif interface['type'] == 'bridge' and i >= 2:
            # openwrt adds "br-" prefix to bridge interfaces
            # we need to take this into account when referring
            # to these physical names
            interface['ifname'] = 'br-{ifname}'.format(**interface)
            # do not repeat bridge attributes (they have already been processed)
            del interface['type']
            del interface['bridge_members']
        elif interface['type'] != 'bridge':
            del interface['type']
        return interface

    def __get_proto(self, interface, address):
        """
        determines UCI interface "proto" option
        """
        # proto defaults to static
        address_proto = address.pop('proto', 'static')
        if 'proto' not in interface:
            return address_proto
        else:
            # allow override on interface level
            return interface.pop('proto')

    def __get_dns_servers(self, uci, address):
        """
        determines UCI interface "dns" option
        """
        # allow override
        if 'dns' in uci:
            return uci['dns']
        # ignore if using DHCP or if "proto" is none
        if address['proto'] in ['dhcp', 'dhcpv6', 'none']:
            return None
        dns = self.netjson.get('dns_servers', None)
        if dns:
            return ' '.join(dns)

    def __get_dns_search(self, uci, address):
        """
        determines UCI interface "dns_search" option
        """
        # allow override
        if 'dns_search' in uci:
            return uci['dns_search']
        # ignore if "proto" is none
        if address['proto'] == 'none':
            return None
        dns_search = self.netjson.get('dns_search', None)
        if dns_search:
            return ' '.join(dns_search)


class Routes(BaseConverter):
    __delete_keys = ['device', 'next', 'destination', 'cost']

    def to_intermediate(self):
        result = []
        i = 1
        for route in get_copy(self.netjson, 'routes'):
            network = ip_interface(route['destination'])
            target = network.ip if network.version == 4 else network.network
            route.update({
                '.type': 'route{0}'.format('6' if network.version == 6 else ''),
                '.name': 'route{0}'.format(i),
                'interface': route['device'],
                'target': str(target),
                'gateway': route['next'],
                'metric': route['cost'],
                'source': route.get('source')
            })
            if network.version == 4:
                route['netmask'] = str(network.netmask)
            for key in self.__delete_keys:
                del route[key]
            result.append(sorted_dict(route))
            i += 1
        return (('network', result),)


class Rules(BaseConverter):
    netjson_key = 'ip_rules'

    def to_intermediate(self):
        result = []
        i = 1
        for rule in get_copy(self.netjson, 'ip_rules'):
            src_net = None
            dest_net = None
            family = 4
            if 'src' in rule:
                src_net = ip_network(rule['src'])
            if 'dest' in rule:
                dest_net = ip_network(rule['dest'])
            if dest_net or src_net:
                family = dest_net.version if dest_net else src_net.version
            rule.update({
                '.type': 'rule{0}'.format(family).replace('4', ''),
                '.name': 'rule{0}'.format(i),
            })
            result.append(sorted_dict(rule))
            i += 1
        return (('network', result),)


class Switch(BaseConverter):
    def to_intermediate(self):
        result = []
        for switch in get_copy(self.netjson, 'switch'):
            switch.update({
                '.type': 'switch',
                '.name': switch['name'],
            })
            i = 1
            vlans = []
            for vlan in switch['vlan']:
                vlan.update({
                    '.type': 'switch_vlan',
                    '.name': '{0}_vlan{1}'.format(switch['name'], i)
                })
                vlans.append(sorted_dict(vlan))
                i += 1
            del switch['vlan']
            result.append(sorted_dict(switch))
            result += vlans
        return (('network', result),)


class Radios(BaseConverter):
    _delete_keys = ['name', 'protocol', 'channel_width']

    def to_intermediate(self):
        result = []
        for radio in get_copy(self.netjson, 'radios'):
            radio.update({
                '.type': 'wifi-device',
                '.name': radio['name'],
            })
            # rename tx_power to txpower
            if 'tx_power' in radio:
                radio['txpower'] = radio['tx_power']
                del radio['tx_power']
            # rename driver to type
            radio['type'] = radio.pop('driver', default_radio_driver)
            # determine hwmode option
            radio['hwmode'] = self.__get_hwmode(radio)
            # check if using channel 0, that means "auto"
            if radio['channel'] is 0:
                radio['channel'] = 'auto'
            # determine channel width
            if radio['type'] == 'mac80211':
                radio['htmode'] = self.__get_htmode(radio)
            # ensure country is uppercase
            if radio.get('country'):
                radio['country'] = radio['country'].upper()
            # delete unneded keys
            for key in self._delete_keys:
                del radio[key]
            # append sorted dict
            result.append(sorted_dict(radio))
        return (('wireless', result),)

    def __get_hwmode(self, radio):
        """
        possible return values are: 11a, 11b, 11g
        """
        protocol = radio['protocol']
        if protocol in ['802.11a', '802.11b', '802.11g']:
            # return 11a, 11b or 11g
            return protocol[4:]
        # determine hwmode depending on channel used
        if radio['channel'] is 0:
            # when using automatic channel selection, we need an
            # additional parameter to determine the frequency band
            return radio.get('hwmode')
        elif radio['channel'] <= 13:
            return '11g'
        else:
            return '11a'

    def __get_htmode(self, radio):
        """
        only for mac80211 driver
        """
        # allow overriding htmode
        if 'htmode' in radio:
            return radio['htmode']
        if radio['protocol'] == '802.11n':
            return 'HT{0}'.format(radio['channel_width'])
        elif radio['protocol'] == '802.11ac':
            return 'VHT{0}'.format(radio['channel_width'])
        # disables n
        return 'NONE'


class Wireless(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        for interface in get_copy(self.netjson, 'interfaces'):
            if 'wireless' not in interface:
                continue
            wireless = interface['wireless']
            # prepare UCI wifi-iface directive
            uci_wifi = wireless.copy()
            # inherit "disabled" attribute if present
            uci_wifi['disabled'] = interface.get('disabled')
            # add ifname
            uci_wifi['ifname'] = interface['name']
            uci_wifi.update({
                '.name': 'wifi_{0}'.format(logical_name(interface['name'])),
                '.type': 'wifi-iface',
            })
            # rename radio to device
            uci_wifi['device'] = wireless['radio']
            del uci_wifi['radio']
            # mac address override
            if 'mac' in interface:
                uci_wifi['macaddr'] = interface['mac']
            # map netjson wifi modes to uci wifi modes
            modes = {
                'access_point': 'ap',
                'station': 'sta',
                'adhoc': 'adhoc',
                'monitor': 'monitor',
                '802.11s': 'mesh'
            }
            uci_wifi['mode'] = modes[wireless['mode']]
            # map advanced 802.11 netjson attributes to UCI
            wifi_options = {
                'ack_distance': 'distance',
                'rts_threshold': 'rts',
                'frag_threshold': 'frag'
            }
            for netjson_key, uci_key in wifi_options.items():
                value = wireless.get(netjson_key)
                if value is not None:
                    # ignore if 0 (autogenerated UIs might use 0 as default value)
                    if value > 0:
                        uci_wifi[uci_key] = value
                    del uci_wifi[netjson_key]
            # determine encryption for wifi
            if uci_wifi.get('encryption'):
                del uci_wifi['encryption']
                uci_encryption = self.__get_encryption(wireless)
                uci_wifi.update(uci_encryption)
            # attached networks (openwrt specific)
            # by default the wifi interface is attached
            # to its defining interface
            # but this behaviour can be overridden
            if not uci_wifi.get('network'):
                # get network, default to ifname
                network = interface.get('network', interface['name'])
                uci_wifi['network'] = [network]
            uci_wifi['network'] = ' '.join(uci_wifi['network'])\
                                     .replace('.', '_')\
                                     .replace('-', '_')
            result.append(sorted_dict(uci_wifi))
        return (('wireless', result),)

    def __get_encryption(self, wireless):
        encryption = wireless.get('encryption', {})
        disabled = encryption.get('disabled', False)
        encryption_map = {
            'wep_open': 'wep-open',
            'wep_shared': 'wep-shared',
            'wpa_personal': 'psk',
            'wpa2_personal': 'psk2',
            'wpa_personal_mixed': 'psk-mixed',
            'wpa_enterprise': 'wpa',
            'wpa2_enterprise': 'wpa2',
            'wpa_enterprise_mixed': 'wpa-mixed',
            'wps': 'psk'
        }
        # if encryption disabled return empty dict
        if not encryption or disabled or encryption['protocol'] == 'none':
            return {}
        # otherwise configure encryption
        uci = encryption.copy()
        for option in ['protocol', 'key', 'cipher', 'disabled']:
            if option in uci:
                del uci[option]
        protocol = encryption['protocol']
        # default to protocol raw value in order
        # to allow customization by child classes
        uci['encryption'] = encryption_map.get(protocol, protocol)
        if protocol.startswith('wep'):
            uci['key'] = '1'
            uci['key1'] = encryption['key']
            # tell hostapd/wpa_supplicant key is not hex format
            if protocol == 'wep_open':
                uci['key1'] = 's:{0}'.format(uci['key1'])
        elif 'key' in encryption:
            uci['key'] = encryption['key']
        # add ciphers
        cipher = encryption.get('cipher')
        if cipher and protocol.startswith('wpa') and cipher != 'auto':
            uci['encryption'] += '+{0}'.format(cipher)
        return uci


class OpenVpn(BaseOpenVpn):
    def __get_vpn(self, vpn):
        config = super(OpenVpn, self).__get_vpn(vpn)
        config['enabled'] = not config.get('disabled', False)
        config.update({
            '.name': logical_name(config.pop('name')),
            '.type': 'openvpn'
        })
        return config


class Default(BaseConverter):
    @classmethod
    def should_run(cls, config):
        """ Always runs """
        return True

    def to_intermediate(self):
        # determine config keys to ignore
        ignore_list = list(self.backend.schema['properties'].keys())
        # determine extra packages used
        extra_packages = {}
        for key, value in self.netjson.items():
            # skip blocks present in ignore_list
            # or blocks not represented by lists
            if key in ignore_list or not isinstance(value, list):
                continue
            block_list = []
            # sort each config block
            i = 1
            for block in value[:]:
                # config block must be a dict
                # with a key named "config_name"
                # otherwise it's skipped with a warning
                if not isinstance(block, dict) or 'config_name' not in block:
                    json_block = json.dumps(block, indent=4)
                    print('Unrecognized config block was skipped:\n\n'
                          '{0}\n\n'.format(json_block))
                    continue
                block['.type'] = block.pop('config_name')
                block['.name'] = block.pop('config_value', '{0}_{1}'.format(block['.type'], i))
                block_list.append(sorted_dict(block))
                i += 1
            extra_packages[key] = block_list
        if extra_packages:
            return sorted_dict(extra_packages).items()
        # return empty tuple if no extra packages are used
        return tuple()
