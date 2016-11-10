#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

from setuptools import setup


# PyQt5 wheels are only available for python 3.5 on Linux, macOS, and Windows
if (sys.version_info.major, sys.version_info.minor) != (3, 5):
    sys.exit("Please use Python version 3.5")

if sys.platform not in ('linux', 'darwin', 'win32'):
    sys.exit("Platform '{}' not supported".format(sys.platform))


metadata_file = open('tahoe_gui/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__\s*=\s*'([^']+)'", metadata_file))

version_file = open('tahoe_gui/_version.py').read()
version = re.findall("__version__\s*=\s*'([^']+)'", version_file)[0]


setup(
    name='tahoe-gui',
    version=version,
    description="A cross-platform GUI for Tahoe-LAFS",
    long_description=open('README.rst').read(),
    author=metadata['author'],
    author_email=metadata['email'],
    url=metadata['url'],
    license=metadata['license'],
    keywords='tahoe-gui tahoe-lafs-gui tahoe-lafs tahoe lafs allmydata-tahoe',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Environment :: X11 Applications :: Gnome",
        "Environment :: X11 Applications :: GTK",
        "Environment :: X11 Applications :: KDE",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: DFSG approved",
        "License :: OSI Approved",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Topic :: Communications :: File Sharing",
        "Topic :: Desktop Environment",
        "Topic :: Internet",
        "Topic :: Security",
        "Topic :: System :: Archiving",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: System :: Archiving :: Mirroring",
        "Topic :: Utilities",
    ],
    packages=['tahoe_gui'],
    package_data={
        'tahoe_gui': ['resources/*']
    },
    entry_points={
        'console_scripts': ['tahoe-gui=tahoe_gui.cli:main'],
    },
    install_requires=['PyQt5', 'qt5reactor', 'magic-wormhole'],
)
