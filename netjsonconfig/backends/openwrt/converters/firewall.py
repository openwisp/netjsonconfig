from collections import OrderedDict

from ..schema import schema
from .base import OpenWrtConverter


class Firewall(OpenWrtConverter):
    netjson_key = 'firewall'
    intermediate_key = 'firewall'
    _uci_types = ['defaults', 'forwarding', 'zone', 'rule']
    _schema = schema['properties']['firewall']

    def to_intermediate_loop(self, block, result, index=None):
        forwardings = self.__intermediate_forwardings(block.pop('forwardings', {}))
        zones = self.__intermediate_zones(block.pop('zones', {}))
        rules = self.__intermediate_rules(block.pop('rules', {}))
        block.update({
            '.type': 'defaults',
            '.name': block.pop('id', 'defaults'),
        })
        result.setdefault('firewall', [])
        result['firewall'] = [self.sorted_dict(block)] + forwardings + zones + rules
        return result

    def __intermediate_forwardings(self, forwardings):
        """
        converts NetJSON forwarding to
        UCI intermediate data structure
        """
        result = []
        for forwarding in forwardings:
            resultdict = OrderedDict((('.name', self.__get_auto_name_forwarding(forwarding)),
                                      ('.type', 'forwarding')))
            resultdict.update(forwarding)
            result.append(resultdict)
        return result

    def __get_auto_name_forwarding(self, forwarding):
        if 'family' in forwarding.keys():
            uci_name = self._get_uci_name('_'.join([forwarding['src'], forwarding['dest'],
                                          forwarding['family']]))
        else:
            uci_name = self._get_uci_name('_'.join([forwarding['src'], forwarding['dest']]))
        return 'forwarding_{0}'.format(uci_name)

    def __intermediate_zones(self, zones):
        """
        converts NetJSON zone to
        UCI intermediate data structure
        """
        result = []
        for zone in zones:
            resultdict = OrderedDict((('.name', self.__get_auto_name_zone(zone)),
                                      ('.type', 'zone')))
            resultdict.update(zone)
            result.append(resultdict)
        return result

    def __get_auto_name_zone(self, zone):
        return 'zone_{0}'.format(self._get_uci_name(zone['name']))

    def __intermediate_rules(self, rules):
        """
        converts NetJSON rule to
        UCI intermediate data structure
        """
        result = []
        for rule in rules:
            if 'config_name' in rule:
                del rule['config_name']
            resultdict = OrderedDict((('.name', self.__get_auto_name_rule(rule)),
                                      ('.type', 'rule')))
            resultdict.update(rule)
            result.append(resultdict)
        return result

    def __get_auto_name_rule(self, rule):
        return 'rule_{0}'.format(self._get_uci_name(rule['name']))

    def to_netjson_loop(self, block, result, index):
        result['firewall'] = self.__netjson_firewall(block)
        return result

    def __netjson_firewall(self, firewall):
        del firewall['.type']
        _name = firewall.pop('.name')
        if _name != 'firewall':
            firewall['id'] = _name
        return self.type_cast(firewall)
