# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QWizard, QWizardPage)


class WelcomePage(QWizardPage):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setTitle("Welcome to Tahoe-LAFS!")
        label = QLabel("Sign-up/wormhole flow goes here..")
        vbox = QVBoxLayout(self)
        vbox.addWidget(label)


class Wizard(QWizard):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setWindowTitle("Tahoe-LAFS - Welcome")
        self.resize(800, 500)
        self.welcome_page = WelcomePage()
        self.addPage(self.welcome_page)
        self.finished.connect(self.finish)

    def finish(self):  # pylint: disable=no-self-use
        sys.exit(0)
