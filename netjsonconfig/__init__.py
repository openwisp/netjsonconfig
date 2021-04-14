import logging

from pkg_resources import iter_entry_points

from .backends.openvpn.openvpn import OpenVpn  # noqa
from .backends.openwisp.openwisp import OpenWisp  # noqa
from .backends.openwrt.openwrt import OpenWrt  # noqa
from .backends.vxlan.vxlan_wireguard import VxlanWireguard  # noqa
from .backends.wireguard.wireguard import Wireguard  # noqa
from .version import VERSION, __version__, get_version  # noqa


def get_backends():
    default = {
        'openwrt': OpenWrt,
        'openwisp': OpenWisp,
        'openvpn': OpenVpn,
        'wireguard': Wireguard,
    }
    logger = logging.getLogger(__name__)

    for entry_point in iter_entry_points('netjsonconfig.backends'):
        try:
            default.update({entry_point.name.lower(): entry_point.load()})
        except ImportError as e:  # noqa
            logger.error("Error loading backend {}".format(entry_point.name.lower()))
    return default
