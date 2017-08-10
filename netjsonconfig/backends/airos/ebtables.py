from .interface import mode, protocol, radio
import copy


def default(interace):
    return {}


def station(interface):
    """
    Returns the configuration for ``ebtables.sys``
    for an interface in ``station`` mode with ``wpa2_enterpise``
    or ``wpa2_personal`` authentication
    """
    return {
        'eap': [
            {
                'devname': radio(interface),
                'status': 'enabled',
            }
        ],
        'eap.status': 'enabled',
    }


_base = {
    'sys': {
        'fw': {'status': 'disabled'},
        'status': 'enabled',
    },
}

_status = {
    'status': 'enabled',
}


_mapping = {
    'access_point': {
        'none': default,
        'wpa2_personal': default,
        'wpa2_enterprise': default,
    },
    'station': {
        'none': default,
        'wpa2_personal': station,
        'wpa2_enterprise': station,
    },
}


def ebtables_from_interface(interface):
    base = copy.deepcopy(_base)
    status = _status.copy()
    base['sys'].update(_mapping[mode(interface)][protocol(interface)](interface))
    return [status, base]
