from ipaddress import ip_interface


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
    return interface['wireless']['encryption']['protocol']


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


    """
    """


def ssid(interface):
    """
    Return the interface ssid
    """
    return interface['wireless']['ssid']


def wireless(interfaces):
    """
    Return the wireless interfaces from the interfaces list
    """
    return [i for i in interfaces if i['type'] == 'wireless']
