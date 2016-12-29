VERSION = (0, 5, 2, 'final')
__version__ = VERSION


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        if VERSION[3] != 'final':
            mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
            version = '%s%s' % (version, mapping[VERSION[3]])
    return version
