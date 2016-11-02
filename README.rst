=========
Tahoe-GUI
=========

.. image:: https://api.travis-ci.org/LeastAuthority/tahoe-gui.svg
    :target: https://travis-ci.org/LeastAuthority/tahoe-gui
.. image:: https://ci.appveyor.com/api/projects/status/github/LeastAuthority/tahoe-gui?svg=true
    :target: https://ci.appveyor.com/project/crwood/tahoe-gui


A cross-platform GUI for `Tahoe-LAFS`_. Inspired by `Gridsync`_.

.. _Tahoe-LAFS: https://tahoe-lafs.org
.. _Gridsync: http://gridsync.io


Installation / Running:
-----------------------

From source (requires Python 3.5):

1. ``python3.5 -m pip install git+https://github.com/LeastAuthority/tahoe-gui.git``
2. ``tahoe-gui``

Mac OS X:

1. Download `Tahoe-GUI.dmg`_
2. Drag the contained Tahoe-GUI.app bundle anywhere (e.g., `~/Applications`)
3. Double-click ``Tahoe-GUI.app``

Windows (64-bit):

1. Download `Tahoe-GUI-win64.zip`_
2. Extract the contained Tahoe-GUI folder anywhere
3. Double-click ``Tahoe-GUI.exe``

.. _Tahoe-GUI.dmg: https://buildbot.gridsync.io/packages/Tahoe-GUI.dmg
.. _Tahoe-GUI-win64.zip: https://buildbot.gridsync.io/packages/Tahoe-GUI-win64.zip

Debian:

To install from inside a clone of this repository on Debian (tested on
"jessie"):

1. `sudo apt-get install virtualenv python3 python-pyqt5`
2. `virtualenv --python=python3 --system-site-packages venv`
3. `./venv/bin/pip install --upgrade pip setuptools`
4. `./venv/bin/pip install --editable .`

The "upgrade" step is because the `pip` that ships with the Debian
virtualenv package is very old.
