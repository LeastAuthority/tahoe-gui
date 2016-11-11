# -*- coding: utf-8 -*-

import os
import sys
from importlib import reload

import tahoe_gui.config


def test_config_dir():
    if sys.platform == 'win32':
        assert tahoe_gui.config.config_dir == os.path.join(
            os.getenv('APPDATA'), 'Tahoe-GUI')
    elif sys.platform == 'darwin':
        assert tahoe_gui.config.config_dir == os.path.join(
            os.path.expanduser('~'), 'Library', 'Application Support',
            'Tahoe-GUI')
    else:
        assert tahoe_gui.config.config_dir == os.path.join(
            os.path.expanduser('~'), '.config', 'tahoe-gui')


def test_config_dir_win32(monkeypatch):
    monkeypatch.setattr("sys.platform", "win32")
    monkeypatch.setenv('APPDATA', 'C:\\Users\\test\\AppData\\Roaming')
    reload(tahoe_gui.config)
    assert tahoe_gui.config.config_dir == os.path.join(
        os.getenv('APPDATA'), 'Tahoe-GUI')


def test_config_dir_darwin(monkeypatch):
    monkeypatch.setattr("sys.platform", "darwin")
    reload(tahoe_gui.config)
    assert tahoe_gui.config.config_dir == os.path.join(
        os.path.expanduser('~'), 'Library', 'Application Support',
        'Tahoe-GUI')


def test_config_dir_other(monkeypatch):
    monkeypatch.setattr("sys.platform", "linux")
    reload(tahoe_gui.config)
    assert tahoe_gui.config.config_dir == os.path.join(
        os.path.expanduser('~'), '.config', 'tahoe-gui')


def test_config_dir_xdg_config_home(monkeypatch):
    monkeypatch.setattr("sys.platform", "linux")
    monkeypatch.setenv('XDG_CONFIG_HOME', '/test')
    reload(tahoe_gui.config)
    assert tahoe_gui.config.config_dir == os.path.join('/test', 'tahoe-gui')
