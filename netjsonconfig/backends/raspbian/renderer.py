from ..base.renderer import BaseRenderer


class RaspbianRenderer(BaseRenderer):
    def cleanup(self, output):
        output = output.replace('    ', '')
        return output
    pass


class Scripts(RaspbianRenderer):
    pass


class Hostname(RaspbianRenderer):
    pass


class Hostapd(RaspbianRenderer):
    pass


class Interfaces(RaspbianRenderer):
    pass


class Resolv(RaspbianRenderer):
    pass


class Ntp(RaspbianRenderer):
    pass
