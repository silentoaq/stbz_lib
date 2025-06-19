# tests/test_mouse.py

from stbz_lib import mouse_block, mouse_hold, mouse_move, mouse_pos, mouse_tap, mouse_unblock


def test_mouse_block():
    assert callable(mouse_block)


def test_mouse_unblock():
    assert callable(mouse_unblock)


def test_mouse_tap():
    assert callable(mouse_tap)


def test_mouse_hold():
    assert callable(mouse_hold)


def test_mouse_pos():
    assert callable(mouse_pos)


def test_mouse_move():
    assert callable(mouse_move)
