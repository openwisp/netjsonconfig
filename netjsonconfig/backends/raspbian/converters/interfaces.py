from ipaddress import IPv4Interface, ip_network

from ....utils import get_copy
from .base import RaspbianConverter


class Interfaces(RaspbianConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        interfaces = get_copy(self.netjson, self.netjson_key)
        for interface in interfaces:
            result.append(self._get_interface(interface))
        return (('interfaces', result),)

    def _get_interface(self, interface):
        new_interface = {}
        ifname = interface.get('name')
        iftype = interface.get('type')
        new_interface.update({
            'ifname': ifname,
            'iftype': iftype
        })
        if iftype in ['ethernet', 'bridge', 'wireless']:
            addresses = self._get_address(interface)
            new_interface.update({
                'address': addresses
            })
        routes = get_copy(self.netjson, 'routes')
        new_interface.update({
            'mac': interface.get('mac', None),
            'mtu': interface.get('mtu', None),
            'txqueuelen': interface.get('txqueuelen', None),
            'autostart': interface.get('autostart', True),
        })
        if routes:
            route = self._get_route(routes)
            new_interface.update({'route': route})
        # mac = interface.get('mac', False)
        # if mac:
        #     new_interface.update({'mac': mac})
        # mtu = interface.get('mtu', False)
        # if mtu:
        #     new_interface.update({'mtu': mtu})
        # txqueuelen = interface.get('txqueuelen', False)
        # if txqueuelen:
        #     new_interface.update({'txqueuelen': txqueuelen})
        # autostart = interface.get('autostart', True)
        # if autostart:
        #     new_interface.update({'autostart': True})
        # else:
        #     new_interface.update({'autostart': False})
        if iftype == 'wireless' and interface.get('wireless').get('mode') == 'adhoc':
            wireless = interface.get('wireless')
            new_interface.update({
                'essid': wireless.get('ssid'),
                'mode': wireless.get('mode')
            })
        if iftype == 'bridge':
            new_interface.update({
                'bridge_members': interface.get('bridge_members'),
                'stp': interface.get('stp', False)
            })
        return new_interface

    def _get_address(self, interface):
        addresses = interface.get('addresses', False)
        if addresses:
            for address in addresses:
                if address.get('proto') == 'static':
                    if address.get('family') == 'ipv4':

                        address_mask = str(address.get('address')) + '/' + str(address.get('mask'))
                        address['netmask'] = IPv4Interface(address_mask).with_netmask.split('/')[1]
                        del address['mask']
                    if address.get('family') == 'ipv6':
                        address['netmask'] = address['mask']
                        del address['mask']
            return addresses

    def _get_route(self, routes):
        for route in routes:
            if ip_network(route.get('next')).version == 4:
                route['version'] = 4
                destination = IPv4Interface(route['destination']).with_netmask
                dest, dest_mask = destination.split('/')
                route['dest'] = dest
                route['dest_mask'] = dest_mask
                del route['destination']
            elif ip_network(route.get('next')).version == 6:
                route['version'] = 6
            return route
