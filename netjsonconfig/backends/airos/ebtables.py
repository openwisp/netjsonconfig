import copy

from .interface import mode, protocol, radio


_base = {
    'sys': {
        'fw': {'status': 'disabled'},
        'status': 'enabled',
    },
}


def default(interace):
    return {}


def station(interface):
    """
    Returns the configuration for ``ebtables.sys``
    for an interface in ``station`` mode with ``wpa2_enterpise``
    or ``wpa2_personal`` authentication
    """
    base = copy.deepcopy(_base)
    base['sys'].update({
        'eap': [
            {
                'devname': radio(interface),
                'status': 'enabled',
            }
        ],
        'eap.status': 'enabled',
    })
    return base


_status = {
    'status': 'enabled',
}


_mapping = {
    'access_point': {
        'none': default,
        'wpa2_personal': station,
        'wpa2_enterprise': default,
    },
    'station': {
        'none': default,
        'wpa2_personal': station,
        'wpa2_enterprise': station,
    },
}


def ebtables_from_interface(interface):
    status = _status.copy()
    base = _mapping[mode(interface)][protocol(interface)](interface)
    return [status, base]
