from copy import deepcopy
from ...utils import get_copy, sorted_dict
from ..base.converter import BaseConverter

from ipaddress import ip_interface

from wpasupplicant import available_encryption_protocols

def status(config, key='disabled'):
    if config.get(key):
        return 'disabled'
    else:
        return 'enabled'


class Aaa(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
                'status': 'disabled',
        })
        result.append([
            {
                'radius': {
                    'acct': [
                        {
                            'port': 1813,
                            'status': 'disabled',
                        },
                    ],
                    'auth': [
                        {
                            'port': 1812,
                        },
                    ],
                },
            }
        ])
        return (('aaa', result),)


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
            for port in interface.get('bridge_members', []):
                bridge_ports.append({
                    'devname':  port,
                    'status':  'enabled',
                })

            bridges.append({
                'comment':  interface.get('comment', ''),
                'devname':  interface['name'],
                'port':  bridge_ports,
                'status':  status(interface),
                'stp': {
                    'status':  'enabled',
                }
            })

        result.append(bridges)
        result.append({
            'status':  'enabled',
        })

        return (('bridge', result),)


class Discovery(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [
               {
                   'cdp': {
                       'status': 'enabled',
                    },
                   'status': 'enabled',
                },
        ]
        return (('discovery', result),)


class Dyndns(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [
#                [
#                    {
#                        'servicename': 'dyndns.org',
#                    },
#                ],
                {
                    'status': 'disabled',
                },
        ]
        return (('dyndns', result),)


class Ebtables(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [
               {
                    'sys': {
                        'fw': {
                            'status':  'enabled',
                        },
                        'status': 'enabled',
                    },
                    'status': 'enabled',
                },
        ]

        return (('httpd', result),)


class Gui(BaseConverter):
    netjson_key = 'gui'

    def to_intermediate(self):
        result = [
               {
                    'language':  'en_US',
                },
               {
                    'network': {
                        'advanced': {
                            'status':  'enabled',
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
                    'https': {
                        'port':  443,
                        'status':  'enabled',
                    },
                },
               {
                    'port':  80,
                    'session': {
                        'timeout':  900,
                    },
                    'status':  'enabled',
                },
        ]

        return (('httpd', result),)


class Igmpproxy(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [
               {
                    'status':  'enabled',
                },
        ]

        return (('igmpproxy', result),)


class Iptables(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [
               {
                    'sys': {
                        'portfw':  {
                            'status': 'enabled',
                        },
                        'status':  'enabled',
                    },
                    'status':  'enabled',
                },
        ]

        return (('iptables', result),)


class Netconf(BaseConverter):
    netjson_key = 'interfaces'

    def type_to_role(self, typestr):
        roles = {
            'ethernet': 'mlan',
            'bridge': 'mlan',
        }
        return roles.get(typestr,'')

    def to_intermediate(self):
        result = []
        interfaces = []
        original = get_copy(self.netjson, self.netjson_key)

        for interface in original:
            base = {
                'devname':  interface['name'],
                'status': 'enabled',  # can't disable interfaces
                'up':  status(interface),
                'mtu': interface.get('mtu', 1500),
            }

            # handle interface type quirks
            if interface['type'] == 'ethernet' and not '.' in interface['name']:
                base['autoneg'] = 'enabled'
                base['flowcontrol'] = {
                        'rx': {
                            'status': 'enabled',
                        },
                        'tx': {
                            'status': 'enabled',
                        },
                    }

            if interface['type'] == 'wireless':
                base['devname'] = interface['wireless']['radio']

            addresses = interface.get('addresses')

            if addresses:
                # for every address policy put a
                # configuration
                for addr in addresses:
                    temp = deepcopy(base)

                    # handle explicit address policy
                    if addr['proto'] == 'dhcp':
                        temp['autoip'] = {}
                        temp['autoip']['status'] = 'enabled'
                    else:
                        ip_and_mask = '%s/%d' % (addr['address'], addr['mask'])
                        network = ip_interface(ip_and_mask)
                        temp['ip'] = str(network.ip)
                        temp['netmask'] = str(network.netmask)

                    interfaces.append(temp)
            else:
                # an interface without address
                # is still valid with these defaults values
                base['autoip'] = {
                        'status': 'disabled',
                    }
                interfaces.append(base)

        result.append(interfaces)
        result.append({
            'status':  'enabled',
        })
        return (('netconf', result),)


class Netmode(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []

        result.append({
            'status': 'enabled',
        })
        return (('netmode', result), )


class Ntpclient(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'status': 'disabled',
        })
        return (('ntpclient', result),)


class Pwdog(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'delay': 300,
            'period': 300,
            'retry': 3,
            'status': 'enabled',
        })
        return (('pwdog', result),)


class Radio(BaseConverter):
    netjson_key = 'radios'

    def to_intermediate(self):
        result = []

        original = get_copy(self.netjson, self.netjson_key)

        radios = []

        for r in original:
            radios.append({
                'devname': r['name'],
                'status': status(r),
                'txpower': r.get('tx_power', ''),
                'chanbw': r.get('channel_width', ''),
            })

        result.append(radios)

        result.append({
            'status': 'enabled',
        })

        return (('radio', result),)


class Resolv(BaseConverter):
    netjson_key = 'dns_servers'

    def to_intermediate(self):
        result = []

        original = get_copy(self.netjson, "general")
        hostname = original.get('hostname', 'airos')

        result.append({
            'host':  [{
                'name':  hostname,
                'status': 'enabled',
            }]
        })

        original = get_copy(self.netjson, self.netjson_key)

        a = {
                'nameserver':  [],
        }
        for nameserver in original:
            a['nameserver'].append({
                'ip':  nameserver,
                'status':  'enabled',
            })

        result.append(a)

        result.append({
            'status':  'enabled',
        })

        return (('resolv', result),)


class Route(BaseConverter):
    netjson_key = 'routes'

    def to_intermediate(self):
        result = []
        original = get_copy(self.netjson, self.netjson_key)

        routes = []

        for r in original:
            routes.append({
                'devname': '',
                'gateway': '0.0.0.0',
                'ip': '0.0.0.0',
                'netmask': 0,
                'status': 'enabled',
            })

        result.append(routes)

        result.append({
            'status': 'enabled',
        })
        return (('route', result),)


class Snmp(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [
               {
                    'community':  'public',
                    'contact':  '',
                    'location':  '',
                    'status':  'enabled',
                },
        ]

        return (('snmp', result),)


class Sshd(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'auth': {
                'passwd': 'enabled',
            },
            'port': 22,
            'status': 'enabled',
        })
        return (('sshd', result),)


class Syslog(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'status': 'disabled',
        })
        return (('syslog', result),)


class System(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'airosx': {
                'prov': {
                    'status': 'enabled',
                },
            },
            'cfg': {
                'version': 0,
            },
            'date': {
                'status': 'enabled',
            },
            'external': {
                'reset': 'enabled',
            },
            'timezone': 'GMT',
        })
        return (('system', result),)


class Telnetd(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'port': 23,
            'status': 'disabled',
        })
        return (('telnetd', result),)


class Tshaper(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):

        return (('tshaper', [{'status': 'disabled', }]),)


class Unms(BaseConverter):
    netjson_keu = 'general'

    def to_intermediate(self):

        return (('unms', [{'status': 'disabled'}]),)


class Update(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'check': {
                'status': 'enabled',
            },
        })
        return (('update', result),)


class Users(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'status': 'disabled',
        })

        result.append([
            {
                'name': 'root',
                'password': 'changeme',
                'status': 'disabled',
            },
        ])

        return (('users', result),)


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
                'comment':  v.get('comment', ''),
                'devname':  v['name'].split('.')[0],
                'id':  v['name'].split('.')[1],
                'status': status(v),
            })

        result.append(vlans)
        result.append({
            'status':  'enabled',
        })

        return (('vlan', result),)


class Wireless(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        original = [
                i for i in get_copy(self.netjson, self.netjson_key) if i['type'] == 'wireless'
                ]

        ws = []
        for w in original:
            ws.append({
                'addmtikie':  'enabled',
                'devname':  w['wireless']['radio'],
                'hide_ssid': 'enabled' if w['wireless'].get('hidden') else 'disabled',
                'security': {
                    'type': 'none',
                },
                'signal_led1': 75,
                'signal_led2': 50,
                'signal_led3': 25,
                'signal_led4': 15,
                'signal_led_status': 'enabled',
                'ssid':  w['wireless']['ssid'],
                'status': status(w),
                'wds': {
                    'status': 'enabled',
                },
            })
        result.append(ws)

        result.append({
            'status':  'enabled',
        })

        return (('wireless', result),)


class Wpasupplicant(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []

        original = [
                i for i in get_copy(self.netjson, self.netjson_key) if i['type'] == 'wireless'
                ]

        temp_dev = {
            'profile': 'AUTO',
            'status': 'enabled',
            'driver': 'madwifi',
            'devname': '',
        }

        if original:
            head = original[0]
            temp_dev['devname'] = head['wireless']['radio']

            if head['encryption']:
                network = available_encryption_protocols.get(head['encryption']['protocol'])(head)

            else:
                network = available_encryption_protocols['none'](head)
                temp_dev['status'] = 'disabled'
                del temp_dev['driver']
                del temp_dev['devname']

        result.append({
            'device': [
                temp_dev,
            ],
            'profile': [
                {
                    'name': 'AUTO',
                    'network': [
                        network,
                        {
                            'key_mgmt': [
                                {
                                    'name': 'NONE',
                                },
                            ],
                            'priority': 2,
                            'status': 'disabled',
                        },
                    ],
                },
            ],
        })
        result.append({
            'status': 'enabled',
        })

        return (('wpasupplicant', result),)
