from ..base import BaseRenderer

class BaseRaspbianRenderer(BaseRenderer):
    def cleanup(self, output):
        return output

class NetworkRenderer(BaseRaspbianRenderer):
    """
    Write configurations for
    - resolv
    - dns servers
    """
    def _get_dns_servers(self):
        dns_servers = self.config.get('dns_servers', [])
        if dns_servers:
            return dns_servers

    def _get_dns_search(self):
        dns_search = self.config.get('dns_search', None)
        if dns_search:
            return dns_search


class WirelessRenderer(BaseRaspbianRenderer):
    """
    Write configurations for
    - interfaces
    """
    def _get_interface(self):
        interfaces = self.config.get('interfaces', {})
