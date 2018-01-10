from .interface import encryption, mode, protocol


def ap_authentication(interface):
    """
    Returns the ``radius.auth`` dict for ``access_point`` interface
    """
    result = {}
    proto = protocol(interface)
    if proto == 'wpa2_personal':
        result.update({
            'status': 'disabled',
        })
    elif proto == 'wpa2_enterprise':
        enc = encryption(interface)
        result.update({
            'ip': enc.get('server', ''),
            'port': enc.get('port', 1812),
            'secret': enc.get('key', ''),
            'status': 'enabled',
        })
    return result


def sta_authentication(interface):
    """
    Returns the ``radius.auth`` dict for ``station`` interface
    """
    result = {}
    return result


_authentication_from_mode = {
    'access_point': ap_authentication,
    'station': sta_authentication,
}


def authentication(interface):
    """
    returns the ``radius.auth`` dict
    """
    result = {
        'port': 1812,
    }
    result.update(_authentication_from_mode[mode(interface)](interface))
    return result


def ap_accounting(interface):
    """
    Returns the ``acct`` dict for ``access_point`` interfaces
    """
    result = {}
    if protocol(interface) == 'wpa2_enterprise':
        enc = encryption(interface)
        result.update({
            'port': enc.get('acct_server_port', 1813),
            'ip': enc.get('acct_server', ''),
            'status': 'enabled',
        })
    return result


def sta_accounting(interface):
    """
    Returns the ``acct`` dict for ``station`` interfaces
    """
    return {}


_accounting_from_mode = {
    'access_point': ap_accounting,
    'station': sta_accounting,
}


def accounting(interface):
    """
    Returns the ``radius.acct`` dict
    """
    result = {
        'port': 1813,
        'status': 'disabled',
    }
    result.update(_accounting_from_mode[mode(interface)](interface))
    return result


def radius_from_interface(interface):
    """
    Return the ``radius`` configuration for
    section ``aaa``
    """
    result = {
        'radius': {
            'auth': [
                authentication(interface),
            ],
            'acct': [
                accounting(interface),
            ],
        }
    }
    if protocol(interface) != 'none' and mode(interface) != 'station':
        result['radius'].update({
            'macacl': {
                'status': 'disabled',
            },
        })

    return result


__all__ = [
    radius_from_interface,
]
