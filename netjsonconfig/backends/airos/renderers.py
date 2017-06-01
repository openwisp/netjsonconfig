from ..base.renderer import BaseRenderer


class AirOS(BaseRenderer):

    def cleanup(self, output):
        stripped = [
                a.strip() for a in output.splitlines() if a.strip()
                ]
        return '\n'.join(stripped)
