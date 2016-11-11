# -*- coding: utf-8 -*-

import os
import sys


if sys.platform == 'win32':
    config_dir = os.path.join(os.getenv('APPDATA'), 'Tahoe-GUI')
elif sys.platform == 'darwin':
    config_dir = os.path.join(
        os.path.expanduser('~'), 'Library', 'Application Support', 'Tahoe-GUI')
else:
    basedir = os.environ.get(
        'XDG_CONFIG_HOME', os.path.join(os.path.expanduser('~'), '.config'))
    config_dir = os.path.join(basedir, 'tahoe-gui')
