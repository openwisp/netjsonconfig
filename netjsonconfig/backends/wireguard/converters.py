from ..base.converter import BaseConverter
from .schema import schema


class Wireguard(BaseConverter):
    netjson_key = 'wireguard'
    intermediate_key = 'wireguard'
    _schema = schema

    def to_intermediate_loop(self, block, result, index=None):
        vpn = self.__intermediate_vpn(block)
        result.setdefault('wireguard', [])
        result['wireguard'].append(vpn)
        return result

    def __intermediate_vpn(self, config, remove=None):
        config['ListenPort'] = config.pop('port')
        config['PrivateKey'] = config.pop('private_key')
        config['peers'] = self.__intermediate_peers(config.get('peers', []))
        return self.sorted_dict(config)

    def __intermediate_peers(self, peers):
        peer_list = []
        for peer in peers:
            peer['AllowedIPs'] = peer.pop('allowed_ips')
            peer['PublicKey'] = peer.pop('public_key')
            peer['Endpoint'] = peer.pop('endpoint', None)
            peer['PreSharedKey'] = peer.pop('preshared_key', None)
            peer_list.append(self.sorted_dict(peer))
        return peer_list
