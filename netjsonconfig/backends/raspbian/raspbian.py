import re

from . import renderers
from ..base import BaseBackend
from .schema import schema

class Raspbian(BaseBackend):
    """
    Raspbian Backend
    """
    schema = schema
    env_path = 'netjsonconfig.backends.raspbian'
    renderers = [
        renderers.NetworkRenderer,
        renderers.WirelessRenderer
    ]
    @classmethod
    def get_renderers(cls):
        pass

    def _generate_contents(self, tar):
        """
        Add configuration files to tar files instance.

        :param tar: tarfile instance
        :return None
        """
        pass
