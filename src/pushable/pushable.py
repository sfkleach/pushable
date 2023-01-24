from collections import deque
from typing import Iterator, Any;

class Pushable( Iterator ):
    """
    Wraps an iterator so that it supports peeking and pushing, much like
    a LIFO queue (aka stack). Another way of looking at it is a lazy queue
    that supports pushbacks.

    This is focussed on the use-case of providing modest look-ahead capabilities 
    on a stream of tokens. 
    """

    def __init__(self, source):
        """Creates a pushable iterator from any iterable."""
        self._source: Iterator[Any] = iter(source)
        self._stored = deque()

    def __iter__(self):
        """Returns itself, like any other iterator."""
        return self

    def __bool__(self):
        """
        Use this to test if the iterator is exhaused. Returns True if another 
        item is available, otherwise False.
        """
        if self._stored:
            return True
        try:
            self._stored.append(next(self._source))
        except StopIteration:
            return False
        return True

    def lenAtLeast( self, N:int ):
        """Are there at least N items in the queue? Does not change the queue."""
        if len(self._stored) >= N:
            return True
        self.skipPeekOr( skip=N )
        return len(self._stored) >= N

    def push(self, value):
        """
        Pushes one item onto the queue, so that it is the new head of the queue.
        """
        self._stored.append(value)

    def multiPush(self, *values):
        """
        Pushes one or more items onto the queue in reverse order, so that the 
        first item becomes the new head of the queue.
        """
        self._stored.extend(reversed(values))

    def peek(self):
        """
        Gets an item from the head of the queue without affecting the
        queue. There must be at least one item or StopIteration is raised.
        """
        if self._stored:
            return self._stored[-1]
        value = next(self._source)
        self._stored.append(value)
        return value

    def skipPeek(self, skip:int=0):
        """
        Gets an item from the head of the queue without affecting the
        queue, optionally skipping the first N items. There must be at least
        N+1 items or StopIteration will be raised, although the queue will be
        unaffected.
        """
        while len(self._stored) <= skip:
            value = next(self._source)
            self._stored.appendleft(value)
        return self._stored[-1-skip]

    def multiPeek( self, skip:int=0, count:int=1):
        """
        Returns zero, one or more items from the front of the queue, as an 
        iterator, optionally skipping the first N items. There must be at least 
        N+count items or a RuntimeError will be raised. The queue will not be 
        affected, although it may be partly instantiated.
        """
        total = skip + count
        while len(self._stored) < total:
            value = next(self._source)
            self._stored.appendleft(value)
        for i in range( 0, count ):
            yield self._stored[-1-skip-i]
    
    def peekOr(self, default=None):
        """
        Gets an item from the head of the queue without affecting the
        queue. If no item is available the default value is returned.
        """
        if self._stored:
            return self._stored[-1]
        try:
            value = next(self._source)
            self._stored.append(value)
            return value        
        except StopIteration:
            return default

    def skipPeekOr(self, default=None, skip:int=0):
        """
        Gets an item from the head of the queue without affecting the
        queue, optionally skipping the first N items. If there are less
        than N+1 items, the default is returned.
        """
        try:
            while len(self._stored) <= skip:
                value = next(self._source)
                self._stored.appendleft(value)
            return self._stored[-1-skip]
        except StopIteration:
            return default

    def multiPeekOr(self, default=None, skip:int=0, count:int=1) -> Iterator[Any]:
        """
        Returns zero, one or more items from the front of the queue as an iterable, optionally
        skipping the first N items. If there are insufficient items in the queue,
        the default value is substituted sufficient to make up the numbers.
        The queue will not be affected, although it will likely be partly 
        instantiated.
        """      
        total = skip + count
        try:
            while len(self._stored) < total:
                value = next(self._source)
                self._stored.appendleft(value)
            for i in range( 0, count ):
                yield self._stored[-1-skip-i]
        except StopIteration:
            yields_remaining = count
            for i in reversed( range( 0, len( self._stored ) - skip ) ):
                yield self._stored[i]
                yields_remaining -= 1
            for _ in range( 0, yields_remaining ):
                yield default     

    def pop(self):
        """
        Gets an item from the head of the queue, removing it from the
        queue. If there are less than 1 item, raise StopIteration. This
        is a synonym for __next__.
        """
        return self.__next__()

    def skipPop(self, skip:int=0):
        """
        Gets an item from the head of the queue, removing it from the
        queue, optionally removing the preceding N items. If there are less
        than N+1 items, raise StopIteration.
        """
        if skip == 0:
            # We specially handle the common case skip==0 for efficiency.
            return self.__next__()
        else:
            for _ in range( 0, skip ):
                self.__next__()
            return self.__next__()

    def multiPop(self, skip:int=0, count:int=1) -> Iterator[Any]:
        """
        Removes and returns zero, one or more items from the front of the queue
        as an iterator, optionally skipping the first N items. There must be at 
        least N+count items or a RuntimeError will be raised.
        """
        for _ in range( 0, skip ):
            self.__next__()
        for i in range( 0, count ):
            yield self.__next__()        


    def popOr( self, default=None ):
        """
        Gets an item from the head of the queue, removing it from the
        queue. If there is less than 1 item, return the supplied default value
        instead.
        """
        if self._stored:
            return self._stored.pop()
        try:
            return next(self._source)        
        except StopIteration:
            return default

    def skipPopOr( self, default=None, skip:int=0 ):
        """
        Gets an item from the head of the queue, removing it from the
        queue, optionally removing the preceding N items. If there are less
        than N+1 items, return the supplied default value.
        """
        try:
            return self.SkipPop(default = default, skip=skip)
        except StopIteration:
            return default

    def multiPopOr(self, default=None, skip:int=0, count:int=1) -> Iterator[Any]:
        """
        Removes and returns zero, one or more items from the front of the queue, optionally
        skipping the first skip+count items. If there are insufficient items
        available then the default value is substututed as many times as needed.
        """
        yields_remaining = count
        try:
            for _ in range( 0, skip ):
                self.__next__()
            for _ in range( 0, count ):
                yield self.__next__()
                yields_remaining -= 1
        except StopIteration:
            for i in range( 0, yields_remaining ):
                yield default

    def __next__(self):
        """
        Get the next item if one is available, removing it from the list.
        Otherwise raises StopException.
        """
        if self._stored:
            return self._stored.pop()
        return next(self._source)
