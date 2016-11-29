# -*- coding: utf-8 -*-

import logging
import os
import shutil

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu, QMessageBox, QSystemTrayIcon
from twisted.internet import reactor

from tahoe_gui.config import config_dir
from tahoe_gui.invite import InviteForm
from tahoe_gui.resource import resource


class RightClickMenu(QMenu):
    def __init__(self, parent):
        super(RightClickMenu, self).__init__()
        self.parent = parent
        self.invite_form = None
        self.populate()

    def populate(self):
        self.clear()
        logging.debug("(Re-)populating systray menu...")

        invite_action = QAction(QIcon(""), 'Enter Invite Code...', self)
        invite_action.triggered.connect(self.show_invite_form)
        self.addAction(invite_action)

        self.addSeparator()

        quit_action = QAction(QIcon(""), '&Quit Tahoe-GUI', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(reactor.stop)
        self.addAction(quit_action)

    def show_invite_form(self):
        nodedir = os.path.join(config_dir, 'default')
        if os.path.isdir(nodedir):
            reply = QMessageBox.question(
                self, "Tahoe-LAFS already configured",
                "Tahoe-LAFS is already configured on this computer. "
                "Do you want to overwrite your existing configuration?")
            if reply == QMessageBox.Yes:
                shutil.rmtree(nodedir, ignore_errors=True)
            else:
                return
        self.invite_form = InviteForm()
        self.invite_form.show()
        self.invite_form.raise_()


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent):
        super(SystemTrayIcon, self).__init__()
        self.parent = parent
        self.setIcon(QIcon(resource('icon.png')))
        self.right_menu = RightClickMenu(self)
        self.setContextMenu(self.right_menu)
