from .interface import mode, protocol, psk, radio, ssid


def ap_none(interface):
    return {}


def ap_psk(interface):
    result = {
        'devname': radio(interface),
        'driver': 'madwifi',
        'ssid': ssid(interface),
        'wpa': {
            '1.pairwise': 'CCMP',
            'key': [
                {
                    'mgmt': 'WPA-PSK',
                }
            ],
            'mode': 2,
            'psk': psk(interface),
        }
    }
    return result


def sta_none(interface):
    return {}


def sta_psk(interface):
    return {
        'wpa': {
            'psk': psk(interface),
        }
    }


_profile = {}

_profile_from_mode = {
    'access_point': {
        'none': ap_none,
        'wpa2_personal': ap_psk,
    },
    'station': {
        'none': sta_none,
        'wpa2_personal': sta_psk,
    },
}


def profile_from_interface(interface):
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
    },
    'station': {
        'none': {
            'status': 'disabled',
        },
        'wpa2_personal': {
            'status': 'disabled',
        },
    }
}


def status_from_interface(interface):
    status = _status.copy()
    status.update(
            _status_from_mode[mode(interface)][protocol(interface)]
    )
    return status


def bridge_devname(wireless_interface, bridge_interface):
    """
    when in ``access_point`` with ``wpa2_personal`` authentication set also the
    bridge interface name

    TODO: check if in ``netmode=router`` this happens again
    """
    if mode(wireless_interface) == 'access_point' and protocol(wireless_interface) == 'wpa2_personal':
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
