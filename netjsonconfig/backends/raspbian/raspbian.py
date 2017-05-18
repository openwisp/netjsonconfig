from re

from . import renderers
from ..base import BaseBackend
from .schema import schema

class Rasbian(BaseBackend):
    """
    Rasbian Backend
    """
    schema = schema
    env_path = 'netjsonconfig.baskend.openwrt'
    renderers = [
        renderers.#
    ]
    @classmethod
    def get_renderers(cls):
        return #
    def _generate_contents(self, tar):
        return #