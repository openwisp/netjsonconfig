from netjsonconfig.backends.base import BaseBackend

from .renderers import OpenVpnRenderer
from .schema import schema


class OpenVpn(BaseBackend):
    """
    OpenVPN 2.3 backend
    """
    schema = schema
    env_path = 'netjsonconfig.backends.openvpn'
    renderers = [OpenVpnRenderer]
