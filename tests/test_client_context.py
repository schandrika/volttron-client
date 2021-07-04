import os
from pathlib import Path

import gevent
from unittest import mock
import pytest

from volttron.client.context import ClientContext

@pytest.fixture
def undocontext():
    # Resets the context of volttron_home klass
    # variable (NOTE not sure if this is the best
    # way or not to undo this.)
    yield

    ClientContext.__volttron_home__ = None


def test_default_VOLTTRON_HOME(undocontext):
    # must be ~/.volttron as default
    path = Path("~/.volttron").expanduser().resolve()
    
    assert str(path) == ClientContext.get_volttron_home()
    assert Path(path).exists()


def test_can_use_VOLTTRON_HOME_DIR(monkeypatch, undocontext):

    original_volttron_home = "/tmp/volttron/testing"
    monkeypatch.setenv("VOLTTRON_HOME", original_volttron_home)

    volttron_home = ClientContext.get_volttron_home()

    assert original_volttron_home == volttron_home
    

def test_change_VOLTTRON_HOME_raises_exception(monkeypatch, undocontext):
    
    volttron_home = ClientContext.get_volttron_home()
    
    monkeypatch.setenv("VOLTTRON_HOME", "~/differnt_vhome")
    
    with pytest.raises(ValueError):
        other_vhome = ClientContext.get_volttron_home() 

    
def test_context_in_gevent(monkeypatch, undocontext):

    my_original = "/tmp/volttron/t4"
    
    def in_gevent():
        nonlocal my_original
        changed = "/tmp/volttron/test/t1"
        monkeypatch.setenv("VOLTTRON_HOME", changed)
        with pytest.raises(ValueError):
            ClientContext.get_volttron_home()
        # if we got here then we know we raised an error like it
        # was supposed to happen, so reset the VOLTTRON_HOME back
        # to what it was originally.
        monkeypatch.setenv("VOLTTRON_HOME", my_original)
    
    monkeypatch.setenv("VOLTTRON_HOME", my_original)
    original = ClientContext.get_volttron_home()
    assert my_original == original

    glet = gevent.spawn(in_gevent)

    gevent.joinall([glet])
    assert my_original == ClientContext.get_volttron_home()
    