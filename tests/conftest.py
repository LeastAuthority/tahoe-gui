# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication


print("QT_VERSION_STR: ", QtCore.QT_VERSION_STR)
print("PYQT_VERSION_STR: ", QtCore.PYQT_VERSION_STR)

app = QApplication([])
