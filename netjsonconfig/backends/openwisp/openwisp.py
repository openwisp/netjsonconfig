import json
import re
import six
import time
import tarfile
from io import BytesIO

from jinja2 import Environment, PackageLoader

from ..openwrt.openwrt import OpenWrt
from .schema import schema


class OpenWisp(OpenWrt):
    """ OpenWisp 1.x Backend """
    schema = schema
    openwisp_env = Environment(loader=PackageLoader('netjsonconfig.backends.openwisp',
                                                    'templates'),
                               trim_blocks=True)

    def render_template(self, template, context={}):
        template = self.openwisp_env.get_template(template)
        return template.render(**context)

    def _add_unique_file(self, item):
        """
        adds a file in self.config['files'] only if not present already
        """
        if item not in self.config['files']:
            self.config['files'].append(item)

    def _add_install(self):
        """
        generates install.sh and adds it to included files
        """
        config = self.config
        # prepare tap VPN list
        l2vpn = []
        for vpn in self.config.get('openvpn', []):
            if vpn.get('dev_type') != 'tap':
                continue
            tap = vpn.copy()
            tap['name'] = tap['config_value']
            l2vpn.append(tap)
        # prepare bridge list
        bridges = []
        for interface in self.config.get('interfaces', []):
            if interface['type'] != 'bridge':
                continue
            bridge = interface.copy()
            if bridge.get('addresses'):
                bridge['proto'] = interface['addresses'][0].get('proto')
                bridge['ip'] = interface['addresses'][0].get('address')
            bridges.append(bridge)
        # fill context
        context = dict(hostname=config['general']['hostname'],  # hostname is required
                       l2vpn=l2vpn,
                       bridges=bridges,
                       radios=config.get('radios', []))  # radios might be empty
        contents = self.render_template('install.sh', context)
        self.config.setdefault('files', [])  # file list might be empty
        # add install.sh to list of included files
        self._add_unique_file({
            "path": "/install.sh",
            "contents": contents,
            "mode": "755"
        })

    def _add_uninstall(self):
        """
        generates uninstall.sh and adds it to included files
        """
        config = self.config
        # prepare tap VPN list
        l2vpn = []
        for vpn in self.config.get('openvpn', []):
            if vpn.get('dev_type') != 'tap':
                continue
            tap = vpn.copy()
            tap['name'] = tap['config_value']
            l2vpn.append(tap)
        # fill context
        context = dict(l2vpn=l2vpn)
        contents = self.render_template('uninstall.sh', context)
        self.config.setdefault('files', [])  # file list might be empty
        # add uninstall.sh to list of included files
        self._add_unique_file({
            "path": "/uninstall.sh",
            "contents": contents,
            "mode": "755"
        })

    def _add_openvpn_scripts(self):
        l2vpn = []
        for vpn in self.config.get('openvpn', []):
            if vpn.get('dev_type') != 'tap':
                continue
            tap = vpn.copy()
            if vpn.get('up'):
                tap['up'] = vpn['up'].split('/')[-1]
            if vpn.get('down'):
                tap['down'] = vpn['down'].split('/')[-1]
            l2vpn.append(tap)
        # add scripts
        for vpn in l2vpn:
            if vpn.get('up'):
                self._add_unique_file({
                    "path": "/openvpn/{0}".format(vpn['up']),
                    "contents": self.render_template('vpn_script_up.sh'),
                    "mode": "755"
                })
            if vpn.get('down'):
                self._add_unique_file({
                    "path": "/openvpn/{0}".format(vpn['down']),
                    "contents": self.render_template('vpn_script_down.sh'),
                    "mode": "755"
                })

    def generate(self, name='openwrt-config'):
        """
        Generates an openwisp configuration archive
        """
        uci = self.render()
        tar = tarfile.open('{0}.tar.gz'.format(name), 'w:gz')
        # create a list with all the packages (and remove empty entries)
        packages = re.split('package ', uci)
        if '' in packages:
            packages.remove('')
        # for each package create a file with its contents in /etc/config
        timestamp = time.time()
        for package in packages:
            lines = package.split('\n')
            package_name = lines[0]
            text_contents = '\n'.join(lines[2:])
            text_contents = 'package {0}\n\n{1}'.format(package_name, text_contents)
            self._add_file(tar=tar,
                           name='uci/{0}.conf'.format(package_name),
                           contents=text_contents,
                           timestamp=timestamp)
        # add install.sh to included files
        self._add_install()
        # add uninstall.sh to included files
        self._add_uninstall()
        # add vpn up and down scripts
        self._add_openvpn_scripts()
        # add files resulting archive
        self._add_files(tar, timestamp)
        # close archive
        tar.close()
