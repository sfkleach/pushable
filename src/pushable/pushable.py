from collections import deque
from typing import Iterator, Any;

class Pushable:
    """
    Wraps an iterator so that it supports peeking and pushing, much like
    a LIFO queue (aka stack). Another way of looking at it is a lazy queue
    that supports pushbacks.

    This is focussed on the use-case of providing modest look-ahead capabilities 
    on a stream of tokens. 
    """

    def __init__(self, iter:Iterator[Any]):
        self.source: Iterator[Any] = iter
        self.stored = deque()

    def __iter__(self):
        """Returns itself, like any other iterator"""
        return self

    def __bool__(self):
        """
        Use this to test if the iterator is exhaused. Returns True if another 
        item is available, otherwise False.
        """
        if self.stored:
            return True
        try:
            self.stored.append(next(self.source))
        except StopIteration:
            return False
        return True

    def len_at_least( self, N:int ):
        """Is there at least N items in the queue, without changing the queue"""
        if len(self._stored) >= N:
            return True
        self.peekOr( skip=N )
        return len(self._stored) >= N

    def push(self, *values):
        """
        Pushes one or more items onto the queue in order, so that the last item
        becomes the new head of the queue.
        """
        self.stored.extend(values)

    def peek(self):
        """
        Gets an item from the head of the queue without affecting the
        queue. There must be at least one item or StopIteration is raised.
        """
        if self.stored:
            return self.stored[-1]
        value = next(self.source)
        self.stored.append(value)
        return value


    def skipPeek(self, skip:int=0):
        """
        Gets an item from the head of the queue without affecting the
        queue, optionally skipping the first N items. There must be at least
        N+1 items or StopIteration will be raised, although the queue will be
        unaffected.
        """
        while len(self._stored) <= skip:
            value = next(self.source)
            self._stored.appendleft(value)
        return self.stored[-1-skip]

    def multiPeek( self, skip:int=0, count:int=1):
        total = skip + count
        while len(self._stored) <= total:
            value = next(self.source)
            self._stored.appendleft(value)
        for i in range( 0, count ):
            yield self._stored[-1-skip-i]

    def peekOr(self, default=None):
        if self.stored:
            return self.stored[-1]
        try:
            value = next(self.source)
            self.stored.append(value)
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
                value = next(self.source)
                self._stored.appendleft(value)
            return self.stored[-1-skip]
        except StopIteration:
            return default

    def multiPeekOr(self, default=None, skip:int=0, count:int=1) -> Iterator[Any]:
        try:
            while len(self._stored) <= skip:
                value = next(self.source)
                self._stored.appendleft(value)
            for i in range( 0, count ):
                yield self._stored[-1-skip-i]
        except StopIteration:
            for i in range( 0, len( self._stored ) ):
                yield self._stored[-1-skip-i]
            for i in range( 0, count - len( self._stored ) ):
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
        for _ in range( 0, skip ):
            self.__next__()
        for i in range( 0, count ):
            yield self.__next__()        

    def popOr( self, default=None ):
        """
        Gets an item from the head of the queue, removing it from the
        queues. If there is less than 1 item, return the supplied default value
        instead.
        """
        if self.stored:
            return self.stored.pop()
        try:
            return next(self.source)        
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

    def multiPopOr(self, skip:int=0, count:int=1) -> Iterator[Any]:
        yields_remaining = count
        try:
            for _ in range( 0, skip ):
                self.__next__()
            for _ in range( 0, count ):
                yield self.__next__()
                yields_remaining -= 1
        except StopIteration:
            for i in range( 0, yields_remaining ):
                yield self.__next__()

    def __next__(self):
        """
        Get the next item if one is available, removing it from the list.
        Otherwise raises StopException.
        """
        if self.stored:
            return self.stored.pop()
        return next(self.source)
