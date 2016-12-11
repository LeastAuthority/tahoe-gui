# -*- coding: utf-8 -*-

from __future__ import print_function

import json
import os

from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QCheckBox, QCompleter, QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QProgressBar, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
from twisted.internet import reactor
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from wormhole.errors import WrongPasswordError
from wormhole.wordlist import raw_words
from wormhole.wormhole import wormhole

from tahoe_gui.config import config_dir
from tahoe_gui.resource import resource
from tahoe_gui.tahoe import Tahoe

appid = u"lothar.com/wormhole/text-or-file-xfer"
#relay = u"ws://wormhole-relay.lothar.com:4000/v1"
relay = u"ws://leastauthority.com:4000/v1"


wordlist = []
for word in raw_words.items():
    wordlist.extend(word[1])
wordlist = sorted([word.lower() for word in wordlist])


def is_valid(code):
    words = code.split('-')
    if len(words) != 3:
        return False
    elif not words[0].isdigit():
        return False
    elif not words[1] in wordlist:
        return False
    elif not words[2] in wordlist:
        return False
    else:
        return True


def sleep(seconds):
    d = Deferred()
    reactor.callLater(seconds, d.callback, seconds)
    return d


# Adapted from 'xfer_util.py' which is not yet in magic-wormhole stable
# https://github.com/warner/magic-wormhole/blob/master/src/wormhole/xfer_util.py
@inlineCallbacks
def wormhole_receive(code, use_tor=None):
    wh = wormhole(appid, relay, reactor, use_tor)
    wh.set_code(code)
    data = yield wh.get()
    data = json.loads(data.decode("utf-8"))
    offer = data.get('offer', None)
    if not offer:
        raise Exception("Do not understand response: {}".format(data))
    msg = None
    if 'message' in offer:
        msg = offer['message']
        wh.send(json.dumps({"answer": {"message_ack": "ok"}}).encode("utf-8"))
    else:
        raise Exception("Unknown offer type: {}".format(offer.keys()))
    yield wh.close()
    returnValue(json.loads(msg))


class Completer(QCompleter):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setMaxVisibleItems(5)
        #self.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompletionMode(QCompleter.InlineCompletion)

    def pathFromIndex(self, index):
        path = QCompleter.pathFromIndex(self, index)
        words = self.widget().text().split('-')
        if len(words) > 1:
            path = '{}-{}'.format('-'.join(words[:-1]), path)
        return path

    def splitPath(self, path):
        return [str(path.split('-')[-1])]


class LineEdit(QLineEdit):
    def __init__(self):
        super(self.__class__, self).__init__()
        font = QFont()
        font.setPointSize(16)
        model = QStringListModel()
        model.setStringList(wordlist)
        completer = Completer()
        completer.setModel(model)
        self.setFont(font)
        self.setCompleter(completer)
        self.setAlignment(Qt.AlignCenter)
        #self.setPlaceholderText("Enter invite code")

    def keyPressEvent(self, event):
        key = event.key()
        text = self.text()
        if key == Qt.Key_Space:
            if text and not text.endswith('-'):
                self.setText(text + '-')
        elif key == Qt.Key_Tab:
            if text and len(text.split('-')) < 3 and not text.endswith('-'):
                self.setText(text + '-')
            else:
                self.setText(text)
        else:
            return QLineEdit.keyPressEvent(self, event)


class InviteForm(QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.resize(500, 333)
        layout = QVBoxLayout(self)

        layout_1 = QHBoxLayout()
        self.icon = QLabel()
        pixmap = QPixmap(resource('mail-envelope-open.png')).scaled(128, 128)
        self.icon.setPixmap(pixmap)
        layout_1.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, 0))
        layout_1.addWidget(self.icon)
        layout_1.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, 0))

        layout_2 = QHBoxLayout()
        self.label = QLabel("Enter invite code:")
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setStyleSheet("color: grey")
        layout_2.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, 0))
        layout_2.addWidget(self.label)
        layout_2.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, 0))

        layout_3 = QHBoxLayout()
        self.lineedit = LineEdit()
        self.lineedit.returnPressed.connect(self.return_pressed)
        self.progressbar = QProgressBar()
        self.progressbar.setMaximum(8)
        self.progressbar.setTextVisible(False)
        self.progressbar.hide()
        layout_3.addItem(QSpacerItem(85, 0, QSizePolicy.Preferred, 0))
        layout_3.addWidget(self.lineedit)
        layout_3.addWidget(self.progressbar)
        layout_3.addItem(QSpacerItem(85, 0, QSizePolicy.Preferred, 0))

        layout_4 = QHBoxLayout()
        self.checkbox = QCheckBox(self)
        self.checkbox.setText("Always connect using Tor")
        self.checkbox.setEnabled(True)
        self.checkbox.setCheckable(False)
        self.checkbox.setStyleSheet("color: grey")
        self.checkbox.setFocusPolicy(Qt.NoFocus)
        self.message = QLabel()
        self.message.hide()
        layout_4.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, 0))
        layout_4.addWidget(self.checkbox)
        layout_4.addWidget(self.message)
        layout_4.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, 0))

        layout.addItem(QSpacerItem(0, 0, 0, QSizePolicy.Expanding))
        layout.addLayout(layout_1)
        layout.addLayout(layout_2)
        layout.addLayout(layout_3)
        layout.addLayout(layout_4)
        layout.addItem(QSpacerItem(0, 0, 0, QSizePolicy.Expanding))

    def update_progress(self, step, message):
        self.progressbar.setValue(step)
        self.progressbar.show()
        self.message.setStyleSheet("color: grey")
        self.message.setText(message)
        self.message.show()

    def show_error(self, message):
        self.message.setStyleSheet("color: red")
        self.message.setText(message)
        self.checkbox.hide()
        self.message.show()
        reactor.callLater(3, self.message.hide)
        reactor.callLater(3, self.checkbox.show)

    @inlineCallbacks
    def setup(self, settings):
        folder = os.path.join(os.path.expanduser('~'), 'Private')
        try:
            os.makedirs(folder)
        except OSError:
            pass

        self.update_progress(2, 'Creating gateway...')
        tahoe = Tahoe(os.path.join(config_dir, 'default'))
        args = ['create-client', '--webport=tcp:0:interface=127.0.0.1']
        for option in ('nickname', 'introducer'):
            # TODO: Add 'needed', 'happy', 'total' pending tahoe-lafs PR #376
            # https://github.com/tahoe-lafs/tahoe-lafs/pull/376
            if option in settings:
                args.extend(['--{}'.format(option), settings[option]])
        yield tahoe.command(args)

        self.update_progress(3, 'Configuring gateway...')
        for option in ('needed', 'happy', 'total'):
            if option in settings:
                tahoe.config_set('client', 'shares.{}'.format(option),
                                 settings[option])

        self.update_progress(4, 'Starting gateway...')
        yield tahoe.start()

        self.update_progress(5, 'Connecting to grid...')
        # TODO: Replace with call to "readiness" API?
        # https://tahoe-lafs.org/trac/tahoe-lafs/ticket/2844
        yield sleep(2)

        self.update_progress(6, 'Creating magic-folder...')
        yield tahoe.command(['magic-folder', 'create', 'magic:', 'admin',
                             folder])

        self.update_progress(7, 'Reloading...')
        yield tahoe.start()

        self.update_progress(8, 'Done!')
        yield sleep(1)
        # TODO: Open local folder with file manager instead?
        yield tahoe.command(['webopen'])
        self.close()

    def reset(self):
        self.update_progress(0, '')
        self.label.setText("Enter invite code:")
        self.progressbar.hide()
        self.message.hide()
        self.lineedit.show()
        self.checkbox.show()

    def show_failure(self, failure):
        print(failure)
        if failure.type == WrongPasswordError:
            # The original magic-wormhole error text is as follows:
            #   "ERROR:  Key confirmation failed. Either you or your
            #   correspondent typed the code wrong, or a would-be
            #   man-in-the-middle attacker guessed incorrectly. You could try
            #   again, giving both your correspondent and the attacker another
            #   chance."
            self.show_error("Invite confirmation failed.")
            QMessageBox.warning(
                self, "Invite confirmation failed.",
                "Either you mistyped your invite code, or a potential "
                "attacker tried to guess your code and failed. To try "
                "again, you will need to obtain a new invite code from "
                "your inviter.", QMessageBox.Retry)  # or "service provider"?
            self.reset()
        elif failure.type == json.decoder.JSONDecodeError:
            self.show_error("Invalid response.")
            QMessageBox.critical(
                self, "Invalid response.",
                "Your invite code worked but your inviter did not provide "
                "the information needed to complete the invitation process. "
                "Please let them know about the error, and try again later "
                "with a new invite code.", QMessageBox.Retry)
            self.reset()
        # XXX: Other errors?

    def return_pressed(self):
        code = self.lineedit.text().lower()
        if is_valid(code):
            self.label.setText('')
            self.lineedit.hide()
            self.checkbox.hide()
            self.update_progress(1, 'Opening wormhole...')
            d = wormhole_receive(code)
            d.addCallback(self.setup)
            d.addErrback(self.show_failure)
        else:
            self.show_error("Invalid code")
