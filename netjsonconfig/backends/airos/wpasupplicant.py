def no_encryption(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for encryption None as the intermediate dict
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


def wpa2_personal(interface):
    """
    Returns the wpasupplicant.profile.1.network
    for wpa2_personal as the indernediate dict
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


def wpa2_enterprise(interface):
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

available_encryption_protocols = {
    'none': no_encryption,
    'wpa2_personal': wpa2_personal,
    'wpa2_enterprise': wpa2_enterprise,
}
