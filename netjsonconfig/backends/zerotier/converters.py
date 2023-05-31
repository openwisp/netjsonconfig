from ..base.converter import BaseConverter
from .schema import schema


class ZeroTier(BaseConverter):
    netjson_key = 'zerotier'
    intermediate_key = 'zerotier'
    _schema = schema

    def to_intermediate_loop(self, block, result, index=None):
        vpn = self.__intermediate_vpn(block)
        result.setdefault('zerotier', [])
        result['zerotier'].append(vpn)
        return result

    def __intermediate_vpn(self, config, remove=[False, 0, '']):
        # The Zerotier network configuration keys taken from:
        # https://github.com/zerotier/ZeroTierOne/blob/dev/node/NetworkConfig.hpp
        config['nwid'] = config.pop('id')
        config['t'] = config.pop('objtype')
        config['r'] = config.pop('revision')
        config['ts'] = config.pop('creationTime')
        config['n'] = config.pop('name')
        config['p'] = config.pop('private')
        config['eb'] = config.pop('enableBroadcast')
        config['v4s'] = config.pop('v4AssignMode')
        config['v6s'] = config.pop('v6AssignMode')
        config['mtu'] = config.pop('mtu')
        config['ml'] = config.pop('multicastLimit')
        config['I'] = config.pop('ipAssignmentPools')
        config['RT'] = config.pop('routes')
        config['DNS'] = config.pop('dns')
        config['R'] = config.pop('rules')
        config['CAP'] = config.pop('capabilities')
        config['TAG'] = config.pop('tags')
        config['tt'] = config.pop('remoteTraceTarget')
        config['tl'] = config.pop('remoteTraceLevel')
        return self.sorted_dict(config)
