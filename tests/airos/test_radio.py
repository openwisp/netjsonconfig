from .mock import ConverterTest, RadioAirOs


class TestRadioStationConverter(ConverterTest):
    """
    Test radio device configuration for ``station`` wireless lan
    """

    backend = RadioAirOs

    def test_no_radio(self):
        o = self.backend({
            "radios": []
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
                'countrycode': 380,
            },
        ]

        self.assertEqualConfig(o.intermediate_data['radio'], expected)

    def test_active_radio(self):
        o = self.backend({
            "interfaces": [
                {
                    'type': 'wireless',
                    'name': 'wlan0',
                    'wireless': {
                        'radio': 'ath0',
                        'mode': 'station',
                        'ssid': 'ubnt',
                        'bssid': '00:11:22:33:44:55',
                        'encryption': {
                            'protocol': 'none',
                        },
                    },
                },
            ],
            "radios": [
                {
                    'name': 'ath0',
                    'channel': 1,
                    'channel_width': 20,
                    'protocol': '802.11n',
                }
            ]
        })
        o.to_intermediate()
        expected = [
            {
                '1.ack.auto': 'enabled',
                '1.ackdistance': 643,
                '1.acktimeout': 35,
                '1.ampdu.frames': 32,
                '1.ampdu.status': 'enabled',
                '1.antenna.gain': 3,
                '1.antenna.id': 2,
                '1.atpc.sta.status': 'enabled',
                '1.atpc.status': 'disabled',
                '1.atpc.threshold': 36,
                '1.cable.loss': 0,
                '1.center.1.freq': 0,
                '1.chanbw': 20,
                '1.cmsbias': 0,
                '1.countrycode': 380,
                '1.cwm.enable': 0,
                '1.cwm.mode': 1,
                '1.devname': 'ath0',
                '1.dfs.status': 'enabled',
                '1.freq': 0,
                '1.ieee_mode': 'auto',
                '1.low_txpower_mode': 'disabled',
                '1.mode': 'managed',
                '1.obey': 'enabled',
                '1.polling': 'enabled',
                '1.polling_11ac_11n_compat': 0,
                '1.polling_ff_dl_ratio': 50,
                '1.polling_ff_dur': 0,
                '1.polling_ff_timing': 0,
                '1.pollingnoack': 0,
                '1.pollingpri': 2,
                '1.ptpmode': 1,
                '1.reg_obey': 'enabled',
                '1.rx_sensitivity': -96,
                '1.scan_list.status': 'disabled',
                '1.scanbw.status': 'disabled',
                '1.status': 'enabled',
                '1.subsystemid': 0xe7f5,
                '1.txpower': 24,
            },
            {
                'countrycode': 380,
                'status': 'enabled',
            }
        ]

        self.assertEqualConfig(o.intermediate_data['radio'], expected)


    def test_channel_width(self):
        """
        TODO: channel brandwidth tested only on 802.11ac
        """
        o = self.backend({
            "interfaces": [
                {
                    'type': 'wireless',
                    'name': 'wlan0',
                    'wireless': {
                        'radio': 'ath0',
                        'mode': 'station',
                        'ssid': 'ubnt',
                        'bssid': '00:11:22:33:44:55',
                        'encryption': {
                            'protocol': 'none',
                        },
                    },
                },
            ],
            "radios": [
                {
                    'name': 'ath0',
                    'channel': 1,
                    'channel_width': 80,
                    'protocol': '802.11ac',
                }
            ]
        })
        o.to_intermediate()
        expected = [
            {
                '1.ack.auto': 'enabled',
                '1.ackdistance': 643,
                '1.acktimeout': 35,
                '1.ampdu.frames': 32,
                '1.ampdu.status': 'enabled',
                '1.antenna.gain': 3,
                '1.antenna.id': 2,
                '1.atpc.sta.status': 'enabled',
                '1.atpc.status': 'disabled',
                '1.atpc.threshold': 36,
                '1.cable.loss': 0,
                '1.center.1.freq': 0,
                '1.chanbw': 80,
                '1.cmsbias': 0,
                '1.countrycode': 380,
                '1.cwm.enable': 0,
                '1.cwm.mode': 1,
                '1.devname': 'ath0',
                '1.dfs.status': 'enabled',
                '1.freq': 0,
                '1.ieee_mode': 'auto',
                '1.low_txpower_mode': 'disabled',
                '1.mode': 'managed',
                '1.obey': 'enabled',
                '1.polling': 'enabled',
                '1.polling_11ac_11n_compat': 0,
                '1.polling_ff_dl_ratio': 50,
                '1.polling_ff_dur': 0,
                '1.polling_ff_timing': 0,
                '1.pollingnoack': 0,
                '1.pollingpri': 2,
                '1.ptpmode': 1,
                '1.reg_obey': 'enabled',
                '1.rx_sensitivity': -96,
                '1.scan_list.status': 'disabled',
                '1.scanbw.status': 'disabled',
                '1.status': 'enabled',
                '1.subsystemid': 0xe7f5,
                '1.txpower': 24,
            },
            {
                'countrycode': 380,
                'status': 'enabled',
            }
        ]

        self.assertEqualConfig(o.intermediate_data['radio'], expected)


class TestRadioAccessPointConverter(ConverterTest):
    """
    Test radio device configuration for ``access_point`` wireless lan
    """

    backend = RadioAirOs

    def test_active_radio(self):
        o = self.backend({
            "interfaces": [
                {
                    'type': 'wireless',
                    'name': 'wlan0',
                    'wireless': {
                        'radio': 'ath0',
                        'mode': 'access_point',
                        'bssid': '00:11:22:33:44:55',
                        'ssid': 'ubnt',
                        'encryption': {
                            'protocol': 'none',
                        },
                    },
                },
            ],
            "radios": [
                {
                    'name': 'ath0',
                    'channel': 36,
                    'channel_width': 20,
                    'protocol': '802.11ac',
                }
            ]
        })
        o.to_intermediate()
        expected = [
            {
                '1.ack.auto': 'enabled',
                '1.ackdistance': 643,
                '1.acktimeout': 35,
                '1.ampdu.frames': 32,
                '1.ampdu.status': 'enabled',
                '1.antenna.gain': 3,
                '1.antenna.id': 2,
                '1.atpc.sta.status': 'enabled',
                '1.atpc.status': 'disabled',
                '1.atpc.threshold': 36,
                '1.cable.loss': 0,
                '1.center.1.freq': 0,
                '1.chanbw': 20,
                '1.cmsbias': 0,
                '1.countrycode': 380,
                '1.cwm.enable': 0,
                '1.cwm.mode': 1,
                '1.devname': 'ath0',
                '1.dfs.status': 'enabled',
                '1.freq': 0,
                '1.ieee_mode': '11acvht20',
                '1.low_txpower_mode': 'disabled',
                '1.mode': 'master',
                '1.obey': 'enabled',
                '1.polling': 'enabled',
                '1.polling_11ac_11n_compat': 0,
                '1.polling_ff_dl_ratio': 50,
                '1.polling_ff_dur': 0,
                '1.polling_ff_timing': 0,
                '1.pollingnoack': 0,
                '1.pollingpri': 2,
                '1.ptpmode': 1,
                '1.reg_obey': 'enabled',
                '1.rx_sensitivity': -96,
                '1.scan_list.status': 'disabled',
                '1.scanbw.status': 'disabled',
                '1.status': 'enabled',
                '1.subsystemid': 0xe7f5,
                '1.txpower': 24,
            },
            {
                'countrycode': 380,
                'status': 'enabled',

            },
        ]

        self.assertEqualConfig(o.intermediate_data['radio'], expected)
