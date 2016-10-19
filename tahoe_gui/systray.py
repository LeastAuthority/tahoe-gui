# -*- coding: utf-8 -*-

import logging
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon

from tahoe_gui.resource import resource


class RightClickMenu(QMenu):
    def __init__(self, parent):
        super(RightClickMenu, self).__init__()
        self.parent = parent
        self.populate()

    def populate(self):
        self.clear()
        logging.debug("(Re-)populating systray menu...")
        quit_action = QAction(QIcon(""), '&Quit Tahoe-LAFS', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(sys.exit)
        self.addAction(quit_action)


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent):
        super(SystemTrayIcon, self).__init__()
        self.parent = parent
        self.setIcon(QIcon(resource('icon.png')))
        self.right_menu = RightClickMenu(self)
        self.setContextMenu(self.right_menu)
