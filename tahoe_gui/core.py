# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)
# qt5reactor must be installed after initializing QApplication but
# before running importing/importing any other Twisted code.
# See https://github.com/sunu/qt5reactor/blob/master/README.rst
import qt5reactor
qt5reactor.install()

from twisted.internet import reactor

from tahoe_gui.config import config_dir
from tahoe_gui.invite import InviteForm
from tahoe_gui.systray import SystemTrayIcon
from tahoe_gui.tahoe import Tahoe


class Core(object):
    def __init__(self, args):
        self.args = args
        self.tray = None
        self.gateways = []

    def get_nodedirs(self):
        nodedirs = []
        for filename in os.listdir(config_dir):
            filepath = os.path.join(config_dir, filename)
            if os.path.isdir(filepath):
                nodedirs.append(filepath)
        return nodedirs

    def stop(self):
        for nodedir in self.get_nodedirs():
            gateway = Tahoe(nodedir)
            gateway.stop()

    def start(self):
        try:
            os.makedirs(config_dir)
        except OSError:
            pass
        nodedirs = self.get_nodedirs()
        if nodedirs:
            for nodedir in nodedirs:
                gateway = Tahoe(nodedir)
                gateway.start()
                self.gateways.append(gateway)
        else:
            inv = InviteForm()
            inv.show()
            inv.raise_()

        self.tray = SystemTrayIcon(self)
        self.tray.show()

        reactor.addSystemEventTrigger('before', 'shutdown', self.stop)
        reactor.run()
