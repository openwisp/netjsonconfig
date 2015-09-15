from ..base import BaseRenderer


class NetworkRenderer(BaseRenderer):
    """
    Renders content importable with:
        uci import network
    """
    block_name = 'network'

    def get_context(self):
        interfaces = self.config.get('interfaces')
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
        return {'interfaces': uci_interfaces}
