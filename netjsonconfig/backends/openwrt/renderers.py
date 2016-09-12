import json
from copy import deepcopy
from ipaddress import ip_interface, ip_network

from ...utils import sorted_dict
from ..base import BaseRenderer
from ..openvpn.renderers import OpenVpnRenderer as BaseOpenVpnRenderer
from .timezones import timezones


def logical_name(name):
    return name.replace('.', '_').replace('-', '_')


class BaseOpenWrtRenderer(BaseRenderer):
    """
    Base OpenWrt Renderer
    """
    def cleanup(self, output):
        """
        OpenWRT specific output cleanup
        """
        # correct indentation
        output = output.replace('    ', '')\
                       .replace('\noption', '\n\toption')\
                       .replace('\nlist', '\n\tlist')
        # convert True to 1 and False to 0
        output = output.replace('True', '1')\
                       .replace('False', '0')
        # max 2 consecutive \n delimiters
        output = output.replace('\n\n\n', '\n\n')
        # if output is present
        # ensure it always ends with 1 new line
        if output.endswith('\n\n'):
            return output[0:-1]
        return output


class NetworkRenderer(BaseOpenWrtRenderer):
    """
    Renders content importable with:
        uci import network
    """
    def _get_interfaces(self):
        """
        converts interfaces object to UCI interface directives
        """
        interfaces = self.config.get('interfaces', [])
        # this line ensures interfaces are not entirely
        # ignored if they do not contain any address
        default_address = [{'proto': 'none'}]
        # results container
        uci_interfaces = []
        for interface in interfaces:
            counter = 1
            is_bridge = False
            # determine uci logical interface name
            network = interface.get('network')
            uci_name = interface['name'] if not network else network
            # convert dot and dashes to underscore
            uci_name = logical_name(uci_name)
            # determine if must be type bridge
            if interface.get('type') == 'bridge':
                is_bridge = True
                bridge_members = ' '.join(interface['bridge_members'])
            # ensure address list is not never empty, even when 'addresses' is []
            address_list = interface.get('addresses')
            if not address_list:
                address_list = default_address
            # address list defaults to empty list
            for address in address_list:
                # prepare new UCI interface directive
                uci_interface = deepcopy(interface)
                if network:
                    del uci_interface['network']
                if 'mac' in uci_interface:
                    if interface.get('type') != 'wireless':
                        uci_interface['macaddr'] = interface['mac']
                    del uci_interface['mac']
                if 'autostart' in uci_interface:
                    uci_interface['auto'] = interface['autostart']
                    del uci_interface['autostart']
                if uci_interface.get('disabled'):
                    uci_interface['enabled'] = not interface['disabled']
                    del uci_interface['disabled']
                if 'addresses' in uci_interface:
                    del uci_interface['addresses']
                if 'type' in uci_interface:
                    del uci_interface['type']
                if 'wireless' in uci_interface:
                    del uci_interface['wireless']
                # default values
                address_key = None
                address_value = None
                netmask = None
                proto = self.__get_proto(uci_interface, address)
                # add suffix if there is more than one config block
                if counter > 1:
                    name = '{name}_{counter}'.format(name=uci_name, counter=counter)
                else:
                    name = uci_name
                if address.get('family') == 'ipv4':
                    address_key = 'ipaddr'
                elif address.get('family') == 'ipv6':
                    address_key = 'ip6addr'
                    proto = proto.replace('dhcp', 'dhcpv6')
                if address.get('address') and address.get('mask'):
                    address_value = '{address}/{mask}'.format(**address)
                    # do not use CIDR notation when using ipv4
                    # see https://github.com/openwisp/netjsonconfig/issues/54
                    if address.get('family') == 'ipv4':
                        netmask = str(ip_interface(address_value).netmask)
                        address_value = address['address']
                # update interface dict
                uci_interface.update({
                    'name': name,
                    'ifname': interface['name'],
                    'proto': proto,
                    'dns': self.__get_dns_servers(uci_interface, address),
                    'dns_search': self.__get_dns_search(uci_interface, address)
                })
                # bridging
                if is_bridge:
                    uci_interface['type'] = 'bridge'
                    # put bridge members in ifname attribute
                    if bridge_members:
                        uci_interface['ifname'] = bridge_members
                    # if no members, this is an empty bridge
                    else:
                        uci_interface['bridge_empty'] = True
                        del uci_interface['ifname']
                    # ensure type "bridge" is only given to one logical interface
                    is_bridge = False
                # bridge has already been defined
                # but we need to add more references to it
                elif interface.get('type') == 'bridge':
                    # openwrt adds "br-"" prefix to bridge interfaces
                    # we need to take this into account when referring
                    # to these physical names
                    uci_interface['ifname'] = 'br-{0}'.format(interface['name'])
                # delete bridge_members attribtue if bridge is empty
                if uci_interface.get('bridge_members') is not None:
                    del uci_interface['bridge_members']
                # add address if any (with correct option name)
                if address_key and address_value:
                    uci_interface[address_key] = address_value
                # add netmask option (only for IPv4)
                if netmask:
                    uci_interface['netmask'] = netmask
                # merge additional address fields (discard default ones first)
                address_copy = address.copy()
                for key in ['address', 'mask', 'proto', 'family']:
                    if key in address_copy:
                        del address_copy[key]
                uci_interface.update(address_copy)
                # append to interface list
                uci_interfaces.append(sorted_dict(uci_interface))
                counter += 1
        return uci_interfaces

    def __get_proto(self, interface, address):
        """
        determines interface "proto" option
        """
        if 'proto' not in interface:
            # proto defaults to static
            return address.get('proto', 'static')
        else:
            # allow override
            return interface['proto']

    def _get_routes(self):
        routes = self.config.get('routes', [])
        # results container
        uci_routes = []
        counter = 1
        # build uci_routes
        for route in routes:
            # prepare UCI route directive
            uci_route = route.copy()
            del uci_route['device']
            del uci_route['next']
            del uci_route['destination']
            del uci_route['cost']
            network = ip_interface(route['destination'])
            version = 'route' if network.version == 4 else 'route6'
            target = network.ip if network.version == 4 else network.network
            uci_route.update({
                'version': version,
                'name': 'route{0}'.format(counter),
                'interface': route['device'],
                'target': str(target),
                'gateway': route['next'],
                'metric': route['cost'],
                'source': route.get('source')
            })
            if network.version == 4:
                uci_route['netmask'] = str(network.netmask)
            uci_routes.append(sorted_dict(uci_route))
            counter += 1
        return uci_routes

    def _get_ip_rules(self):
        rules = self.config.get('ip_rules', [])
        uci_rules = []
        for rule in rules:
            uci_rule = rule.copy()
            src_net = None
            dest_net = None
            family = 4
            if rule.get('src'):
                src_net = ip_network(rule['src'])
            if rule.get('dest'):
                dest_net = ip_network(rule['dest'])
            if dest_net or src_net:
                family = dest_net.version if dest_net else src_net.version
            uci_rule['block_name'] = 'rule{0}'.format(family).replace('4', '')
            uci_rules.append(sorted_dict(uci_rule))
        return uci_rules

    def __get_dns_servers(self, uci, address):
        # allow override
        if 'dns' in uci:
            return uci['dns']
        # ignore if using DHCP or if "proto" is none
        if address['proto'] in ['dhcp', 'none']:
            return None
        # general setting
        dns = self.config.get('dns_servers', None)
        if dns:
            return ' '.join(dns)

    def __get_dns_search(self, uci, address):
        # allow override
        if 'dns_search' in uci:
            return uci['dns_search']
        # ignore if "proto" is none
        if address['proto'] == 'none':
            return None
        # general setting
        dns_search = self.config.get('dns_search', None)
        if dns_search:
            return ' '.join(dns_search)

    def _get_switches(self):
        uci_switches = []
        for switch in self.config.get('switch', []):
            uci_switch = sorted_dict(deepcopy(switch))
            uci_switch['vlan'] = [sorted_dict(vlan) for vlan in uci_switch['vlan']]
            uci_switches.append(uci_switch)
        return uci_switches

    def _get_globals(self):
        ula_prefix = self.config.get('general', {}).get('ula_prefix', None)
        if ula_prefix:
            return {'ula_prefix': ula_prefix}
        return {}


class SystemRenderer(BaseOpenWrtRenderer):
    """
    Renders content importable with:
        uci import system
    """
    def _get_system(self):
        general = self.config.get('general', {}).copy()
        # ula_prefix is not related to system
        if 'ula_prefix' in general:
            del general['ula_prefix']
        if general:
            timezone_human = general.get('timezone', 'UTC')
            timezone_value = timezones[timezone_human]
            general.update({
                'hostname': general.get('hostname', 'OpenWRT'),
                'timezone': timezone_value,
            })
        return sorted_dict(general)

    def _get_ntp(self):
        return sorted_dict(self.config.get('ntp', {}))

    def _get_leds(self):
        uci_leds = []
        for led in self.config.get('led', []):
            uci_leds.append(sorted_dict(led))
        return uci_leds


class WirelessRenderer(BaseOpenWrtRenderer):
    """
    Renders content importable with:
        uci import wireless
    """
    def _get_radios(self):
        radios = self.config.get('radios', [])
        uci_radios = []
        for radio in radios:
            uci_radio = radio.copy()
            # rename tx_power to txpower
            if 'tx_power' in radio:
                uci_radio['txpower'] = radio['tx_power']
                del uci_radio['tx_power']
            # rename driver to type
            uci_radio['type'] = radio['driver']
            del uci_radio['driver']
            # determine hwmode option
            uci_radio['hwmode'] = self.__get_hwmode(radio)
            del uci_radio['protocol']
            # check if using channel 0, that means "auto"
            if uci_radio['channel'] is 0:
                uci_radio['channel'] = 'auto'
            # determine channel width
            if radio['driver'] == 'mac80211':
                uci_radio['htmode'] = self.__get_htmode(radio)
            del uci_radio['channel_width']
            # ensure country is uppercase
            if uci_radio.get('country'):
                uci_radio['country'] = uci_radio['country'].upper()
            # append sorted dict
            uci_radios.append(sorted_dict(uci_radio))
        return uci_radios

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

    def _get_wifi_interfaces(self):
        # select interfaces that have type == "wireless"
        wifi_interfaces = [i for i in self.config.get('interfaces', [])
                           if 'wireless' in i]
        # results container
        uci_wifi_ifaces = []
        for wifi_interface in wifi_interfaces:
            wireless = wifi_interface['wireless']
            # prepare UCI wifi-iface directive
            uci_wifi = wireless.copy()
            # inherit "disabled" attribute if present
            uci_wifi['disabled'] = wifi_interface.get('disabled')
            # add ifname
            uci_wifi['ifname'] = wifi_interface['name']
            # uci identifier
            uci_wifi['id'] = 'wifi_{0}'.format(logical_name(wifi_interface['name']))
            # rename radio to device
            uci_wifi['device'] = wireless['radio']
            del uci_wifi['radio']
            # mac address override
            if 'mac' in wifi_interface:
                uci_wifi['macaddr'] = wifi_interface['mac']
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
                network = wifi_interface.get('network', wifi_interface['name'])
                uci_wifi['network'] = [network]
            uci_wifi['network'] = ' '.join(uci_wifi['network'])\
                                     .replace('.', '_')\
                                     .replace('-', '_')
            uci_wifi_ifaces.append(sorted_dict(uci_wifi))
        return uci_wifi_ifaces

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


class DefaultRenderer(BaseOpenWrtRenderer):
    """
    Default OpenWrt Renderer
    Allows great flexibility in defining UCI configuration in JSON format
    """
    def _get_custom_packages(self):
        # determine config keys to ignore
        ignore_list = list(self.backend.schema['properties'].keys())
        ignore_list += self.backend.get_renderers()
        # determine custom packages
        custom_packages = {}
        for key, value in self.config.items():
            if key not in ignore_list:
                block_list = []
                # sort each config block
                if isinstance(value, list):
                    for block in value[:]:
                        # config block must be a dict
                        # with a key named "config_name"
                        # otherwise it's skipped with a warning
                        if not isinstance(block, dict) or 'config_name' not in block:
                            json_block = json.dumps(block, indent=4)
                            print('Unrecognized config block was skipped:\n\n'
                                  '{0}\n\n'.format(json_block))
                            continue
                        block_list.append(sorted_dict(block))
                # if not a list just skip
                else:  # pragma: nocover
                    continue
                custom_packages[key] = block_list
        # sort custom packages
        return sorted_dict(custom_packages)


class OpenVpnRenderer(BaseOpenWrtRenderer, BaseOpenVpnRenderer):
    """
    Produces an OpenVPN configuration in UCI format for OpenWRT
    """
    def _transform_vpn(self, vpn):
        config = super(OpenVpnRenderer, self)._transform_vpn(vpn)
        if 'enabled' not in config:
            config['enabled'] = True
        return config
