from ...utils import get_copy, sorted_dict
from ..base.converter import BaseConverter

class Bridge(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        original = [
                i for i in get_copy(self.netjson, self.netjson_key) if i['type'] == 'bridge'
                ]

        bridges = []
        for interface in original:
            bridge_ports = []
            for port in interface.get('bridge_members',[]):
                bridge_ports.append({
                    'devname' : port,
                    'status' : 'enabled',
                })

            bridges.append({
                'comment' : interface.get('comment', ''),
                'devname' : interface['name'],
                'port' : bridge_ports,
            })


        result.append(bridges)
        result.append({
            'status': 'enabled',
        })

        return (('bridge', result),)



class Gui(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [
                {
                    'language': 'it_IT',
                },
                {
                    'network' : {
                        'advanced' : {
                            'status' : 'enabled',
                        }
                    }
                }
        ]
        return (('gui', result),)


class Httpd(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [
                {
                    'https' : {
                        'port' : 443,
                        'status' : 'enabled',
                    },
                },
                {
                    'port' : 80,
                    'session' : {
                        'timeout' : 900,
                    },
                    'status': 'enabled',
                },
        ]

        return (('httpd', result),)


class Resolv(BaseConverter):
    netjson_key = 'dns_servers'

    def to_intermediate(self):
        result = []

        result.append({
            'host': [{
                'name' : ''
            }]
        })

        original = get_copy(self.netjson, self.netjson_key)

        a = {
                'nameserver' : [],
        }
        for nameserver in original:
            a['nameserver'].append({
                'ip': nameserver,
                'status': 'enabled',
            })

        result.append(a)

        result.append({
            'status': 'enabled',
        })

        return (('resolv', result),)


class Snmp(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [
                {
                    'community' : 'public',
                    'contact' : 'value',
                    'location': '',
                    'status': 'enabled',
                },
        ]

        return (('snmp', result),)



class Vlan(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        original = [
                i for i in get_copy(self.netjson, self.netjson_key) if '.' in i['name']
                ]

        vlans = []
        for v in original:
            vlans.append({
                'comment' : v.get('comment', ''),
                'devname' : v['name'].split('.')[0],
                'id' : v['name'].split('.')[1],
                'status' : 'disabled' if v['disabled'] else 'enabled',
            })

        result.append(vlans)
        result.append({
            'status': 'enabled',
        })

        return (('vlan', result),)


class Wireless(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        original = [
                i for i in get_copy(self.netjson, self.netjson_key) if hasattr(i,'wireless')
                ]

        ws = []
        for w in original:
            hide_ssid = 'enabled' if w['wireless']['hide_ssid'] else 'disabled'
            encryption = w['wireless'].get('encryption', 'none')
            ws.append({
                'addmtikie': 'enabled',
                'devname' : w['name'],
                'hide_ssid' : hide_ssid,
                'security' : { 'type' : encryption },
                'ssid' : w['wireless']['ssid'],
                'status' : 'enabled',
                'wds' : { 'status': 'enabled' },
            })
        result.append(ws)

        result.append({
            'status': 'enabled',
        })

        return (('wireless', result),)
