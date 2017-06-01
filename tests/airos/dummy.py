from netjsonconfig import AirOS

from netjsonconfig.backends.airos.converters import *


class VlanAirOS(AirOS):
    converters = [
            Vlan,
    ]
