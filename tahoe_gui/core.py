# -*- coding: utf-8 -*-

import logging
import os
import sys

from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)

from tahoe_gui.systray import SystemTrayIcon


class Core(object):
    def __init__(self, args):
        self.args = args
        self.tray = None

    def notify(self, title, message):
        self.tray.showMessage(title, message, msecs=5000)

    def first_run(self):  # pylint: disable=no-self-use
        from tahoe_gui.wizard import Wizard
        w = Wizard()
        w.exec_()
        logging.debug("Setup wizard finished")

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
        self.first_run()
        app.exec_()
