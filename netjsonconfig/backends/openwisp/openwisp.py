import json
import re
import six
import time
import tarfile
from io import BytesIO

from ..openwrt.openwrt import OpenWrt


class OpenWisp(OpenWrt):
    """ OpenWisp Backend """

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
        # insert additional files
        for file_item in self.config.get('files', []):
            contents = file_item['contents']
            path = file_item['path']
            # join lines if contents is a list
            if isinstance(contents, list):
                contents = '\n'.join(contents)
            # remove leading slashes from path
            if path.startswith('/'):
                path = path[1:]
            self._add_file(tar=tar,
                           name=path,
                           contents=contents,
                           timestamp=timestamp)
        # close archive
        tar.close()
