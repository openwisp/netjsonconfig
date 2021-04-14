from ..wireguard.wireguard import Wireguard


class VxlanWireguard(Wireguard):
    @classmethod
    def auto_client(cls, vni=0, server_ip_address='', **kwargs):
        """
        Returns a configuration dictionary representing VXLAN configuration
        that is compatible with the passed server configuration.

        :param vni: Virtual Network Identifier
        :param server_ip_address: server internal tunnel address
        :returns: dictionary representing VXLAN properties
        """
        config = {
            'server_ip_address': server_ip_address,
            'vni': vni,
        }
        return config
