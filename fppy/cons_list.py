from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic

from _pytest.mark.structures import EMPTY_PARAMETERSET_OPTION
from .gt import S, T

@dataclass
class LazyVal(Generic[S]):
    val: S

    @property
    def get(self):
        return self.val

class ConsList(Generic[S]):
    pass

@dataclass
class Empty(ConsList, Generic[S]):
    def map(self, _: Callable[[S], T]) -> Empty:
        return Empty()

    def filter(self, _: Callable[[S], T]) -> Empty:
        return Empty()
    
    def fold_left(self, _: Callable[[S], T], init: S) -> Empty:
        return init

@dataclass
class Cons(ConsList, Generic[S]):
    head: S
    tail: S

    @classmethod
    def maker(cls, *args: S) -> ConsList[S]:
        if len(args) == 0:
            return Empty()
        else:
            return Cons(args[0], cls.maker(*args[1:]))

    def map(self, f: Callable[[S], T]) -> ConsList[T]:
        return Cons(f(self.head), self.tail.map(f))

    def filter(self, f: Callable[[S], bool]) -> ConsList[S]:
        if f(self.head):
            return Cons(self.head, self.tail.filter(f))
        else:
            return self.tail.filter(f)
            
    def fold_left(self, f: Callable[[S, T], S], init: S) -> S:
            return self.tail.fold_left(f, f(init, self.head))

class LazyConsList(Generic[S]):
    pass

@dataclass
class LazyEmpty(LazyConsList, Generic[S]):
    def map(self, f):
        return self
    
    def collect(self):
        return self
        
    def filter(self, f):
        return self


@dataclass
class LazyStop(LazyConsList, Generic[S]):
    def map(self, f):
        return self

    def collect(self):
        return self

    def filter(self, f):
        return self

@dataclass
class LazyCons(LazyConsList, Generic[S]):
    head: Callable[[], S]
    tail: Callable[[], S]

    def __init__(self, head: S | LazyVal[S], tail: LazyConsList):
        if isinstance(head, LazyVal):
            if head.is_cal:
                self.head = head.get
            else:
                self.head = lambda: head.get
        else:
            self.head =  lambda: head
        self.tail = tail

    def map(self, f: Callable[[S], T]) -> LazyConsList[T]:
        return LazyCons(LazyVal(lambda: f(self.head())), self.tail.map(f))
    
    def collect(self):
        if self == LazyEmpty():
            return Empty()
        else:
            if self.head == LazyStop():
                return self.tail.collect()
            else:
                return Cons(self.head(), self.tail.collect())

    def filter(self, f: Callable[[S], T]):
            return LazyCons(
                LazyVal(lambda: self.head() if f(self.head()) else LazyStop()),
                self.tail.filter(f)
            )

    def take(self, n):
        if n == 0:
            return LazyEmpty()
        if self.head == LazyStop():
            return self.tail.take(n)
        else:
            return LazyCons(LazyVal(self.head), self.tail.take(n - 1))



