from ..base import BaseRenderer

class BaseRaspbianRenderer(BaseRenderer):
    def cleanup(self, output):
        return output