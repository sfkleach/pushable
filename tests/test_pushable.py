from pushable import *
import pytest

### test __bool__

def test_bool_empty():
    p:Pushable[str] = Pushable( "" )
    assert not bool(p)   

def test_bool_nonempty():
    p:Pushable[str] = Pushable( "abc" )
    assert bool(p)

## test __iter__ via list

def test_iter_empty():
    p:Pushable[str] = Pushable( "" )
    assert [] == list(p)

def test_iter_nonempty():
    p:Pushable[str] = Pushable( "abc" )
    assert ["a", "b", "c"] == list(p)

## test __next__

def test_next_empty():
    p:Pushable[str] = Pushable( "" )
    with pytest.raises(StopIteration):
        next(p)

def test_next_nonempty():
    p:Pushable[str] = Pushable( "x" )
    assert "x" == next(p)

def test_next_after_push():
    p:Pushable[str] = Pushable( "" )
    p.push( "xxx" )
    assert "xxx" == next(p)

### test the peek family

def test_peek_empty():
    p:Pushable[str] = Pushable( "" )
    with pytest.raises(StopIteration):
        p.peek()

def test_peek_nonempty():
    p:Pushable[str] = Pushable( "abc" )
    assert "a" == p.peek()
    assert "a" == p.peek()

def test_skipPeek_empty():
    p:Pushable[str] = Pushable( "" )
    with pytest.raises(StopIteration):
        p.skipPeek()

def test_skipPeek_nonempty_enough():
    p:Pushable[str] = Pushable( "abc" )
    assert "b" == p.skipPeek(skip=1)
    assert "b" == p.skipPeek(skip=1)

def test_skipPeek_nonempty_tooMany():
    p:Pushable[str] = Pushable( "abc" )
    with pytest.raises(StopIteration):
        p.skipPeek(skip=4)

def test_peekOr_empty():
    p:Pushable[str] = Pushable( "" )
    assert None is p.peekOr()
    assert None is p.peekOr()

def test_peekOr_empty_with_default():
    p:Pushable[str] = Pushable( "" )
    arbitrary_value = 999
    assert arbitrary_value is p.peekOr(arbitrary_value)
    assert arbitrary_value is p.peekOr(arbitrary_value)

def test_peekOr_nonempty():
    p:Pushable[str] = Pushable( "abc" )
    assert "a" == p.peek()
    assert "a" == p.peek()

def test_peekOr_nonempty_with_default():
    p:Pushable[str] = Pushable( "abc" )
    assert "a" == p.peekOr(999)
    assert "a" == p.peekOr(999)

def test_multiPeek_empty():
    p:Pushable[str] = Pushable( "" )
    assert [] == list(p.multiPeek(skip=0, count=0))
    assert [] == list(p.multiPeek(skip=0, count=0))

def test_multiPeek_nonempty_enough():
    p:Pushable[str] = Pushable( "abcdef" )
    assert ["b", "c"] == list(p.multiPeek(skip=1, count=2))
    assert ["b", "c"] == list(p.multiPeek(skip=1, count=2))

def test_multiPeek_nonempty_tooMany():
    p:Pushable[str] = Pushable( "abcdef" )
    with pytest.raises(RuntimeError):
        tuple(p.multiPeek(skip=5, count=2))

def test_multiPeekOr_empty():
    p:Pushable[str] = Pushable( "" )
    assert [] == list(p.multiPeekOr(skip=0, count=0))
    assert [] == list(p.multiPeekOr(skip=0, count=0))

def test_multiPeekOr_nonempty_enough():
    p:Pushable[str] = Pushable( "abcdef" )
    assert ["b", "c"] == list(p.multiPeekOr(skip=1, count=2))
    assert ["b", "c"] == list(p.multiPeekOr(skip=1, count=2))

def test_multiPeekOr_nonempty_tooMany():
    p:Pushable[str] = Pushable( "abcdef" )
    assert ("f", None, None) == tuple(p.multiPeekOr(skip=5, count=3))
    assert ("f", None, None) == tuple(p.multiPeekOr(skip=5, count=3))

### test the pop family

def test_pop_empty():
    p:Pushable[str] = Pushable( "" )
    with pytest.raises(StopIteration):
        p.pop()

def test_pop_nonempty():
    p:Pushable[str] = Pushable( "abc" )
    assert "a" == p.pop()
    assert "b" == p.pop()
    assert "c" == p.pop()
    with pytest.raises(StopIteration):
        p.pop()

def test_skipPop_empty():
    p:Pushable[str] = Pushable( "" )
    with pytest.raises(StopIteration):
        p.skipPop()

def test_skipPop_nonempty_enough():
    p:Pushable[str] = Pushable( "abc" )
    assert "b" == p.skipPop(skip=1)
    with pytest.raises(StopIteration):
        p.skipPop(skip=1)
        
def test_skipPop_nonempty_tooMany():
    p:Pushable[str] = Pushable( "abc" )
    with pytest.raises(StopIteration):
        p.skipPop(skip=4)

def test_skipPopOr_empty():
    p:Pushable[str] = Pushable( "" )
    assert 99 == p.skipPopOr(default=99)

def test_skipPopOr_nonempty_enough():
    p:Pushable[str] = Pushable( "abc" )
    assert "b" == p.skipPop(skip=1)
    assert 99 == p.skipPopOr(skip=1, default=99)
        
def test_skipPopOr_nonempty_tooMany():
    p:Pushable[str] = Pushable( "abc" )
    assert None is p.skipPopOr(skip=4)

def test_popOr_empty():
    p:Pushable[str] = Pushable( "" )
    assert None is p.popOr()
    assert None is p.popOr()

def test_popOr_empty_with_default():
    p:Pushable[str] = Pushable( "" )
    arbitrary_value = 999
    assert arbitrary_value is p.popOr(arbitrary_value)
    assert arbitrary_value is p.popOr(arbitrary_value)

def test_popOr_nonempty():
    p:Pushable[str] = Pushable( "abc" )
    assert "a" == p.popOr()
    assert "b" == p.popOr()

def test_popOr_nonempty_with_default():
    p:Pushable[str] = Pushable( "abc" )
    assert "a" == p.popOr(999)
    assert "b" == p.popOr(999)

def test_multiPop_empty():
    p:Pushable[str] = Pushable( "" )
    assert [] == list(p.multiPop(skip=0, count=0))
    assert [] == list(p.multiPop(skip=0, count=0))

def test_multiPop_nonempty_enough():
    p:Pushable[str] = Pushable( "abcdef" )
    assert ["b", "c"] == list(p.multiPop(skip=1, count=2))
    assert ["e", "f"] == list(p.multiPop(skip=1, count=2))

def test_multiPop_nonempty_tooMany():
    p:Pushable[str] = Pushable( "abcdef" )
    with pytest.raises(RuntimeError):
        tuple(p.multiPop(skip=5, count=2))

def test_multiPopOr_empty():
    p:Pushable[str] = Pushable( "" )
    assert [] == list(p.multiPopOr(skip=0, count=0))
    assert [] == list(p.multiPopOr(skip=0, count=0))

def test_multiPopOr_nonempty_enough():
    p:Pushable[str] = Pushable( "abcdef" )
    assert ["b", "c"] == list(p.multiPopOr(skip=1, count=2))
    assert ["e", "f"] == list(p.multiPopOr(skip=1, count=2))

def test_multiPopOr_nonempty_tooMany():
    p:Pushable[str] = Pushable( "abcdef" )
    assert ("f", None, None) == tuple(p.multiPopOr(skip=5, count=3))
    assert (None, None, None) == tuple(p.multiPopOr(skip=5, count=3))

def test_lenAtLeast():
    p:Pushable[str] = Pushable( "abcdef" )
    assert p.lenAtLeast( 3 )
    p.push( 99 )
    assert p.lenAtLeast( 7 )
    assert not p.lenAtLeast( 8 )


### test the push family

def test_push_unpeeked():
    p:Pushable[str] = Pushable( "abc" )
    p.push( *"x" )
    assert ["x", "a", "b", "c" ] == list(p)

def test_push_peeked():
    p:Pushable[str] = Pushable( "abc" )
    p.peek()
    p.push( *"x" )
    assert ["x", "a", "b", "c" ] == list(p)

def test_multiPush_peeked():
    p:Pushable[str] = Pushable( "abc" )
    p.peek()
    p.multiPush( *"xy" )
    assert ["x", "y", "a", "b", "c" ] == list(p)

def test_multiPush_skipPeeked():
    p:Pushable[str] = Pushable( "abc" )
    p.multiPeek(skip=1)
    p.multiPush( *"xy" )
    assert ["x", "y", "a", "b", "c" ] == list(p)



