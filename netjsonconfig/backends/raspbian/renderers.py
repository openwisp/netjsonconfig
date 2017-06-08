from ..base.renderer import BaseRenderer


class Raspbian(BaseRenderer):
    def cleanup(self, output):
        return output
