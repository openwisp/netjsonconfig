from copy import deepcopy
from ...utils import get_copy, sorted_dict
from ..base.converter import BaseConverter

from ipaddress import ip_interface

from wpasupplicant import available_mode_authentication


def status(config, key='disabled'):
    if config.get(key):
        return 'disabled'
    else:
        return 'enabled'


class AirOSConverter(BaseConverter):
    """
    Always run the converter from NetJSON
    to native
    """

    @classmethod
    def should_run_forward(cls, config):
        return True


class Aaa(AirOSConverter):
    netjson_key = 'general'

    def wpa2_personal(self):
        """
        When using wpa_personal the wifi password is written
        in ``aaa.1.wpa.psk`` instead of ``wpasupplicant``
        """
        wireless = [ i for i in get_copy(self.netjson, 'interfaces') if i['type'] == 'wireless']

        def get_psk(interface):
            t = {
                'wpa': {
                    'psk': interface['encryption']['key'],
                },
            }
            return t

        def is_wpa2_personal(interface):
            try:
                return interface['encryption']['protocol'] == 'wpa2_personal'
            except:
                return False

        try:
            return [get_psk(i) for i in wireless if is_wpa2_personal(i)][0]
        except IndexError:
            return {}

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
                'status': 'disabled',
            }
        ])

        w = self.wpa2_personal()
        if w:
            result.append([w])

        return (('aaa', result),)


class Bridge(AirOSConverter):
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


class Discovery(AirOSConverter):
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


class Dyndns(AirOSConverter):
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


class Ebtables(AirOSConverter):
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


class Gui(AirOSConverter):
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


class Httpd(AirOSConverter):
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


class Igmpproxy(AirOSConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [
               {
                    'status':  'enabled',
                },
        ]

        return (('igmpproxy', result),)


class Iptables(AirOSConverter):
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


class Netconf(AirOSConverter):
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
            if interface['type'] == 'ethernet' and '.' not in interface['name']:
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

                    if addr.get('management'):
                        temp['role'] = self.type_to_role(interface['type'])

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


class Netmode(AirOSConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []

        result.append({
            'status': 'enabled',
        })
        return (('netmode', result), )


class Ntpclient(AirOSConverter):
    netjson_key = 'ntp_servers'

    def to_intermediate(self):
        result = []
        temp = []

        original = get_copy(self.netjson, self.netjson_key, [])

        if original:
            for ntp in original:
                temp.append({
                    'server': ntp,
                    'status': 'enabled',
                })

            result.append(temp)
            result.append({
                'status': 'enabled',
            })
        else:
            result.append({
                'status': 'disabled',
            })

        return (('ntpclient', result),)


class Pwdog(AirOSConverter):
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


class Resolv(AirOSConverter):
    netjson_key = 'dns_servers'

    def host(self):
        original = get_copy(self.netjson, 'general', {})
        return {
            'host':  [{
                'name': original.get('hostname', 'airos'),
                'status': 'enabled',
            }],
        }

    def nameserver(self):
        original = get_copy(self.netjson, self.netjson_key)

        t = []

        for nameserver in original:
            t.append({
                'ip':  nameserver,
                'status':  'enabled',
            })

        return {'nameserver': t}

    def to_intermediate(self):
        result = []

        result.append(self.host())

        result.append(self.nameserver())

        result.append({
            'status':  'enabled',
        })

        return (('resolv', result),)


class Route(AirOSConverter):
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


class Snmp(AirOSConverter):
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


class Sshd(AirOSConverter):
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


class Syslog(AirOSConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'status': 'disabled',
        })
        return (('syslog', result),)


class System(AirOSConverter):
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


class Telnetd(AirOSConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'port': 23,
            'status': 'disabled',
        })
        return (('telnetd', result),)


class Tshaper(AirOSConverter):
    netjson_key = 'general'

    def to_intermediate(self):

        return (('tshaper', [{'status': 'disabled', }]),)


class Unms(AirOSConverter):
    netjson_keu = 'general'

    def to_intermediate(self):

        return (('unms', [{'status': 'disabled'}]),)


class Update(AirOSConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'check': {
                'status': 'enabled',
            },
        })
        return (('update', result),)


class Users(AirOSConverter):
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


class Vlan(AirOSConverter):
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


class Wireless(AirOSConverter):
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
                'l2_isolation': 'disabled',
                'mac_acl': {
                    'policy': 'allow',
                    'status': 'disabled',
                },
                'mcast': {
                    'enhance': 0,
                },
                'rate': {
                    'auto': 'enabled',
                    'mcs': -1,
                },
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


class Wpasupplicant(AirOSConverter):
    netjson_key = 'interfaces'

    def _station_intermediate(self, original):
        result = []
        station_auth_protocols = available_mode_authentication['station']

        temp_dev = {
            'profile': 'AUTO',
            'status': 'enabled',
            'driver': 'madwifi',
            'devname': '',
        }

        if original:
            head = original[0]
            temp_dev['devname'] = head['wireless']['radio']

            if 'encryption' in head:
                network = station_auth_protocols.get(head['encryption']['protocol'])(head)

            else:
                network = station_auth_protocols['none'](head)
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
                        self.secondary_network(),
                    ],
                },
            ],
        })
        result.append({
            'status': 'enabled',
        })

        return (('wpasupplicant', result),)

    def _access_point_intermediate(self, original):
        """
        Intermediate representation for ``access_point`` mode

        wpasupplicant.device is missing when using the ``access_point`` mode
        to the temp_dev will not be generated
        """
        result = []
        ap_auth_protocols = available_mode_authentication['access_point']

        temp_dev = {
            'profile': 'AUTO',
            'status': 'disabled',
        }

        if original:
            head = original[0]

            if 'encryption' in head:
                network = ap_auth_protocols.get(head['encryption']['protocol'])(head)
                result.append({
                    'status': 'disabled',
                })

            else:
                network = ap_auth_protocols['none'](head)
                temp_dev['status'] = 'enabled'
                result.append({
                    'status': 'enabled',
                })

        result.append({
            'device': [
                temp_dev,
            ],
            'profile': [
                {
                    'name': 'AUTO',
                    'network': [
                        network,
                        self.secondary_network(),
                    ],
                },
            ],
        })

        return (('wpasupplicant', result),)

    def secondary_network(self):
        """
        The default secondary network configuration
        """
        return {
            'key_mgmt': [
                {
                    'name': 'NONE',
                },
            ],
            'priority': 2,
            'status': 'disabled',
        }

    def to_intermediate(self):
        original = [
                i for i in get_copy(self.netjson, self.netjson_key) if i['type'] == 'wireless'
                ]

        if original:
            head = original[0]
            # call either ``_station_intermediate`` or ``_access_point_intermediate``
            # and return the result
            return getattr(self, '_%s_intermediate' % head['wireless']['mode'])(original)
