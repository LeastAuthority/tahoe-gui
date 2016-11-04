"A cross-platform GUI for Tahoe-LAFS"

import sys

from tahoe_gui import _version


__author__ = 'Christopher R. Wood'
__email__ = 'chris@leastauthority.com'
__url__ = 'https://github.com/LeastAuthority/tahoe-gui'
__license__ = 'GPL'
__version__ = _version.__version__


if getattr(sys, 'frozen', False):
    # This workaround is needed to bypass PyInstaller's Twisted runtime hook
    # which effectively prevents qt5reactor from being imported/installed.
    # See https://groups.google.com/forum/#!topic/pyinstaller/fbl5XOOSAtk
    try:
        del sys.modules['twisted.internet.reactor']
    except KeyError:
        pass
