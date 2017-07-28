from .interface import mode, protocol

_radius = {
    'radius': {
        'acct': [
            {
                'port': 1813,
                'status': 'disabled',
            }
        ],
        'auth': [
            {
                'port': 1812,
            },
        ],
    },
    'status': 'disabled',
}

_radius_from_mode = {
    'access_point': {
        'none': {},
        'wpa2_personal': {
            'radius': {
                'auth': [{
                    'port': 1812,
                    'status': 'disabled',
                }],
                'acct': [
                    {
                        'port': 1813,
                        'status': 'disabled',
                    }
                ],
                'macacl': {
                    'status': 'disabled',
                },
            },
            'status': 'enabled',
        },
    },
    'station': {
        'none': {},
        'wpa2_personal': {},
    }
}

def radius_from_interface(interface):
    radius = _radius.copy()
    radius.update(
            _radius_from_mode[mode(interface)][protocol(interface)]
    )
    return radius

__all__ = [
    radius_from_interface,
]
