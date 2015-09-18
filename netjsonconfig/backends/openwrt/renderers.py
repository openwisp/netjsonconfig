from collections import OrderedDict
from ipaddress import ip_interface

from .timezones import timezones
from ..base import BaseRenderer


class NetworkRenderer(BaseRenderer):
    """
    Renders content importable with:
        uci import network
    """

    def _get_interfaces(self):
        interfaces = self.config.get('interfaces', [])
        # results container
        uci_interfaces = []
        for interface in interfaces:
            counter = 1
            # ensure uci interface name is valid
            uci_name = interface['name'].replace('.', '_')
            # address list defaults to empty list
            for address in interface.get('addresses', []):
                address_key = None
                address_value = None
                # proto defaults to static
                proto = address.get('proto', 'static')
                # add suffix if there is more than one config block
                if counter > 1:
                    name = '{name}_{counter}'.format(name=uci_name, counter=counter)
                else:
                    name = uci_name
                if address['family'] == 'ipv4':
                    address_key = 'ipaddr'
                elif address['family'] == 'ipv6':
                    address_key = 'ip6addr'
                    proto = proto.replace('dhcp', 'dhcpv6')
                if address.get('address') and address.get('mask'):
                    address_value = '{address}/{mask}'.format(**address)
                # append to results
                uci_interfaces.append({
                    'uci_name': name,
                    'name': interface['name'],
                    'proto': proto,
                    'address_key': address_key,
                    'address_value': address_value
                })
                counter += 1
        return uci_interfaces

    def _get_routes(self):
        routes = self.config.get('routes', [])
        # results container
        uci_routes = []
        counter = 1
        # build uci_routes
        for route in routes:
            network = ip_interface(route['destination'])
            version = 'route' if network.version == 4 else 'route6'
            target = network.ip if network.version == 4 else network.network
            uci_routes.append({
                'version': version,
                'name': 'route{0}'.format(counter),
                'interface': route['device'],
                'target': str(target),
                'netmask': str(network.netmask),
                'gateway': route['next'],
                'metric': route.get('cost'),
                'source': route.get('source')
            })
            counter += 1
        return uci_routes


class SystemRenderer(BaseRenderer):
    """
    Renders content importable with:
        uci import system
    """

    def _get_system(self):
        general = self.config.get('general', None)
        if general:
            timezone_human = general.get('timezone', 'Coordinated Universal Time')
            timezone_value = timezones[timezone_human]
            return {
                'hostname': general.get('hostname', 'OpenWRT'),
                'timezone': timezone_value,
            }
        return None


class WirelessRenderer(BaseRenderer):
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
            uci_radio['txpower'] = radio['tx_power']
            del uci_radio['tx_power']
            # rename driver to type
            uci_radio['type'] = radio['driver']
            del uci_radio['driver']
            # determine hwmode option
            uci_radio['hwmode'] = self.__get_hwmode(radio)
            del uci_radio['protocol']
            # determine channel width
            if radio['driver'] == 'mac80211':
                uci_radio['htmode'] = self.__get_htmode(radio)
            elif radio['driver'] in ['ath9k', 'ath5k']:
                uci_radio['chanbw'] = radio['channel_width']
            del uci_radio['channel_width']
            # ensure country is uppercase
            if uci_radio.get('country'):
                uci_radio['country'] = uci_radio['country'].upper()
            # covert disabled boolean to integer
            if uci_radio.get('disabled'):
                uci_radio['disabled'] = int(uci_radio['disabled'])
            # sort keys in OrderedDict
            uci_radios.append(OrderedDict(sorted(uci_radio.items())))
        return uci_radios

    def __get_hwmode(self, radio):
        """
        possible return values are: 11a, 11b, 11g
        """
        protocol = radio['protocol']
        if protocol not in ['802.11n', '802.11ac']:
            return protocol.replace('802.', '')
        elif protocol == '802.11n' and radio['channel'] <= 13:
            return '11g'
        return '11a'

    def __get_htmode(self, radio):
        """
        only for mac80211 driver
        """
        if radio['protocol'] == '802.11n':
            return 'HT{0}'.format(radio['channel_width'])
        elif radio['protocol'] == '802.11ac':
            return 'VHT{0}'.format(radio['channel_width'])
        # disables n
        return 'NONE'
