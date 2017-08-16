from .interface import bssid, encryption, ssid


def ap_no_encryption(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for encryption None as the intermediate dict
    """
    return {
        'ssid': ssid(interface),
        'priority': 100,
        'key_mgmt': [{'name': 'NONE'}],
    }


def ap_wpa2_personal(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for wpa2_personal as the indernediate dict
    in ``access_point`` mode
    """
    base = ap_no_encryption(interface)
    base.update({'psk': encryption(interface)['key']})
    return base


def ap_wpa2_enterprise(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for wpa2_personal as the indernediate dict
    in ``access_point`` mode
    """
    return ap_no_encryption(interface)


def sta_no_encryption(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for encryption None as the intermediate dict
    in ``station`` mode
    """
    return {
        'ssid': ssid(interface),
        'priority': 100,
        'key_mgmt': [{'name': 'NONE'}],
    }


def sta_wpa2_personal(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for wpa2_personal as the indernediate dict
    in ``station`` mode
    """
    base = sta_no_encryption(interface)
    base.update({
        'psk': encryption(interface)['key'],
        'eap': [{'status': 'disabled'}],
        'key_mgmt': [{'name': 'WPA-PSK'}],
        'pairwise': [{'name': 'CCMP'}],
        'phase2=auth': 'MSCHAPV2',
        'proto': [{'name': 'RSN'}],
    })
    return base


def sta_wpa2_enterprise(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for wpa2_enterprise as the intermediate dict
    """
    base = ap_no_encryption(interface)
    base.update({
        'bssid': bssid(interface),
        'phase2=auth': 'MSCHAPV2',
        'eap': [
            {
                'name': 'TTLS',
                'status': 'enabled',
            },
        ],
        'password': encryption(interface)['password'],
        'identity': encryption(interface)['identity'],
        'pairwise': [{'name': 'CCMP'}],
        'proto': [{'name': 'RSN'}],
        'key_mgmt': [{'name': 'WPA-EAP'}],
    })
    return base


available_mode_authentication = {
    'access_point': {
        'none': ap_no_encryption,
        'wpa2_personal': ap_wpa2_personal,
        'wpa2_enterprise': ap_wpa2_enterprise,
    },
    'station': {
        'none': sta_no_encryption,
        'wpa2_personal': sta_wpa2_personal,
        'wpa2_enterprise': sta_wpa2_enterprise,
    },
}
