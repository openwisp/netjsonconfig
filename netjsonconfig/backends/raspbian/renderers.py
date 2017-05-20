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


class WirelessRenderer(BaseRaspbianRenderer):
    """
    Write configurations for
    - interfaces
    """
    def _get_interface(self):
        interfaces = self.config.get('interfaces', {}).copy()
        print interfaces
        # test_interface = []
        # if interfaces:
