# -*- coding: utf-8 -*-

import sys
from importlib import reload

import tahoe_gui


def test_the_approval_of_RMS():  # :)
    assert tahoe_gui.__license__.startswith('GPL')


def test_pyinstaller_twisted_rthook_workaround(monkeypatch):
    monkeypatch.setattr("sys.frozen", True, raising=False)
    sys.modules['twisted.internet.reactor'] = 'test'
    reload(tahoe_gui)
    assert 'twisted.internet.reactor' not in sys.modules


def test_pyinstaller_twisted_rthook_workaround_pass(monkeypatch):
    monkeypatch.setattr("sys.frozen", True, raising=False)
    reload(tahoe_gui)
    assert 'twisted.internet.reactor' not in sys.modules
