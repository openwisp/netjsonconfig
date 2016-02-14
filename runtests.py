#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import nose
except ImportError:
    message = """nose package not installed, install test requirements with:

    pip install -r requirements-test.txt
    """
    raise ImportError(message)

if __name__ == "__main__":
    result = nose.run()
    if result is False:
        import sys
        sys.exit(1)
