from copy import deepcopy
from ipaddress import ip_interface

from ...utils import get_copy
from ..base.converter import BaseConverter
from .aaa import bridge_devname, profile_from_interface, status_from_interface
from .interface import (autonegotiation, bridge, flowcontrol, mode, protocol,
                        radio, split_cidr, stp, vlan, wireless)
from .radio import radio_available_mode, radio_configuration
from .radius import radius_from_interface
from .schema import default_ntp_servers
from .wireless import wireless_available_mode
from .wpasupplicant import available_mode_authentication


def status(config, key='disabled'):
    if config.get(key):
        return 'disabled'
    else:
        return 'enabled'


class AirOsConverter(BaseConverter):
    """
    Always run the converter from NetJSON
    to native
    """
    @classmethod
    def should_run_forward(cls, config):
        return True

    @property
    def netmode(self):
        return self.config.get('netmode', 'bridge')


class Aaa(AirOsConverter):
    netjson_key = 'general'

    @property
    def bridge(self):
        """
        Return all the bridge interfaces
        """
        return bridge(get_copy(self.netjson, 'interfaces', []))

    @property
    def wireless(self):
        """
        Return all the wireless interfaces
        """
        return wireless(get_copy(self.netjson, 'interfaces', []))

    def to_intermediate(self):
        base = {}
        result = []
        try:
            wireless = self.wireless[0]
            base.update(profile_from_interface(wireless))
            base.update(status_from_interface(wireless))
            base.update(radius_from_interface(wireless))
        except IndexError:
            raise Exception('input is missing a wireless or bridge interface')

        try:
            bridge = self.bridge[0]
            base.update(bridge_devname(wireless, bridge))
        except IndexError:
            pass

        result.append(status_from_interface(wireless))
        result.append([base])

        return (('aaa', result),)


class Bridge(AirOsConverter):
    netjson_key = 'interfaces'

    @property
    def bridge(self):
        return bridge(get_copy(self.netjson, self.netjson_key, []))

    def to_intermediate(self):
        result = []
        bridges = []
        for interface in self.bridge:
            bridge_ports = []
            for port in interface.get('bridge_members', []):
                bridge_ports.append({
                    'devname': port,
                    'status': 'enabled',
                })
            bridges.append({
                'comment': interface.get('comment', ''),
                'devname': interface['name'],
                'port': bridge_ports,
                'status': status(interface),
                'stp': {'status': stp(interface)}
            })

        result.append(bridges)
        result.append({
            'status': 'enabled',
        })
        return (('bridge', result),)


class Discovery(AirOsConverter):
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


class Dyndns(AirOsConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [{'status': 'disabled'}]
        return (('dyndns', result),)


class Ebtables(AirOsConverter):
    netjson_key = 'general'

    _base = {
        'sys': {
            'fw': {
                'status': 'disabled',
            },
            'status': 'enabled'
        },
        'status': 'enabled'
    }

    def bridge_intermediate(self):
        base = self._base.copy()
        return [base]

    def router_intermediate(self):
        return [{}]

    def to_intermediate(self):
        netmode = get_copy(self.netjson, 'netmode', 'bridge')
        result = getattr(self, '{netmode}_intermediate'.format(netmode=netmode))()
        return (('ebtables', result),)


class Gui(AirOsConverter):
    netjson_key = 'gui'

    def to_intermediate(self):
        original = get_copy(self.netjson, self.netjson_key, {})
        result = [
            {
                'language': original.get('language', 'en_US'),
            },
            {
                'network': {
                    'advanced': {
                        'status': 'enabled',
                    }
                }
            }
        ]
        return (('gui', result),)


class Httpd(AirOsConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [
            {
                'https': {
                    'port': 443,
                    'status': 'enabled',
                },
            },
            {
                'port': 80,
                'session': {'timeout': 900},
                'status': 'enabled',
            }
        ]
        return (('httpd', result),)


class Igmpproxy(AirOsConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = {'status': 'disabled'}
        if self.netmode == 'router':
            result.update({'upstream': {'devname': ''}})
        return (('igmpproxy', [result]),)


class Iptables(AirOsConverter):
    netjson_key = 'general'

    _base = {
        'sys': {
            'portfw': {'status': 'disabled'},
            'status': 'enabled',
        },
        'status': 'disabled'
    }

    def bridge_intermediate(self):
        base = self._base.copy()
        return [base]

    def router_intermediate(self):
        base = self._base.copy()
        base.update({
            'status': 'enabled',
        })
        base['sys'].update({
            'fw': {'status': 'disabled'},
            'mgmt': [
                {
                    'devname': 'br0',
                    'status': 'enabled',
                }
            ],
            'mgmt.status': 'enabled',
        })

        return [base]

    def to_intermediate(self):
        netmode = get_copy(self.netjson, 'netmode', 'bridge')
        result = getattr(self, '{netmode}_intermediate'.format(netmode=netmode))()
        return (('iptables', result),)


class Netconf(AirOsConverter):
    netjson_key = 'interfaces'

    def type_to_role(self, typestr):
        roles = {
            'ethernet': 'mlan',
            'bridge': 'mlan',
        }
        return roles.get(typestr, '')

    def to_intermediate(self):
        result = []
        interfaces = []
        original = get_copy(self.netjson, self.netjson_key, [])

        for interface in original:
            base = {
                'devname':  interface['name'],
                'status': 'enabled',  # can't disable interfaces
                'up':  status(interface),
                'mtu': interface.get('mtu', 1500),
            }
            # handle interface type quirks
            if interface['type'] == 'ethernet' and '.' not in interface['name']:
                base['autoneg'] = autonegotiation(interface)

                base['flowcontrol'] = flowcontrol(interface)

            if interface['type'] == 'wireless':
                base['devname'] = radio(interface)

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
                        temp['autoip'] = {'status': 'enabled'}
                    else:
                        temp.update(split_cidr(addr))
                    interfaces.append(temp)
            else:
                # an interface without address
                # is still valid with these defaults values
                base['autoip'] = {'status': 'disabled'}
                interfaces.append(base)
        result.append(interfaces)
        result.append({'status': 'enabled'})
        return (('netconf', result),)


class Netmode(AirOsConverter):
    netjson_key = 'netmode'

    def to_intermediate(self):
        result = []
        result.append({
            'status': self.netjson.get('netmode', 'bridge'),
        })
        return (('netmode', result), )


class Ntpclient(AirOsConverter):
    netjson_key = 'ntp'

    def ntp_status(self, ntp):
        if ntp.get('enabled', True):
            return 'enabled'
        else:
            return 'disabled'

    def to_intermediate(self):
        result = []
        servers = []
        original = get_copy(self.netjson, self.netjson_key, {})
        result.append({'status': self.ntp_status(original)})

        for ntp in original.get('server', default_ntp_servers):
            servers.append({
                'server': ntp,
                'status': 'enabled',
            })
        result.append(servers)
        return (('ntpclient', result),)


class Pwdog(AirOsConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []
        result.append({
            'delay': 300,
            'period': 300,
            'retry': 3,
            'status': 'disabled',
        })
        return (('pwdog', result),)


class Radio(AirOsConverter):
    netjson_key = 'radios'

    @property
    def radio(self):
        return get_copy(self.netjson, self.netjson_key, [])

    @property
    def wireless(self):
        return wireless(get_copy(self.netjson, 'interfaces', []))

    def to_intermediate(self):
        result = []
        radios = []
        wireless = {radio(w): w for w in self.wireless}
        for logic in self.radio:
            w = wireless.get(logic['name'])
            if w:
                user_config = radio_available_mode[mode(w)](logic)
                radios.append(user_config)

        result.append(radios)
        result.append(radio_configuration)
        return (('radio', result),)


class Resolv(AirOsConverter):
    netjson_key = 'dns_servers'

    def host(self):
        original = get_copy(self.netjson, 'general', {})
        return {
            'host': [{
                'name': original.get('hostname', 'airos'),
                'status': 'enabled',
            }],
        }

    def nameserver(self):
        result = []
        original = get_copy(self.netjson, self.netjson_key, [])
        for nameserver in original:
            result.append({
                'ip': nameserver,
                'status': 'enabled',
            })
        return {'nameserver': result}

    def to_intermediate(self):
        result = []
        result.append(self.host())
        result.append(self.nameserver())
        result.append({'status': 'enabled'})
        return (('resolv', result),)


class Route(AirOsConverter):
    netjson_key = 'routes'

    def default_routes(self):
        def is_default_route(interface):
            try:
                t = [addr.get('gateway', '') for addr in interface['addresses']]
                return any(t)
            except KeyError:
                return False

        result = []
        original = [x for x in get_copy(self.netjson, 'interfaces', []) if is_default_route(x)]
        for interface in original:
            for address in interface['addresses']:
                try:
                    result.append({
                        'devname': interface['name'],
                        'gateway': address['gateway'],
                        'ip': '0.0.0.0',
                        'netmask': 0,
                        'status': 'enabled',
                    })
                except KeyError:
                    pass
        return result

    def to_intermediate(self):
        result = []
        routes = []
        routes = self.default_routes()
        original = get_copy(self.netjson, self.netjson_key, [])
        for r in original:
            network = ip_interface(r['destination'])
            temp = {}
            temp['ip'] = str(network.ip)
            temp['netmask'] = str(network.netmask)
            routes.append({
                'gateway': r['next'],
                'ip': temp['ip'],
                'netmask': temp['netmask'],
                'status': 'enabled',
            })
        result.append(routes)
        result.append({'status': 'enabled'})
        return (('route', result),)


class Snmp(AirOsConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        original = get_copy(self.netjson, self.netjson_key, {})
        result = [
           {
                'community':  'public',
                'contact':  original.get('mantainer', ''),
                'location':  original.get('location', ''),
                'status':  'enabled',
            },
        ]
        return (('snmp', result),)


class Sshd(AirOsConverter):
    netjson_key = 'sshd'

    def to_intermediate(self):
        def status(original, key='enabled'):
            if original.get(key, True):
                return 'enabled'
            else:
                return 'disabled'

        def to_key(x):
            result = []
            for y in x:
                result.append({
                    'status': status(y),
                    'type': y['type'],
                    'value': y['key'],
                    'comment': y.get('comment', '')
                })
            return result

        result = []
        original = get_copy(self.netjson, self.netjson_key, {})
        auth = {'passwd': status(original, 'password_auth')}
        key = to_key(original.get('keys', []))
        if key:
            auth.update({'key': key})

        result.append({
            'auth': auth,
            'port': original.get('port', 22),
            'status': status(original, 'enabled'),
        })
        return (('sshd', result),)


class Syslog(AirOsConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'remote': {
                'port': 514,
                'status': 'disabled',
            },
            'status': 'enabled',
        })
        return (('syslog', result),)


class System(AirOsConverter):
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
                'status': 'disabled',
            },
            'external': {
                'reset': 'enabled',
            },
            'timezone': 'GMT',
        })
        return (('system', result),)


class Telnetd(AirOsConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []
        result.append({
            'port': 23,
            'status': 'disabled',
        })
        return (('telnetd', result),)


class Tshaper(AirOsConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        return (('tshaper', [{'status': 'disabled'}]),)


class Unms(AirOsConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        return (('unms', [{'status': 'disabled'}]),)


class Update(AirOsConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []
        result.append({'check': {'status': 'enabled'}})
        return (('update', result),)


class Upnpd(AirOsConverter):
    @classmethod
    def should_run_forward(cls, config):
        if config.get('netmode', 'bridge') == 'bridge':
            return False
        else:
            return True

    def to_intermediate(self):
        return (('upnpd', [{'status': 'disabled'}]),)


class Users(AirOsConverter):
    netjson_key = 'user'

    def key_derivation(self):
        original = get_copy(self.netjson, self.netjson_key, {})
        return '$1${salt}${derivation}'.format(salt=original['salt'], derivation=original['password'])

    def to_intermediate(self):
        result = []
        original = get_copy(self.netjson, self.netjson_key, {})
        result.append({'status': 'enabled'})
        result.append([
            {
                'name': original.get('name'),
                'password': self.key_derivation(),
                'status': 'enabled',
            },
        ])
        return (('users', result),)


class Vlan(AirOsConverter):
    netjson_key = 'interfaces'

    @property
    def vlan(self):
        return vlan(get_copy(self.netjson, self.netjson_key, []))

    def to_intermediate(self):
        result = []
        vlans = []
        for v in self.vlan:
            vlans.append({
                'comment': v.get('comment', ''),
                'devname': v['name'].split('.')[0],
                'id': v['name'].split('.')[1],
                'status': status(v),
            })
        result.append(vlans)
        result.append({'status': 'enabled'})
        return (('vlan', result),)


class Wireless(AirOsConverter):
    netjson_key = 'interfaces'

    @property
    def wireless(self):
        """
        Return all the wireless interfaces
        """
        return wireless(get_copy(self.netjson, 'interfaces', []))

    def to_intermediate(self):
        result = []
        wireless_list = []
        for w in self.wireless:
            user_config = wireless_available_mode[mode(w)](w)
            wireless_list.append(user_config)
        result.append(wireless_list)
        result.append({'status': 'enabled'})
        return (('wireless', result),)


class Wpasupplicant(AirOsConverter):
    netjson_key = 'interfaces'

    @property
    def wireless(self):
        """
        Return all the wireless interfaces
        """
        return wireless(get_copy(self.netjson, 'interfaces', []))

    def _station_intermediate(self, original):
        station_auth_protocols = available_mode_authentication['station']
        temp_dev = {
            'profile': 'AUTO',
            'status': 'enabled',
            'driver': 'madwifi',
            'devname': '',
        }
        result = []

        if original:
            head = original[0]
            proto = protocol(head)
            temp_dev['devname'] = radio(head)
            network = station_auth_protocols[proto](head)

            if proto == 'none':
                del temp_dev['driver']
                del temp_dev['devname']

        result.append({
            'device': [temp_dev],
            'profile': [
                {
                    'name': 'AUTO',
                    'network': [network, self.secondary_network()]
                }
            ]
        })
        result.append({'status': 'enabled'})
        return (('wpasupplicant', result),)

    def _access_point_intermediate(self, original):
        """
        Intermediate representation for ``access_point`` mode
        """
        ap_auth_protocols = available_mode_authentication['access_point']
        temp_dev = {
            'profile': 'AUTO',
        }
        wpasupplicant_status = {
            'none': 'enabled',
            'wpa2_personal': 'disabled',
            'wpa2_enterprise': 'disabled',
        }
        result = []

        if original:
            head = original[0]
            proto = protocol(head)
            status = wpasupplicant_status[proto]
            result.append({
                'status': status
            })
            temp_dev['status'] = status
            network = ap_auth_protocols[proto](head)
            profile = {
                'name': 'AUTO',
                'network': [network, self.secondary_network()],
            }

            if proto == 'wpa2_enterprise':
                del temp_dev['profile']
                del profile['name']

        result.append({
            'device': [temp_dev],
            'profile': [profile],
        })
        return (('wpasupplicant', result),)

    def secondary_network(self):
        """
        The default secondary network configuration
        """
        return {
            'key_mgmt': [{'name': 'NONE'}],
            'priority': 2,
            'status': 'disabled',
        }

    def to_intermediate(self):
        try:
            head = self.wireless[0]
            # call either ``_station_intermediate`` or ``_access_point_intermediate``
            # and return the result
            return getattr(self, '_%s_intermediate' % head['wireless']['mode'])(self.wireless)
        except IndexError:
            raise Warning('Zero wireless interface found')
