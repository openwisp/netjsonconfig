from ipaddress import ip_interface


def autonegotiation(interface):
    """
    Return the configuration for ``autoneg`` on interface
    """
    if interface.get('autoneg'):
        return 'enabled'
    else:
        return 'disabled'


def bridge(interfaces):
    """
    Return the bridge interfaces from the interfaces list
    """
    return [i for i in interfaces if i['type'] == 'bridge']


def bssid(interface):
    """
    Return the interface bssid
    """
    return interface['wireless'].get('bssid', '')


def encryption(interface):
    """
    Return the encryption dict for a wireless interface
    """
    return interface['wireless'].get('encryption', {'protocol': 'none'})


def flowcontrol(interface):
    """
    Return the configuration for ``flowcontrol`` on interface
    """
    if interface.get('flowcontrol'):
        status = 'enabled'
    else:
        status = 'disabled'
    return {
        'rx': {
            'status': status,
        },
        'tx': {
            'status': status,
        },
    }


def hidden_ssid(interface):
    """
    Return wether the ssid is hidden
    """
    if interface['wireless'].get('hidden', False):
        return 'enabled'
    else:
        return 'disabled'


def mode(interface):
    """
    Return wireless interface mode
    """
    return interface['wireless']['mode']


def protocol(interface):
    """
    Return wireless interface encryption
    """
    return encryption(interface)['protocol']


def psk(interface):
    """
    Return the wpa2_personal psk
    """
    return interface['wireless']['encryption']['key']


def radio(interface):
    """
    Return wireless interface's radio name
    """
    return interface['wireless']['radio']


def split_cidr(address):
    """
    Return the address in dict format
    """
    network = ip_interface('{addr}/{mask}'.format(addr=address['address'], mask=address['mask']))
    return {'ip': str(network.ip), 'netmask': str(network.netmask)}


def ssid(interface):
    """
    Return the interface ssid
    """
    return interface['wireless']['ssid']


def stp(interface):
    """
    Return wether the spanning tree protocol is enabled
    """
    if interface.get('stp', False):
        return 'enabled'
    else:
        return 'disabled'


def vlan(interfaces):
    """
    Return the vlan interfaces from the interfaces list
    """
    return [i for i in interfaces if '.' in i['name']]


def wireless(interfaces):
    """
    Return the wireless interfaces from the interfaces list
    """
    return [i for i in interfaces if i['type'] == 'wireless']
