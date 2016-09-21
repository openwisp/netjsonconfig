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
    def auto_client(self, host, server, ca_path=None, ca_contents=None,
                    cert_path=None, cert_contents=None, key_path=None,
                    key_contents=None):
        """
        Returns a configuration dictionary representing an OpenVPN client configuration
        that is compatible with the passed server configuration.

        :param host: remote VPN server
        :param server: dictionary representing a single OpenVPN server configuration
        :param ca_path: optional string representing path to CA, will consequently add
                        a file in the resulting configuration dictionary
        :param ca_contents: optional string representing contents of CA file
        :param cert_path: optional string representing path to certificate, will consequently add
                        a file in the resulting configuration dictionary
        :param cert_contents: optional string representing contents of cert file
        :param key_path: optional string representing path to key, will consequently add
                        a file in the resulting configuration dictionary
        :param key_contents: optional string representing contents of key file
        :returns: dictionary representing a single OpenVPN client configuration
        """
        # client defaults
        c = {
            "mode": "p2p",
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
        # determine if pull must be True
        if 'server' in server or 'server_bridge' in server:
            c['pull'] = True
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
        # prepare files if necessary
        files = []
        if ca_path and ca_contents:
            c['ca'] = ca_path
            files.append(dict(path=ca_path,
                              mode='0644',
                              contents=ca_contents))
        if cert_path and cert_contents:
            c['cert'] = cert_path
            files.append(dict(path=cert_path,
                              mode='0644',
                              contents=cert_contents))
        if key_path and key_contents:
            c['key'] = key_path
            files.append(dict(path=key_path,
                              mode='0644',
                              contents=key_contents))
        # prepare result
        netjson = {'openvpn': [c]}
        if files:
            netjson['files'] = files
        return netjson
