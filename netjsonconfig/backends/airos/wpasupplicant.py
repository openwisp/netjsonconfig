def ap_no_encryption(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for encryption None as the intermediate dict
    """
    return {
        'ssid': interface['wireless']['ssid'],
        'key_mgmt': [
            {
                'name': 'NONE',
            },
        ],
    }


def ap_wpa2_personal(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for wpa2_personal as the indernediate dict
    in ``access_point`` mode
    """
    return {
        'psk': interface['encryption']['key'],
        'ssid': interface['wireless']['ssid'],
    }


def sta_no_encryption(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for encryption None as the intermediate dict
    in ``station`` mode
    """
    return {
        'ssid': interface['wireless']['ssid'],
        'priority': 100,
        'key_mgmt': [
            {
                'name': 'NONE',
            },
        ],
    }


def sta_wpa2_personal(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for wpa2_personal as the indernediate dict
    in ``station`` mode
    """
    return {
        'phase2=auth': 'MSCHAPV2',
        'eap': [
            {
                'status': 'disabled',
            },
        ],
        'psk': interface['encryption']['key'],
        'pairwise': [
            {
                'name': 'CCMP',
            },
        ],
        'proto': [
            {
                'name': 'RSN',
            },
        ],
        'ssid': interface['wireless']['ssid'],
        'priority': 100,
        'key_mgmt': [
            {
                'name': 'WPA-PSK',
            },
        ],
    }


def sta_wpa2_enterprise(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for wpa2_enterprise as the intermediate dict
    """
    return {
        'phase2=auth': 'MSCHAPV2',
        'eap': [
            {
                'name': 'TTLS',
                'status': 'enabled',
            },
        ],
        'password': 'TODO',
        'identity': 'TODO',
        'anonymous_identity': 'TODO',
        'pairwise': [
            {
                'name': 'CCMP',
            },
        ],
        'proto': [
            {
                'name': 'RSN',
            },
        ],
        'ssid': interface['wireless']['ssid'],
        'priority': 100,
        'key_mgmt': [
            {
                'name': 'WPA-EAP',
            },
        ],
    }


available_mode_authentication = {
    'access_point': {
        'none': ap_no_encryption,
        'wpa2_personal': ap_wpa2_personal,
    },
    'station': {
        'none': sta_no_encryption,
        'wpa2_personal': sta_wpa2_personal,
#        'wpa2_enterprise': sta_wpa2_enterprise,
    },
}
