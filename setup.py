#!/usr/bin/env python
import sys
from setuptools import setup, find_packages

# avoid ImportError
sys.path.insert(0, 'netjsonconfig')
from version import get_version
sys.path.remove('netjsonconfig')


if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'\n")


if sys.argv[-1] == 'publish':
    import os
    os.system("python setup.py sdist bdist_wheel upload -s")
    args = {'version': get_version()}
    print("You probably want to also tag the version now:")
    print("  git tag -a %(version)s -m 'version %(version)s'" % args)
    print("  git push --tags")
    sys.exit()


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


setup(
    name='netjsonconfig',
    version=get_version(),
    description="Converts NetJSON DeviceConfiguration objects to real router configurations",
    long_description=open('README.rst').read(),
    author='Federico Capoano (nemesisdesign)',
    author_email='f.capoano@cineca.it',
    license='MIT',
    url='https://github.com/openwisp/netjsonconfig',
    packages=find_packages(exclude=['tests', 'tests.*', 'docs', 'docs.*']),
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Networking',
    ],
    install_requires=get_install_requires(),
    test_suite='nose.collector',
    scripts=['bin/netjsonconfig'],
)
