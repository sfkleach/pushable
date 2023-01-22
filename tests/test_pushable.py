from pushable import *
import pytest

### test __bool__

def test_bool_empty():
    p = Pushable( "" )
    assert not bool(p)   

def test_bool_nonempty():
    p = Pushable( "abc" )
    assert bool(p)

## test __iter__ via list

def test_iter_nonempty():
    p = Pushable( "abc" )
    assert ["a", "b", "c"] == list(p)

## test __next__

def test_next_empty():
    p = Pushable( "" )
    with pytest.raises(StopIteration):
        next(p)

### test the peek family

def test_peek_empty():
    p = Pushable( "" )
    with pytest.raises(StopIteration):
        p.peek()

def test_peek_nonempty():
    p = Pushable( "abc" )
    assert "a" == p.peek()

def test_skipPeek_empty():
    p = Pushable( "" )
    with pytest.raises(StopIteration):
        p.skipPeek()

def test_skipPeek_nonempty_enough():
    p = Pushable( "abc" )
    assert "b" == p.skipPeek(skip=1)

def test_skipPeek_nonempty_tooMany():
    p = Pushable( "abc" )
    with pytest.raises(StopIteration):
        p.skipPeek(skip=4)

def test_peekOr_empty():
    p = Pushable( "" )
    assert None is p.peekOr()

def test_peekOr_empty_with_default():
    p = Pushable( "" )
    arbitrary_value = 999
    assert arbitrary_value is p.peekOr(arbitrary_value)

def test_peekOr_nonempty():
    p = Pushable( "abc" )
    assert "a" == p.peek()

def test_peekOr_nonempty_with_default():
    p = Pushable( "abc" )
    assert "a" == p.peekOr(999)

def test_multiPeek_empty():
    p = Pushable( "" )
    assert [] == list(p.multiPeek(skip=0, count=0))

def test_multiPeek_nonempty_enough():
    p = Pushable( "abcdef" )
    assert ["b", "c"] == list(p.multiPeek(skip=1, count=2))

def test_multiPeek_nonempty_tooMany():
    p = Pushable( "abcdef" )
    with pytest.raises(RuntimeError):
        tuple(p.multiPeek(skip=5, count=2))

def test_multiPeekOr_empty():
    p = Pushable( "" )
    assert [] == list(p.multiPeekOr(skip=0, count=0))

def test_multiPeekOr_nonempty_enough():
    p = Pushable( "abcdef" )
    assert ["b", "c"] == list(p.multiPeekOr(skip=1, count=2))

def test_multiPeekOr_nonempty_tooMany():
    p = Pushable( "abcdef" )
    assert ("f", None, None) == tuple(p.multiPeekOr(skip=5, count=3))



### test the push family

def test_push_unpeeked():
    p = Pushable( "abc" )
    p.push( *"x" )
    assert ["x", "a", "b", "c" ] == list(p)

def test_push_peeked():
    p = Pushable( "abc" )
    p.peek()
    p.push( *"x" )
    assert ["x", "a", "b", "c" ] == list(p)

def test_multiPush_peeked():
    p = Pushable( "abc" )
    p.peek()
    p.multiPush( *"xy" )
    assert ["x", "y", "a", "b", "c" ] == list(p)

def test_multiPush_skipPeeked():
    p = Pushable( "abc" )
    p.multiPeek(skip=1)
    p.multiPush( *"xy" )
    assert ["x", "y", "a", "b", "c" ] == list(p)



