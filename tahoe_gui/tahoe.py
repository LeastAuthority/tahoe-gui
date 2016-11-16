# -*- coding: utf-8 -*-

import configparser
import os
import sys

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, Deferred
from twisted.internet.error import ProcessDone
from twisted.internet.protocol import ProcessProtocol


if getattr(sys, 'frozen', False):
    os.environ["PATH"] += os.pathsep + os.path.join(
        os.path.dirname(sys.executable), 'Tahoe-LAFS')


class CommandProtocol(ProcessProtocol):
    def __init__(self, parent, callback_trigger=None):
        self.parent = parent
        self.trigger = callback_trigger
        self.done = Deferred()

    def outReceived(self, data):
        for line in data.decode('utf-8').strip().split('\n'):
            self.parent.out_received(line)
            if not self.done.called and self.trigger and self.trigger in line:
                self.done.callback(None)

    def errReceived(self, data):
        for line in data.decode('utf-8').strip().split('\n'):
            self.parent.err_received(line)

    def processEnded(self, reason):
        if not self.done.called:
            self.done.callback(None)

    def processExited(self, reason):
        if not self.done.called and not isinstance(reason.value, ProcessDone):
            self.done.errback(reason)


class Tahoe():
    def __init__(self, nodedir=None):
        self.nodedir = nodedir

    def config_set(self, section, option, value):
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read(os.path.join(self.nodedir, 'tahoe.cfg'))
        config.set(section, option, value)
        with open(os.path.join(self.nodedir, 'tahoe.cfg'), 'w') as f:
            config.write(f)

    def config_get(self, section, option):
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read(os.path.join(self.nodedir, 'tahoe.cfg'))
        return config.get(section, option)

    def out_received(self, msg):
        # TODO: Connect to Core via Qt signals/slots?
        print(">>> " + msg)

    def err_received(self, msg):
        # TODO: Connect to Core via Qt signals/slots?
        print(">>> " + msg)

    @inlineCallbacks
    def command(self, args, callback_trigger=None):
        protocol = CommandProtocol(self, callback_trigger)
        exe = 'tahoe' + ('.exe' if sys.platform == 'win32' else '')
        args = [exe] + (['-d', self.nodedir] if self.nodedir else []) + args
        env = os.environ
        env['PYTHONUNBUFFERED'] = '1'
        reactor.spawnProcess(protocol, exe, args=args, env=env)
        yield protocol.done

    @inlineCallbacks
    def start_monitor(self):
        furl = os.path.join(self.nodedir, 'private', 'logport.furl')
        yield self.command(['debug', 'flogtool', 'tail', furl])

    @inlineCallbacks
    def start(self):
        if os.path.isfile(os.path.join(self.nodedir, 'twistd.pid')):
            yield self.command(['stop'])
        yield self.command(['run'], 'client running')
        #self.start_monitor()
