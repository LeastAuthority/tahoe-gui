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

(Note: this assumes that a `tahoe` binary is already installed and available in $PATH. If not, see the virtualenv method below.)

GNU/Linux, inside a virtualenv (tested on Debian 8.6 "jessie" and Ubuntu 16.10 "Yakkety Yak"):

1. `sudo apt-get install virtualenv git build-essential python-dev libssl-dev libffi-dev python-pyqt5`
2. `virtualenv --python=python2 --system-site-packages ~/.local/venvs/tahoe-gui`
3. `~/.local/venvs/tahoe-gui/bin/pip install --upgrade pip setuptools`
4. `~/.local/venvs/tahoe-gui/bin/pip install --find-links=https://tahoe-lafs.org/deps/ git+https://github.com/tahoe-lafs/tahoe-lafs.git`
5. `~/.local/venvs/tahoe-gui/bin/pip install --upgrade git+https://github.com/LeastAuthority/tahoe-gui.git`
6. `PATH=$PATH:~/.local/venvs/tahoe-gui/bin tahoe-gui`

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

