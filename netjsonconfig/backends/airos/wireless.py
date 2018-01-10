from .interface import bssid, hidden_ssid, radio, ssid

_wireless_base = {
    'addmtikie': 'enabled',
    'devname': '',
    'hide_ssid': '',
    'l2_isolation': 'disabled',
    'mac_acl': {
        'policy': 'allow',
        'status': 'disabled',
    },
    'mcast': {'enhance': 0},
    'rate': {
        'auto': 'enabled',
        'mcs': -1,
    },
    'security': {'type': 'none'},
    'signal_led1': 75,
    'signal_led2': 50,
    'signal_led3': 25,
    'signal_led4': 15,
    'signal_led_status': 'enabled',
    'ssid': '',
    'status': '',
    'wds': {'status': 'enabled'},
}


def status(interface):
    """
    Return the ``wireless`` status
    """
    if interface.get('disabled'):
        return 'disabled'
    else:
        return 'enabled'


def access_point(wlan):
    """
    Return the configuration for a wireless lan in ``access_point`` mode
    """
    base = _wireless_base.copy()
    base.update({
        'devname': radio(wlan),
        'hide_ssid': hidden_ssid(wlan),
        'ssid': ssid(wlan),
        'status': status(wlan),
    })
    return base


def station(wlan):
    """
    Return the configuration for a wireless lan in ``station`` mode
    """
    base = _wireless_base.copy()
    base.update({
        'ap': bssid(wlan),
        'devname': radio(wlan),
        'hide_ssid': hidden_ssid(wlan),
        'ssid': ssid(wlan),
        'status': status(wlan),
    })
    return base


wireless_available_mode = {
    'access_point': access_point,
    'station': station,
}
