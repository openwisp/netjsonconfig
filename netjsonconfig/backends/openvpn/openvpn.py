import re

from ..base import BaseBackend
from .renderers import OpenVpnRenderer
from .schema import schema


class OpenVpn(BaseBackend):
    """
    OpenVPN 2.3 backend
    """
    schema = schema
    env_path = 'netjsonconfig.backends.openvpn'
    renderers = [OpenVpnRenderer]
    VPN_REGEXP = re.compile('# openvpn config: ')

    def _generate_contents(self, tar):
        """
        Adds configuration files to tarfile instance.

        :param tar: tarfile instance
        :returns: None
        """
        text = self.render(files=False)
        # create a list with all the packages (and remove empty entries)
        vpn_instances = self.VPN_REGEXP.split(text)
        if '' in vpn_instances:
            vpn_instances.remove('')
        # for each package create a file with its contents in /etc/config
        for vpn in vpn_instances:
            lines = vpn.split('\n')
            vpn_name = lines[0]
            text_contents = '\n'.join(lines[2:])
            # do not end with double new line
            if text_contents.endswith('\n\n'):
                text_contents = text_contents[0:-1]
            self._add_file(tar=tar,
                           name='{0}.conf'.format(vpn_name),
                           contents=text_contents)

    @classmethod
    def generate_client(self, host, server):
        """
        Generates an OpenVPN client configuration
        from an existing server configuration.

        :param server: dictionary representing a single OpenVPN server configuration
        :returns: dictionary representing a single OpenVPN client configuration
        """
        # client defaults
        c = {
            "mode": "client",
            "nobind": True,
            "resolv_retry": True,
            "tls_client": True
        }
        # remote
        port = server.get('port') or 1195
        c['remote'] = [{'host': host, 'port': port}]
        # proto
        if server.get('proto') == 'tcp-server':
            c['proto'] = 'tcp-client'
        else:
            c['proto'] = 'udp'
        # tls_client
        if 'tls_server' not in server or not server['tls_server']:
            c['tls_client'] = False
        # ns_cert_type
        if not server.get('ns_cert_type'):
            c['ns_cert_type'] = ''
        elif server.get('ns_cert_type') == 'client':
            c['ns_cert_type'] = 'server'
        copy_keys = ['name', 'dev_type', 'dev', 'comp_lzo', 'auth',
                     'cipher', 'ca', 'cert', 'key', 'mtu_disc', 'mtu_test',
                     'fragment', 'mssfix', 'keepalive', 'persist_tun', 'mute',
                     'persist_key', 'script_security', 'user', 'group', 'log',
                     'mute_replay_warnings', 'secret', 'fast_io', 'verb']
        for key in copy_keys:
            if key in server:
                c[key] = server[key]
        return c
