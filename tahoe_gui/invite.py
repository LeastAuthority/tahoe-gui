# -*- coding: utf-8 -*-

import binascii
import json
import os

from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QCheckBox, QCompleter, QHBoxLayout, QLabel, QLineEdit, QProgressBar,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
from twisted.internet import reactor
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
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
    returnValue(msg)


class LineEdit(QLineEdit):
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


class HorizontalSpacer(QSpacerItem):
    def __init__(self):
        super(self.__class__, self).__init__(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)


class VerticalSpacer(QSpacerItem):
    def __init__(self):
        super(self.__class__, self).__init__(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)


class InviteForm(QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.resize(450, 300)
        layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        self.icon = QLabel()
        pixmap = QPixmap(resource('mail-envelope-open.png')).scaled(128, 128)
        self.icon.setPixmap(pixmap)
        top_layout.addItem(HorizontalSpacer())
        top_layout.addWidget(self.icon)
        top_layout.addItem(HorizontalSpacer())

        middle_layout = QHBoxLayout()
        self.lineedit = LineEdit(self)
        font = QFont()
        font.setPointSize(16)
        model = QStringListModel()
        model.setStringList(wordlist)
        completer = Completer()
        completer.setModel(model)
        self.lineedit.setCompleter(completer)  # XXX: Disable?
        self.lineedit.setFont(font)
        self.lineedit.setAlignment(Qt.AlignCenter)
        self.lineedit.setPlaceholderText("Enter invite code")
        self.lineedit.returnPressed.connect(self.return_pressed)
        self.progressbar = QProgressBar()
        self.progressbar.setTextVisible(False)
        self.progressbar.hide()
        middle_layout.addItem(HorizontalSpacer())
        middle_layout.addWidget(self.lineedit)
        middle_layout.addWidget(self.progressbar)
        middle_layout.addItem(HorizontalSpacer())

        bottom_layout = QHBoxLayout()
        self.checkbox = QCheckBox(self)
        self.checkbox.setText("Always connect using Tor")
        self.checkbox.setEnabled(True)
        self.checkbox.setCheckable(False)
        self.checkbox.setStyleSheet("color: grey")
        self.checkbox.setFocusPolicy(Qt.NoFocus)
        self.label = QLabel()
        self.label.setStyleSheet("color: grey")
        self.label.hide()
        bottom_layout.addItem(HorizontalSpacer())
        bottom_layout.addWidget(self.checkbox)
        bottom_layout.addWidget(self.label)
        bottom_layout.addItem(HorizontalSpacer())

        layout.addItem(VerticalSpacer())
        layout.addLayout(top_layout)
        layout.addLayout(middle_layout)
        layout.addLayout(bottom_layout)
        layout.addItem(VerticalSpacer())

    def update_progress(self, percentage, message):
        self.progressbar.setValue(percentage)
        self.progressbar.show()
        self.label.setStyleSheet("color: grey")
        self.label.setText(message)
        self.label.show()

    def show_error(self, message):
        self.label.setStyleSheet("color: red")
        self.label.setText(message)
        self.checkbox.hide()
        self.label.show()
        reactor.callLater(3, self.label.hide)
        reactor.callLater(3, self.checkbox.show)

    @inlineCallbacks
    def setup(self, code):
        folder = os.path.join(os.path.expanduser('~'), 'Private')
        try:
            os.makedirs(folder)
        except OSError:
            pass
        self.update_progress(12.5, 'Opening wormhole...')
        data = yield wormhole_receive(code)
        settings = json.loads(data)

        self.update_progress(25, 'Creating gateway...')
        nodeid = binascii.b2a_hex(os.urandom(32)).decode('utf-8')
        tahoe = Tahoe(os.path.join(config_dir, nodeid))
        args = ['create-client', '--webport=tcp:0:interface=127.0.0.1']
        for option in ('nickname', 'introducer'):
            # TODO: Add 'needed', 'happy', 'total' pending tahoe-lafs PR #376
            # https://github.com/tahoe-lafs/tahoe-lafs/pull/376
            if option in settings:
                args.extend(['--{}'.format(option), settings[option]])
        yield tahoe.command(args)

        self.update_progress(37.5, 'Configuring gateway...')
        for option in ('needed', 'happy', 'total'):
            if option in settings:
                tahoe.config_set('client', 'shares.{}'.format(option),
                                 settings[option])

        self.update_progress(50, 'Starting gateway...')
        yield tahoe.start()

        self.update_progress(62.5, 'Connecting to grid...')
        # TODO: Replace with call to "readiness" API?
        # https://tahoe-lafs.org/trac/tahoe-lafs/ticket/2844
        yield sleep(2)

        self.update_progress(75, 'Creating magic-folder...')
        yield tahoe.command(['magic-folder', 'create', 'magic:', 'admin',
                             folder])

        self.update_progress(87.5, 'Reloading...')
        yield tahoe.start()

        self.update_progress(100, 'Done!')
        yield sleep(1)
        # TODO: Open local folder with file manager instead?
        yield tahoe.command(['webopen'])
        returnValue(None)

    def done(self, msg):
        print(msg)
        self.close()

    def return_pressed(self):
        code = self.lineedit.text().lower()
        if is_valid(code):
            self.lineedit.hide()
            self.checkbox.hide()
            d = self.setup(code)
            d.addCallback(self.done)
        else:
            self.show_error("Invalid code")
