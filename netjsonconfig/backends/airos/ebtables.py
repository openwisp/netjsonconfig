import copy

from .interface import radio

_base = {
    'sys': {
        'status': 'enabled',
    },
}


def encrypted(interface):
    """
    Returns the configuration for ``ebtables.sys`` when encrypted
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


def unencrypted(interface):
    """
    Returns the configuration for ``ebtables.sys``
    for an interface withouth encryption
    """
    return {}
