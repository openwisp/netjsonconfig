from ipaddress import ip_interface

from .timezones import timezones
from ..base import BaseRenderer
from ...utils import sorted_dict


class NetworkRenderer(BaseRenderer):
    """
    Renders content importable with:
        uci import network
    """

    def _get_interfaces(self):
        """
        converts interfaces object to UCI interface directives
        """
        interfaces = self.config.get('interfaces', [])
        # results container
        uci_interfaces = []
        for interface in interfaces:
            counter = 1
            # ensure uci interface name is valid
            uci_name = interface['name'].replace('.', '_')
            # address list defaults to empty list
            for address in interface.get('addresses', []):
                # prepare new UCI interface directive
                uci_interface = interface.copy()
                if uci_interface.get('addresses'):
                    del uci_interface['addresses']
                if uci_interface.get('type'):
                    del uci_interface['type']
                if uci_interface.get('wireless'):
                    del uci_interface['wireless']
                # default values
                address_key = None
                address_value = None
                # proto defaults to static
                proto = address.get('proto', 'static')
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
                # update interface dict
                uci_interface.update({
                    'name': name,
                    'ifname': interface['name'],
                    'proto': proto
                })
                # add address if any (with correct option name)
                if address_key and address_value:
                    uci_interface[address_key] = address_value
                # append to interface list
                uci_interfaces.append(sorted_dict(uci_interface))
                counter += 1
        return uci_interfaces

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
            if uci_route.get('cost'):
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
                'metric': route.get('cost'),
                'source': route.get('source')
            })
            if network.version == 4:
                uci_route['netmask'] = str(network.netmask)
            uci_routes.append(sorted_dict(uci_route))
            counter += 1
        return uci_routes


class SystemRenderer(BaseRenderer):
    """
    Renders content importable with:
        uci import system
    """

    def _get_system(self):
        general = self.config.get('general', {}).copy()
        if general:
            timezone_human = general.get('timezone', 'Coordinated Universal Time')
            timezone_value = timezones[timezone_human]
            general.update({
                'hostname': general.get('hostname', 'OpenWRT'),
                'timezone': timezone_value,
            })
        return sorted_dict(general)


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
            # append sorted dict
            uci_radios.append(sorted_dict(uci_radio))
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

    def _get_wifi_interfaces(self):
        wifi_interfaces = [i for i in self.config.get('interfaces', []) if 'wireless' in i]
        # results container
        uci_wifi_ifaces = []
        for wifi_interface in wifi_interfaces:
            wireless = wifi_interface['wireless']
            # prepare UCI wifi-iface directive
            uci_wifi = wireless.copy()
            if uci_wifi.get('encryption'):
                del uci_wifi['encryption']
            # rename radio to device
            uci_wifi['device'] = wireless['radio']
            del uci_wifi['radio']
            # determine mode
            modes = {
                'access_point': 'ap',
                'station': 'sta',
                'adhoc': 'adhoc',
                'wds': 'wds',
                'monitor': 'monitor',
                '802.11s': 'mesh'
            }
            uci_wifi['mode'] = modes[wireless['mode']]
            uci_wifi['network'] = wifi_interface['name']
            uci_wifi_ifaces.append(sorted_dict(uci_wifi))
        return uci_wifi_ifaces
