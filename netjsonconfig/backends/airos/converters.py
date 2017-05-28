from ...utils import get_copy, sorted_dict
from ..base.converter import BaseConverter

class Dns(BaseConverter):
    netjson_key = 'dns_servers'

    def to_intermediate(self):
        result = []
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
