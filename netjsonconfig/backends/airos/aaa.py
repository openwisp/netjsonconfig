from .interface import mode, protocol, psk, radio, ssid


def ap_none(interface):
    """
    Returns the configuration for ``aaa``
    when in ``access_point`` mode without authentication
    """
    return {}


def ap_psk(interface):
    """
    Returns the configuration for ``aaa``
    when in ``access_point`` mode with psk authentication
    """
    result = {
        'devname': radio(interface),
        'driver': 'madwifi',
        'ssid': ssid(interface),
        'wpa': {
            '1.pairwise': 'CCMP',
            'key': [{'mgmt': 'WPA-PSK'}],
            'mode': 2,
            'psk': psk(interface),
        }
    }
    return result


def ap_eap(interface):
    """
    Return the configuration for ``aaa``
    when in ``access_point`` mode with eap authentication
    """
    return {
        'devname': radio(interface),
        'driver': 'madwifi',
        'ssid': ssid(interface),
        'wpa': {
            '1.pairwise': 'CCMP',
            'key': [{'mgmt': 'WPA-EAP'}],
            'mode': 2,
        },
    }


def sta_none(interface):
    """
    Return the configuration for ``aaa``
    when in station mode without authentication
    """
    return {}


def sta_psk(interface):
    """
    Return the configuration for ``aaa``
    when in station mode with psk authentication
    """
    return {
        'wpa': {
            'psk': psk(interface),
        }
    }


def sta_eap(interface):
    """
    Return the configuration for ``aaa``
    when in station mode with eap authentication
    """
    return {}


_profile = {}

_profile_from_mode = {
    'access_point': {
        'none': ap_none,
        'wpa2_personal': ap_psk,
        'wpa2_enterprise': ap_eap,
    },
    'station': {
        'none': sta_none,
        'wpa2_personal': sta_psk,
        'wpa2_enterprise': sta_eap,
    },
}


def profile_from_interface(interface):
    """
    Returns the ``aaa`` configuration for interface
    """
    profile = _profile.copy()
    profile.update(
            _profile_from_mode[mode(interface)][protocol(interface)](interface)
    )
    return profile


_status = {}

_status_from_mode = {
    'access_point': {
        'none': {
            'status': 'disabled',
        },
        'wpa2_personal': {
            'status': 'enabled',
        },
        'wpa2_enterprise': {
            'status': 'enabled',
        },
    },
    'station': {
        'none': {
            'status': 'disabled',
        },
        'wpa2_personal': {
            'status': 'disabled',
        },
        'wpa2_enterprise': {
            'status': 'disabled',
        },
    }
}


def status_from_interface(interface):
    """
    Returns ``aaa.status`` from interface
    """
    status = _status.copy()
    status.update(
            _status_from_mode[mode(interface)][protocol(interface)]
    )
    return status


def bridge_devname(wireless_interface, bridge_interface):
    """
    when in ``access_point`` with authentication set also the
    bridge interface name

    TODO: check if in ``netmode=router`` this happens again
    """
    if mode(wireless_interface) == 'access_point' and protocol(wireless_interface) != 'none':
        return {
            'br': {
                'devname': bridge_interface['name'],
            }
        }
    else:
        return {}


__all__ = [
    bridge_devname,
    profile_from_interface,
    status_from_interface,
]
