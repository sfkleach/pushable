from pushable import *
import pytest

def test_bool_empty():
    p = Pushable( "" )
    assert not bool(p)   

def test_bool_nonempty():
    p = Pushable( "abc" )
    assert bool(p)

def test_iter_nonempty():
    p = Pushable( "abc" )
    assert ["a", "b", "c"] == list(p)

def test_next_empty():
    p = Pushable( "" )
    with pytest.raises(StopIteration):
        next(p)

def test_peek_empty():
    p = Pushable( "" )
    with pytest.raises(StopIteration):
        p.peek()

def test_peekOr_empty():
    p = Pushable( "" )
    assert None is p.peekOr()

def test_peekOr_empty_with_default():
    p = Pushable( "" )
    arbitrary_value = 999
    assert arbitrary_value is p.peekOr(arbitrary_value)

def test_peek_nonempty():
    p = Pushable( "abc" )
    assert "a" == p.peek()

def test_peekOr_nonempty():
    p = Pushable( "abc" )
    assert "a" == p.peek()

def test_peekOr_nonempty_with_default():
    p = Pushable( "abc" )
    assert "a" == p.peekOr(999)

