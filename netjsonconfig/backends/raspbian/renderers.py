from ..base.renderer import BaseRenderer


class Resolv(BaseRenderer):
    def cleanup(self, output):
        return output

class Hostapd(BaseRenderer):
    def cleanup(self, output):
        return output
