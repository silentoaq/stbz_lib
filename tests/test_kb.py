# tests/test_kb.py

from stbz_lib import kb_block, kb_hold, kb_tap, kb_unblock


def test_kb_block():
    assert callable(kb_block)


def test_kb_unblock():
    assert callable(kb_unblock)


def test_kb_tap():
    assert callable(kb_tap)


def test_kb_hold():
    assert callable(kb_hold)
