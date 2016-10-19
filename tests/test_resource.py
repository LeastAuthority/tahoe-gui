import os
import sys

from tahoe_gui.resource import resource


def test_resource():
    import tahoe_gui.resource
    basepath = os.path.dirname(os.path.realpath(tahoe_gui.resource.__file__))
    assert resource('test') == os.path.join(basepath, 'resources', 'test')


def test_resource_frozen(monkeypatch):
    monkeypatch.setattr("sys.frozen", True, raising=False)
    basepath = os.path.dirname(os.path.realpath(sys.executable))
    assert resource('test') == os.path.join(basepath, 'resources', 'test')
