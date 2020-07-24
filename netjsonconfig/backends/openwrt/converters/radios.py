from ..schema import default_radio_driver
from .base import OpenWrtConverter


class Radios(OpenWrtConverter):
    netjson_key = 'radios'
    intermediate_key = 'wireless'
    _uci_types = ['wifi-device']

    def to_intermediate_loop(self, block, result, index=None):
        radio = self.__intermediate_radio(block)
        result.setdefault('wireless', [])
        result['wireless'].append(radio)
        return result

    def __intermediate_radio(self, radio):
        radio.update({'.type': 'wifi-device', '.name': radio.pop('name')})
        # rename tx_power to txpower
        if 'tx_power' in radio:
            radio['txpower'] = radio.pop('tx_power')
        # rename driver to type
        radio['type'] = radio.pop('driver', default_radio_driver)
        # determine hwmode option
        radio['hwmode'] = self.__intermediate_hwmode(radio)
        # check if using channel 0, that means "auto"
        if radio['channel'] == 0:
            radio['channel'] = 'auto'
        # determine channel width
        if radio['type'] == 'mac80211':
            radio['htmode'] = self.__intermediate_htmode(radio)
        # ensure country is uppercase
        if 'country' in radio:
            radio['country'] = radio['country'].upper()
        return self.sorted_dict(radio)

    def __intermediate_hwmode(self, radio):
        """
        possible return values are: 11a, 11b, 11g
        """
        protocol = radio['protocol']
        if protocol in ['802.11a', '802.11b', '802.11g']:
            # return 11a, 11b or 11g
            return protocol[4:]
        # determine hwmode depending on channel used
        if radio['channel'] == 0:
            # when using automatic channel selection, we need an
            # additional parameter to determine the frequency band
            return radio.get('hwmode')
        elif radio['channel'] <= 13:
            return '11g'
        else:
            return '11a'

    def __intermediate_htmode(self, radio):
        """
        only for mac80211 driver
        """
        protocol = radio.pop('protocol')
        channel_width = radio.pop('channel_width')
        # allow overriding htmode
        if 'htmode' in radio:
            return radio['htmode']
        if protocol == '802.11n':
            return 'HT{0}'.format(channel_width)
        elif protocol == '802.11ac':
            return 'VHT{0}'.format(channel_width)
        # disables n
        return 'NONE'

    def to_netjson_loop(self, block, result, index):
        radio = self.__netjson_radio(block)
        result.setdefault('radios', [])
        result['radios'].append(radio)
        return result

    def __netjson_radio(self, radio):
        del radio['.type']
        radio['name'] = radio.pop('.name')
        if 'txpower' in radio:
            radio['tx_power'] = int(radio.pop('txpower'))
        radio['driver'] = radio.pop('type')
        if 'disabled' in radio:
            radio['disabled'] = radio['disabled'] == '1'
        radio['protocol'] = self.__netjson_protocol(radio)
        radio['channel'] = self.__netjson_channel(radio)
        radio['channel_width'] = self.__netjson_channel_width(radio)
        return radio

    def __netjson_protocol(self, radio):
        """
        determines NetJSON protocol radio attribute
        """
        htmode = radio.get('htmode')
        hwmode = radio.get('hwmode', None)
        if htmode.startswith('HT'):
            return '802.11n'
        elif htmode.startswith('VHT'):
            return '802.11ac'
        return '802.{0}'.format(hwmode)

    def __netjson_channel(self, radio):
        """
        determines NetJSON channel radio attribute
        """
        if radio['channel'] == 'auto':
            return 0
        # delete hwmode because is needed
        # only when channel is auto
        del radio['hwmode']
        return int(radio['channel'])

    def __netjson_channel_width(self, radio):
        """
        determines NetJSON channel_width radio attribute
        """
        htmode = radio.pop('htmode')
        if htmode == 'NONE':
            return 20
        channel_width = htmode.replace('VHT', '').replace('HT', '')
        # we need to override htmode
        if '+' in channel_width or '-' in channel_width:
            radio['htmode'] = htmode
            channel_width = channel_width[0:-1]
        return int(channel_width)
