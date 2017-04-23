
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
        dns_server = self.config.get('dns_server', [])
