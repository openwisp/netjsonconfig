#!/usr/bin/env python
import os
import sys

from setuptools import find_packages, setup

# avoid ImportError when dependencies are not installed yet
sys.path.insert(0, 'netjsonconfig')
from version import get_version
sys.path.remove('netjsonconfig')

if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'\n")

if sys.argv[-1] == 'publish':
    if sys.version_info.major < 3:
        print('Error: do not publish release with python2!')
        sys.exit(1)
    os.system('find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf')
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload -s dist/*")
    os.system("rm -rf dist build")
    args = {'version': get_version()}
    print("You probably want to also tag the version now:")
    print("  git tag -a %(version)s -m 'version %(version)s'" % args)
    print("  git push --tags")
    sys.exit()

extras_require = {
    # used for wheel package,
    # see http://wheel.readthedocs.io/en/latest/#defining-conditional-dependencies
    ':python_version in "2.6 2.7"': ['py2-ipaddress']
}


def get_install_requires():
    """
    parse requirements.txt, ignore links, exclude comments
    """
    requirements = []
    for line in open('requirements.txt').readlines():
        # skip to next iteration if comment or empty line
        if line.startswith('#') or line == '' or line.startswith('http') or line.startswith('git'):
            continue
        # add line to requirements
        requirements.append(line.replace('\n', ''))
    # add py2-ipaddress if python2
    if sys.version_info.major < 3:
        requirements.append('py2-ipaddress')
    return requirements


description = 'Netjsonconfig is a python library that converts NetJSON DeviceConfiguration '\
              'objects into real router configurations that can be installed on systems like '\
              'OpenWRT or OpenWisp Firmware.'

setup(
    name='netjsonconfig',
    version=get_version(),
    description=description,
    long_description=open('README.rst').read(),
    author='Federico Capoano (nemesisdesign)',
    author_email='f.capoano@cineca.it',
    license='GPL3',
    url='http://netjsonconfig.openwisp.org',
    download_url='https://github.com/openwisp/netjsonconfig/releases',
    keywords=['openwrt', 'openwisp', 'netjson', 'networking'],
    packages=find_packages(exclude=['tests', 'tests.*', 'docs', 'docs.*']),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Networking',
    ],
    install_requires=get_install_requires(),
    extras_require=extras_require,
    test_suite='nose.collector',
    scripts=['bin/netjsonconfig'],
)
