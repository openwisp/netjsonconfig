from ..base import BaseRenderer

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
