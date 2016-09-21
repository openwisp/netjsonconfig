from copy import deepcopy

from ...utils import sorted_dict
from ..base import BaseRenderer


class OpenVpnRenderer(BaseRenderer):
    """
    Produces an OpenVPN configuration string
    """
    def cleanup(self, output):
        # remove indentations
        output = output.replace('    ', '')
        # remove last newline
        if output.endswith('\n\n'):
            output = output[0:-1]
        return output

    def _transform_vpn(self, vpn):
        config = deepcopy(vpn)
        skip_keys = ['script_security', 'remote']
        delete_keys = []
        # allow server_bridge to be empty and still rendered
        if config.get('server_bridge') == '':
            config['server_bridge'] = True
        for key, value in config.items():
            if key in skip_keys:
                continue
            # mark keys which contain falsy values
            # usually not useful in the openvpn configuration format
            if any([value is False, value is 0, value == '']):
                delete_keys.append(key)
        # delete config keys which are not needed (marked previously)
        for key in delete_keys:
            del config[key]
        # reformat remote list in order for simpler handling in template
        if 'remote' in config:
            remote = ['{host} {port}'.format(**r) for r in config['remote']]
            config['remote'] = remote
        # do not display status-version if status directive not present
        if 'status' not in config and 'status_version' in config:
            del config['status_version']
        return config

    def _get_openvpn(self):
        openvpn = []
        for vpn in self.config.get('openvpn', []):
            config = self._transform_vpn(vpn)
            openvpn.append(sorted_dict(config))
        return openvpn
