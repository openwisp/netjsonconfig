from ....utils import get_copy
from .base import RaspbianConverter
from ipaddress import IPv4Interface


class Interfaces(RaspbianConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        interfaces = get_copy(self.netjson, self.netjson_key)
        for interface in interfaces:
            new_interface = {}
            ifname = interface.get('name')
            iftype = interface.get('type')
            new_interface.update({
                'ifname': ifname,
                'iftype': iftype
            })
            if iftype in ['ethernet', 'bridge', 'loopback']:
                addresses = self._get_address(interface)
                new_interface.update({
                    'address': addresses
                })
            mac = interface.get('mac', False)
            if mac:
                new_interface.update({'mac': mac})
            mtu = interface.get('mtu', False)
            if mtu:
                new_interface.update({'mtu': mtu})
            txqueuelen = interface.get('txqueuelen', False)
            if txqueuelen:
                new_interface.update({'txqueuelen': txqueuelen})
            autostart = interface.get('autostart', False)
            if autostart:
                new_interface.update({'autostart': autostart})
            if iftype == 'wireless' and interface.get('wireless').get('mode') == 'adhoc':
                wireless = interface.get('wireless')
                new_interface.update({
                    'essid': wireless.get('ssid'),
                    'mode': wireless.get('mode')
                })
            if iftype == 'bridge':
                new_interface.update({
                    'bridge_members': interface.get('bridge_members')
                })
            result.append(new_interface)
        return (('interfaces', result),)

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
