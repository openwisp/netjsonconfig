"""
This configuration is for a radio in a ``station`` device without encryption
"""
radio_device_base = {
    'ack': {'auto': 'enabled'},
    'ackdistance': 643,
    'acktimeout': 35,
    'ampdu': {
        'frames': 32,
        'status': 'enabled',
    },
    'antenna': {
        'gain': 3,
        'id': 2,
    },
    'atpc': {
        'sta.status': 'enabled',
        'status': 'disabled',
        'threshold': 36,
    },
    'cable': {'loss': 0},
    'center': [{'freq': 0}],
    'chanbw': 0,
    'cmsbias': 0,
    'countrycode': 380,
    'cwm': {
        'enable': 0,
        'mode': 1,
    },
    'devname': 'ath0',
    'dfs': {'status': 'enabled'},
    'freq': 0,
    'ieee_mode': 'auto',
    'low_txpower_mode': 'disabled',
    'mode': 'managed',
    'obey': 'enabled',
    'polling': 'enabled',
    'polling_11ac_11n_compat': 0,
    'polling_ff_dl_ratio': 50,
    'polling_ff_dur': 0,
    'polling_ff_timing': 0,
    'pollingnoack': 0,
    'pollingpri': 2,
    'ptpmode': 1,
    'reg_obey': 'enabled',
    'rx_sensitivity': -96,
    'scan_list': {'status': 'disabled'},
    'scanbw': {'status': 'disabled'},
    'status': 'enabled',  # cannot disable
    'subsystemid': 0xe7f5,
    'txpower': 24,
}

radio_configuration = {
    'status': 'enabled',
    'countrycode': 380,
}


def access_point(radio):
    """
    Return the configuration for a radio device whose wireless
    interface is in ``access_point`` mode
    """
    base = radio_device_base.copy()
    base.update({
        'devname': radio['name'],
        'chanbw': 80,
        'ieee_mode': '11acvht80',
        'mode': 'master',
    })
    return base


def station(radio):
    """
    Return the configuration for a radio device whose wireless
    interface is in ``station`` mode
    """
    base = radio_device_base.copy()
    base.update({
        'devname': radio['name'],
        'chanbw': 0,
        'txpower': radio.get('tx_power', 24),
    })
    return base


radio_available_mode = {
    'access_point': access_point,
    'station': station,
}


__all__ = [
    radio_available_mode,
    radio_configuration,
]
