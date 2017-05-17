import re

from . import renderers
from ..base import BaseBackend
from .schema import schema

class AirOS(BaseBackend):
    """
    AirOS backend
    """

    # backend schema validator
    schema = schema

    # the environment where airos
    # templates lives
    env_path = 'netjsonconfig.backends.airos'

    # list of renderers available
    # for this backend
    renderers = [
            renderers.SystemRenderer
    ]

    @classmethod
    def get_renderers(cls):
        pass

    def _generate_contents(self, tar):
        """
        Add configuration files rendered by backend
        to tarfile instance
        
        :param tar: tarfile instance
        :returns: None
        """
        pass

