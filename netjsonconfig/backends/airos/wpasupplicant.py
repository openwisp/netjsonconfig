from interface import encryption, ssid


def ap_no_encryption(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for encryption None as the intermediate dict
    """
    return {
        'ssid': ssid(interface),
        'priority': 100,
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
        'psk': encryption(interface)['key'],
        'ssid': ssid(interface),
        'priority': 100,
        'key_mgmt': [
            {
                'name': 'NONE',
            },
        ],
    }


def ap_wpa2_enterprise(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for wpa2_personal as the indernediate dict
    in ``access_point`` mode
    """
    return {
        'ssid': ssid(interface),
    }


# STATION
def sta_no_encryption(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for encryption None as the intermediate dict
    in ``station`` mode
    """
    return {
        'ssid': ssid(interface),
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
        'ssid': ssid(interface),
        'psk': encryption(interface)['key'],
        # no advanced authentication methods
        # with psk
        'eap': [
            {
                'status': 'disabled',
            },
        ],
        'key_mgmt': [
            {
                'name': 'WPA-PSK',
            },
        ],
        'pairwise': [
            {
                'name': 'CCMP',
            },
        ],
        # this may be not necessary
        # as further authentication is not
        # supported
        'phase2=auth': 'MSCHAPV2',
        'priority': 100,
        'proto': [
            {
                'name': 'RSN',
            },
        ],
    }


def sta_wpa2_enterprise(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for wpa2_enterprise as the intermediate dict
    """
    return {
        'ssid': ssid(interface),
        'phase2=auth': 'MSCHAPV2',
        'eap': [
            {
                'name': 'TTLS',
                'status': 'enabled',
            },
        ],
        'password': encryption(interface)['password'],
        'identity': encryption(interface)['identity'],
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
        'wpa2_enterprise': ap_wpa2_enterprise,
    },
    'station': {
        'none': sta_no_encryption,
        'wpa2_personal': sta_wpa2_personal,
        'wpa2_enterprise': sta_wpa2_enterprise,
    },
}
