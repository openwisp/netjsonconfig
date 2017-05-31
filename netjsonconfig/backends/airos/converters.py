from ...utils import get_copy, sorted_dict
from ..base.converter import BaseConverter

class Bridge(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        original = list(enumerate([
                i for i in get_copy(self.netjson, self.netjson_key) if i['type'] == 'bridge'
                ]))

        for index, interface in original:
            result.append({
                'key' : '{n}.comment'.format(n= index + 1 ),
                'value' : interface.get('comment', ''),
            })
            result.append({
                'key' : '{n}.devname'.format(n= index + 1 ),
                'value' : interface['name'],
            })

            for port_index, port in enumerate(interface.get('bridge_members',[])):
                result.append({
                    'key': '{n}.port.{m}.devname'.format(n= index + 1, m= port_index + 1),
                    'value': port,
                })
                result.append({
                    'key': '{n}.port.{m}.status'.format(n= index + 1, m= port_index + 1),
                    'value': 'enabled',
                })

        result.append({
            'key': 'status',
            'value': 'enabled',
        })

        return (('bridge', result),)



class Gui(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [
                {
                    'key': 'language',
                    'value': 'it_IT',
                },
                {
                    'key': 'network.advanced.status',
                    'value': 'enabled',
                }
        ]
        return (('gui', result),)


class Httpd(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [
                {
                    'key': 'https.port',
                    'value': 443,
                },
                {
                    'key': 'https.status',
                    'value': 'enabled',
                },
                {
                    'key': 'port',
                    'value': 80,
                },
                {
                    'key': 'session.timeout',
                    'value': 900,
                },
                {
                    'key': 'status',
                    'value': 'enabled',
                },
        ]

        return (('httpd', result),)


class Resolv(BaseConverter):
    netjson_key = 'dns_servers'

    def to_intermediate(self):
        result = []

        result.append({
            'key': 'host.1.name',
            'value': '',
        })

        original = list(enumerate(get_copy(self.netjson, self.netjson_key)))
        for index, nameserver in reversed(original):
            result.append({
                'key' : 'nameserver.{index}.ip'.format(index= index + 1 ),
                'value' : nameserver,
            })
            result.append({
                'key': 'nameserver.{index}.status'.format(index= index + 1),
                'value': 'enabled',
            })

        result.append({
            'key': 'status',
            'value': 'enabled',
        })

        return (('resolv', result),)


class Snmp(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [
                {
                    'key': 'community',
                    'value': 'public',
                },
                {
                    'key': 'contact',
                    'value': '',
                },
                {
                    'key': 'location',
                    'value': '',
                },
                {
                    'key': 'status',
                    'value': 'enabled',
                },
        ]

        return (('snmp', result),)



class Vlan(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        original = list(enumerate([
                i for i in get_copy(self.netjson, self.netjson_key) if '.' in i['name']
                ]))

        for index, v in original:
            result.append({
                'key' : '{index}.comment'.format(index= index + 1 ),
                'value' : v.get('comment', ''),
            })
            result.append({
                'key' : '{index}.devname'.format(index= index + 1 ),
                'value' : v['name'].split('.')[0],
            })
            result.append({
                'key' : '{index}.id'.format(index= index + 1 ),
                'value' : v['name'].split('.')[1],
            })
            result.append({
                'key' : '{index}.status'.format(index= index + 1 ),
                'value' : 'disabled' if v['disabled'] else 'enabled',
            })

        result.append({
            'key': 'status',
            'value': 'enabled',
        })

        return (('vlan', result),)


class Wireless(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        original = list(enumerate([
                i for i in get_copy(self.netjson, self.netjson_key) if hasattr(i,'wireless')
                ]))

        for index, w in original:
            result.append({
                'key' : '{index}.addmtikie'.format(index= index + 1 ),
                'value' : 'enabled',
            })
            result.append({
                'key' : '{index}.devname'.format(index= index + 1 ),
                'value' : w['name'],
            })

            hide_ssid = 'enabled' if w['wireless']['hide_ssid'] else 'disabled'
            result.append({
                'key' : '{index}.hide_ssid'.format(index= index + 1 ),
                'value' : hide_ssid
            })

            encryption = w['wireless'].get('encryption', 'none')
            result.append({
                'key' : '{index}.security.type'.format(index= index + 1 ),
                'value' : encryption,
            })

            result.append({
                'key' : '{index}.ssid'.format(index= index + 1 ),
                'value' : w['wireless']['ssid'],
            })

            result.append({
                'key' : '{index}.status'.format(index= index + 1 ),
                'value' : 'enabled',
            })

            result.append({
                'key' : '{index}.wds.status'.format(index= index + 1 ),
                'value' : 'enabled',
            })
        result.append({
            'key': 'status',
            'value': 'enabled',
        })

        return (('wireless', result),)
