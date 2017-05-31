import re

from .converters import *
from .renderers import AirOS
from ..base.backend import BaseBackend
from .schema import schema

class AirOS(BaseBackend):
    """
    AirOS backend
    """

    # backend schema validator
    schema = schema

    # converters from configuration
    # dictionary to intermediate representation
    converters = [
            Bridge,
            Gui,
            Httpd,
            Resolv,
            Snmp,
            Vlan,
            Wireless,
    ]

    # the environment where airos
    # templates lives
    env_path = 'netjsonconfig.backends.airos'

    # TODO: remove
    # list of renderers available
    # for this backend
#    renderers = [
#            renderers.SystemRenderer,
#            renderers.NetworkRenderer,
#    ]

    renderer = AirOS

#    @classmethod
#    def get_renderers(cls):
#        pass
#
#    def _generate_contents(self, tar):
#        """
#        Add configuration files rendered by backend
#        to tarfile instance
#        
#        :param tar: tarfile instance
#        :returns: None
#        """
#        pass
