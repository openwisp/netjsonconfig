
from ..base import BaseRenderer

class BaseAirOSRenderer(BaseRenderer):

    def cleanup(self, output):
       return output 


class SystemRenderer(BaseAirOSRenderer):
    """
    Write configuration for
    - resolv
    - system
    - users
    """

    def _get_resolv(self):
        dns_server = self.config.get('dns_servers', [])
        return {
                'nameserver' : reversed(list(enumerate(dns_server))),
        }

    def _get_system(self):
        general = self.config.get('general', {}).copy()
        if general:
            general['timezone'] = general.get('timezone', 'UTC')
            general['latitude'] = general.get('latitude', '')
            general['longitude'] = general.get('longitude', '')
            general['timestamp'] = general.get('timestamp','')
            general['reset'] = general.get('reset', 'enabled')

        return general

    
class NetworkRenderer(BaseAirOSRenderer):
    """
    Write configuration for
    - bridge
    """

    def _get_bridge(self):
        interfaces = self.config.get('interfaces', [])
        bridge_def = [
                i for i in interfaces if i['type'] == 'bridge'
                ]
        return reversed(list(enumerate(bridge_def)))
