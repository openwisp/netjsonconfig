from collections import OrderedDict
from copy import deepcopy
from ipaddress import ip_address, ip_interface

from ..schema import schema
from .base import OpenWrtConverter


class Interfaces(OpenWrtConverter):
    netjson_key = 'interfaces'
    intermediate_key = 'network'
    _uci_types = ['interface', 'globals']
    _bridge_interface_options = {
        'stp': [
            'stp',
            'forward_delay',
            'hello_time',
            'priority',
            'ageing_time',
            'max_age',
        ],
        'igmp_snooping': [
            'igmp_snooping',
            'multicast_querier',
            'query_interval',
            'query_response_interval',
            'last_member_interval',
            'hash_max',
            'robustness',
        ],
        'all': ['vlan_filtering', 'macaddr'],
    }

    def to_intermediate_loop(self, block, result, index=None):
        result.setdefault('network', [])
        uci_name = self._get_uci_name(block.get('network') or block['name'])
        address_list = self.__intermediate_addresses(block)
        interface = self.__intermediate_interface(block, uci_name)
        uci_new_bridge = self.__intermediate_new_bridge(interface)
        if uci_new_bridge:
            result['network'].append(self.sorted_dict(uci_new_bridge))
        # create one or more "config interface" UCI blocks
        i = 1
        for address in address_list:
            uci_interface = deepcopy(interface)
            # add suffix to logical name when
            # there is more than one interface
            if i > 1:
                uci_interface['.name'] = '{name}_{i}'.format(name=uci_name, i=i)
            uci_interface.update(
                {
                    'dns': self.__intermediate_dns_servers(uci_interface, address),
                    'dns_search': self.__intermediate_dns_search(
                        uci_interface, address
                    ),
                    'proto': self.__intermediate_proto(uci_interface, address),
                }
            )
            uci_interface = self.__intermediate_bridge(uci_interface, i)
            if address:
                uci_interface.update(address)
            result.setdefault('network', [])
            result['network'].append(self.sorted_dict(uci_interface))
            i += 1
        return result

    def __intermediate_addresses(self, interface):
        """
        converts NetJSON address to
        UCI intermediate data structure
        """
        # wireguard interfaces need a different format
        if interface.get('type') == 'wireguard':
            return self.__intermediate_wireguard_addresses(interface)
        address_list = self.get_copy(interface, 'addresses')
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
                dhcp.append(self.__intermediate_address(address))
                continue
            if 'gateway' in address:
                uci_key = 'gateway' if family == 'ipv4' else 'ip6gw'
                interface[uci_key] = address['gateway']
            # static
            address_key = 'ipaddr' if family == 'ipv4' else 'ip6addr'
            static.setdefault(address_key, [])
            static[address_key].append('{address}/{mask}'.format(**address))
            static.update(self.__intermediate_address(address))
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

    def __intermediate_wireguard_addresses(self, interface):
        addresses = interface.pop('addresses')
        address_list = []
        for address_dict in addresses:
            address = address_dict['address']
            if 'mask' in address_dict:
                address = f'{address}/{address_dict["mask"]}'
            address_list.append(address)
        static = {'addresses': address_list, 'proto': 'wireguard'}
        return [static]

    def __intermediate_interface(self, interface, uci_name):
        """
        converts NetJSON interface to
        UCI intermediate data structure
        """
        interface.update({'.type': 'interface', '.name': uci_name})
        interface['ifname'] = interface.pop('name')
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
        # specific transformation
        type_ = self._get_uci_name(interface["type"])
        method = getattr(self, f'_intermediate_{type_}', None)
        if method:
            interface = method(interface)
        return interface

    def _intermediate_modem_manager(self, interface):
        interface['proto'] = 'modemmanager'
        interface['pincode'] = interface.pop('pin', None)
        return interface

    def _intermediate_wireguard(self, interface):
        interface['proto'] = 'wireguard'
        interface['listen_port'] = interface.pop('port', None)
        del interface['ifname']
        return interface

    def _intermediate_vxlan(self, interface):
        interface['proto'] = 'vxlan'
        interface['peeraddr'] = interface.pop('vtep')
        interface['vid'] = interface.pop('vni')
        return interface

    _address_keys = ['address', 'mask', 'family', 'gateway']

    def __intermediate_address(self, address):
        """
        deletes NetJSON address keys
        """
        for key in self._address_keys:
            if key in address:
                del address[key]
        return address

    def __intermediate_new_bridge(self, interface):
        """
        Converts NetJSON bridge to intermediate
        data structure compatible with new syntax
        introduced in OpenWrt 21.
        """

        def _add_additional_options(property_name, property_options, bridge, interface):
            if interface.get(property_name, False):
                bridge[property_name] = True
                for option in property_options:
                    if interface.get(option):
                        bridge[option] = interface[option]

        def _add_l2_options(bridge, interface):
            l2_options = [
                'rpfilter',
                'txqueuelen',
                'neighreachabletime',
                'neighgcstaletime',
                'neighlocktime',
                'igmpversion',
                'mldversion',
                'promisc',
                'acceptlocal',
                'sendredirects',
                'multicast',
            ]
            for option in l2_options:
                if option in interface:
                    bridge[option] = interface.pop(option)

        if interface['type'] != 'bridge':
            return
        bridge = {
            '.type': 'device',
            '.name': 'device_{}'.format(interface['.name']),
            'name': interface['ifname'],
            'type': 'bridge',
        }
        # Only add STP options if STP is enabled
        _add_additional_options(
            'stp', self._bridge_interface_options['stp'], bridge, interface
        )

        # Only add IGMP snooping options if IGMP snooping is enabled
        _add_additional_options(
            'igmp_snooping',
            self._bridge_interface_options['igmp_snooping'],
            bridge,
            interface,
        )

        # Add L2 options added in OpenWrt 21
        _add_l2_options(bridge, interface)

        for option in self._bridge_interface_options['all']:
            if option in interface:
                bridge[option] = interface[option]
        bridge['ports'] = interface.get('bridge_members', [])
        if bridge['ports'] == []:
            bridge['bridge_empty'] = True
            del bridge['ports']
        return self.sorted_dict(bridge)

    def __clean_intermediate_bridge(self, interface):
        """
        Removes options that are not required in the configuration.
        """
        if not interface.get('igmp_snooping', False):
            for option in self._bridge_interface_options['igmp_snooping']:
                interface.pop(option, None)
        if not interface.get('stp', False):
            for option in self._bridge_interface_options['stp']:
                interface.pop(option, None)

    def __intermediate_bridge(self, interface, i):
        """
        converts NetJSON bridge to
        UCI intermediate data structure
        """
        # ensure type "bridge" is only given to one logical interface
        if interface['type'] == 'bridge' and i < 2:
            bridge_members = ' '.join(interface.pop('bridge_members'))
            interface['device'] = interface['ifname']
            # put bridge members in ifname attribute
            if bridge_members:
                interface['ifname'] = bridge_members
            # if no members, this is an empty bridge
            else:
                interface['bridge_empty'] = True
                del interface['ifname']
            self.__clean_intermediate_bridge(interface)
        # bridge has already been defined
        # but we need to add more references to it
        elif interface['type'] == 'bridge' and i >= 2:
            # openwrt adds "br-" prefix to bridge interfaces
            # we need to take this into account when referring
            # to these physical names
            if 'br-' not in interface['ifname']:
                interface['ifname'] = 'br-{ifname}'.format(**interface)
            # do not repeat bridge attributes (they have already been processed)
            repeated_options = (
                ['type', 'bridge_members', 'gateway']
                + self._bridge_interface_options['stp']
                + self._bridge_interface_options['igmp_snooping']
            )
            for attr in repeated_options:
                if attr in interface:
                    del interface[attr]
        elif interface['type'] != 'bridge':
            del interface['type']
        return interface

    def __intermediate_proto(self, interface, address):
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

    def __intermediate_dns_servers(self, uci, address):
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

    def __intermediate_dns_search(self, uci, address):
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

    def __update_existing_bridge(self, interface, result):
        """
        The UCI configuration might contain configuration
        for bridge in both syntaxes (pre and post OpenWrt 21).
        This method updates the existing bridge NetJSON if it
        finds a repetitive bridge definition.
        Returns "True" if the method updated an existing bridge.
        Otherwise, returns "False".
        """
        if not interface['type'] == 'bridge':
            return False
        for _interface in result['interfaces']:
            if (
                interface['name'] == _interface['name']
                and interface['type'] == _interface['type']
            ):
                _interface.update(interface)
                return True
        return False

    def to_netjson_loop(self, block, result, index):
        _type = block.get('.type')
        if _type == 'globals':
            ula_prefix = block.get('ula_prefix')
            if ula_prefix:
                result = {'general': {'ula_prefix': ula_prefix}}
                _name = block.pop('.name')
                if _name != 'globals':
                    result['general']['globals_id'] = _name
        elif _type == 'interface':
            interface = self.__netjson_interface(block)
            self.__netjson_dns(interface, result)
            result.setdefault('interfaces', [])
            if not self.__update_existing_bridge(interface, result):
                result['interfaces'].append(interface)
        return result

    def __netjson_interface(self, interface):
        del interface['.type']
        interface['network'] = interface.pop('.name')
        interface['name'] = interface.pop('ifname', interface['network'])
        interface['type'] = self.__netjson_type(interface)
        interface = self.__netjson_addresses(interface)
        if 'auto' in interface:
            interface['autostart'] = interface.pop('auto') == '1'
        if 'enabled' in interface:
            interface['disabled'] = interface.pop('enabled') == '0'
        if 'mtu' in interface:
            interface['mtu'] = int(interface['mtu'])
        if 'macaddr' in interface:
            interface['mac'] = interface.pop('macaddr')
        if interface['network'] == self._get_uci_name(interface['name']):
            del interface['network']
        # specific transformation
        method = getattr(self, f'_netjson_{interface.get("proto")}', None)
        if method:
            interface = method(interface)
        return interface

    def __clean_netjson_bridge(self, interface):
        """
        The two bridge declaration syntaxes (pre and post OpenWrt 21)
        defines bridge members differently.
        This method parses bridge members from both syntaxes.
        It also cleans "name" and "network" field for OpenWrt 21 syntax.
        """
        interface.pop('device', None)
        if interface.pop('bridge_21', False):
            interface['bridge_members'] = interface.pop('ports', [])
            interface['name'] = interface['name'].lstrip('device_')
            interface['network'] = interface['network'].lstrip('device_')
            # Parse L2 config options added in OpenWrt 21
            for option in [
                'txqueuelen',
                'neighreachabletime',
                'neighgcstaletime',
                'neighlocktime',
                'igmpversion',
                'mldversion',
            ]:
                try:
                    interface[option] = int(interface[option])
                except ValueError:
                    del interface[option]
                except KeyError:
                    continue
            for option in [
                'promisc',
                'acceptlocal',
                'sendredirects',
                'multicast',
            ]:
                try:
                    interface[option] = interface[option] == '1'
                except KeyError:
                    continue
        else:
            interface['bridge_members'] = interface['name'].split()

    def __netjson_type(self, interface):
        if 'type' in interface and interface['type'] == 'bridge':
            self.__clean_netjson_bridge(interface)
            interface['name'] = 'br-{0}'.format(interface['network'])
            # cleanup automatically generated "br_" network prefix
            interface['name'] = interface['name'].replace('br_', '')
            for option in [
                'stp',
                'igmp_snooping',
                'multicast_querier',
                'vlan_filtering',
            ]:
                if option in interface:
                    interface[option] = interface[option] == '1'
            for option in [
                'forward_delay',
                'hello_time',
                'max_age',
                'priority',
                'query_interval',
                'query_response_interval',
                'last_member_interval',
                'hash_max',
                'robustness',
            ]:
                if option in interface:
                    try:
                        interface[option] = int(interface[option])
                    except ValueError:
                        del interface[option]
            if interface.pop('bridge_empty', None) == '1':
                interface['bridge_members'] = []
            return 'bridge'
        if interface['name'] in ['lo', 'lo0', 'loopback']:
            return 'loopback'
        return 'ethernet'

    def __netjson_addresses(self, interface):
        proto = interface.get('proto', 'none')
        address_protos = ['static', 'dhcp', 'dhcpv6', 'none']
        if 'proto' in interface and proto in address_protos:
            del interface['proto']
        if 'ipaddr' not in interface and 'ip6addr' not in interface and proto == 'none':
            return interface
        if proto not in address_protos:
            interface['type'] = 'other'
        return self._add_netjson_addresses(interface, proto)

    def _add_netjson_addresses(self, interface, proto):
        addresses = []
        ipv4 = interface.pop('ipaddr', [])
        ipv6 = interface.pop('ip6addr', [])
        if not isinstance(ipv4, list):
            netmask = interface.pop('netmask', 32)
            parsed_ip = self.__netjson_parse_ip(ipv4, netmask)
            ipv4 = [parsed_ip] if parsed_ip else []
        if not isinstance(ipv6, list):
            netmask = interface.pop('netmask', 128)
            parsed_ip = self.__netjson_parse_ip(ipv6, netmask)
            ipv6 = [parsed_ip] if parsed_ip else []
        if proto.startswith('dhcp'):
            family = 'ipv4' if proto == 'dhcp' else 'ipv6'
            addresses.append({'proto': 'dhcp', 'family': family})
        for address in ipv4 + ipv6:
            address = self.__netjson_parse_ip(address)
            if not address:
                continue
            addresses.append(self.__netjson_address(address, interface))
        if addresses:
            interface['addresses'] = addresses
        return interface

    def _netjson_dialup(self, interface):
        interface['type'] = 'dialup'
        return interface

    _modem_manager_schema = schema['definitions']['modemmanager_interface']['allOf'][0]

    def _netjson_modem_manager(self, interface):
        del interface['proto']
        interface['type'] = 'modem-manager'
        interface['pin'] = interface.pop('pincode', None)
        return self.type_cast(interface, schema=self._modem_manager_schema)

    _netjson_modemmanager = _netjson_modem_manager

    _wireguard_schema = schema['definitions']['wireguard_interface']['allOf'][0]

    def _netjson_wireguard(self, interface):
        interface['type'] = interface.pop('proto', None)
        interface['port'] = interface.pop('listen_port', None)
        addresses = []
        for address in interface['addresses']:
            cidr = ip_interface(address)
            addresses.append(
                {
                    'address': str(cidr.ip),
                    'mask': cidr.network.prefixlen,
                    'proto': 'static',
                    'family': f'ipv{cidr.ip.version}',
                }
            )
        interface['addresses'] = addresses
        return self.type_cast(interface, schema=self._wireguard_schema)

    _vxlan_schema = schema['definitions']['vxlan_interface']['allOf'][0]

    def _netjson_vxlan(self, interface):
        interface['type'] = interface.pop('proto', None)
        interface['vtep'] = interface.pop('peeraddr', None)
        interface['vni'] = interface.pop('vid', None)
        interface['port'] = interface['port']
        return self.type_cast(interface, schema=self._vxlan_schema)

    def __netjson_address(self, address, interface):
        ip = ip_interface(address)
        family = 'ipv{0}'.format(ip.version)
        netjson = OrderedDict(
            (
                ('address', str(ip.ip)),
                ('mask', ip.network.prefixlen),
                ('proto', 'static'),
                ('family', family),
            )
        )
        uci_gateway_key = 'gateway' if family == 'ipv4' else 'ip6gw'
        gateway = interface.get(uci_gateway_key, None)
        if gateway and ip_address(gateway) in ip.network:
            netjson['gateway'] = gateway
            del interface[uci_gateway_key]
        return netjson

    def __netjson_parse_ip(self, ip, netmask=32):
        if '/' in ip:
            parts = ip.split('/')
            ip = parts[0]
            netmask = parts[1] or netmask
        if ip and netmask:
            return '{0}/{1}'.format(ip, netmask)
        else:
            return None

    def __netjson_dns(self, interface, result):
        key_mapping = {'dns': 'dns_servers', 'dns_search': 'dns_search'}
        for uci_key, netjson_key in key_mapping.items():
            if uci_key not in interface:
                continue
            items = interface.pop(uci_key)
            if isinstance(items, str):
                items = items.split()
            result.setdefault(netjson_key, [])
            result[netjson_key] += items


for proto in [
    '3g',
    '6in4',
    'aiccu',
    'l2tp',
    'ncm',
    'ppp',
    'pppoa',
    'pppoe',
    'pptp',
    'qmi',
    'wwan',
]:
    setattr(Interfaces, f'_netjson_{proto}', Interfaces._netjson_dialup)
