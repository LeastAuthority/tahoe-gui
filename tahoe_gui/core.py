# -*- coding: utf-8 -*-

import logging
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

from tahoe_gui.invite import InviteForm
from tahoe_gui.systray import SystemTrayIcon


class Core(object):
    def __init__(self, args):
        self.args = args
        self.tray = None

    def notify(self, title, message):
        self.tray.showMessage(title, message, msecs=5000)

    def start(self):
        if self.args.debug:
            logging.basicConfig(
                format='%(asctime)s %(funcName)s %(message)s',
                level=logging.DEBUG,
                stream=sys.stdout)
        else:
            logging.basicConfig(
                format='%(asctime)s %(funcName)s %(message)s',
                level=logging.INFO,
                stream=sys.stdout)
        logging.info("Core starting with args: %s", self.args)
        logging.debug("$PATH is: %s", os.getenv('PATH'))

        # XXX TODO: Load config, check if first run, launch tahoe daemons, etc.

        self.tray = SystemTrayIcon(self)
        self.tray.show()
        inv = InviteForm()
        inv.show()
        inv.raise_()

        reactor.run()
