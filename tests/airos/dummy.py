from netjsonconfig import AirOS

from netjsonconfig.backends.airos.converters import *


class BridgeAirOS(AirOS):
    converters = [
            Bridge,
    ]

class ResolvAirOS(AirOS):
    converters = [
            Resolv,
    ]

class VlanAirOS(AirOS):
    converters = [
            Vlan,
    ]

class WirelessAirOS(AirOS):
    converters = [
            Wireless,
    ]
