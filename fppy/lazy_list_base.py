from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic
from .gt import S, T
from .cons_list import ConsList, Empty, Cons

class LazyConsList(Generic[S]):
    pass

@dataclass
class LazyEmpty(LazyConsList, Generic[S]):
    def map(self, _: Callable[[S], T]) -> LazyEmpty[S]:
        return self
    
    def collect(self) -> LazyEmpty[S]:
        return self
        
    def filter(self, _: Callable[[S]], T) -> LazyEmpty[S]:
        return self


@dataclass
class LazyStop(LazyConsList, Generic[S]):
    def map(self, _: Callable[[S], T]) -> LazyStop:
        return self

    def collect(self, _: Callable[[S], T]) -> LazyStop[S]:
        return self

    def filter(self, _: Callable[[S], T]) -> LazyStop[S]:
        return self

@dataclass
class LazyCons(LazyConsList, Generic[S]):
    head: Callable[[], S]
    tail: Callable[[], LazyConsList[S]]

    def __init__(self, head: S | Callable[[], S], tail: LazyConsList | Callable[[], LazyConsList[S]]):
        if callable(head):
            self.head = head
        else:
            self.head = lambda : head
        if isinstance(tail, LazyConsList):
            self.tail = lambda: tail
        else:
            self.tail = tail

    @classmethod
    def maker(cls, *args: S) -> LazyConsList:
        if len(args) == 0:
            return LazyEmpty()
        else:
            return LazyCons(args[0], cls.maker(*args[1:]))

    @classmethod
    def from_iter(cls, start: S):
        def helper(f: Callable[[S], S]):
            return LazyCons(start, lambda: cls.from_iter(f(start))(f))
        return helper

    def map(self, f: Callable[[S], T]) -> LazyConsList[T]:
        return LazyCons(lambda: f(self.head()), lambda : self.tail().map(f))
    
    def collect(self) -> ConsList[S]:
        if self == LazyEmpty():
            return Empty()
        else:
            if self.head() == LazyStop():
                return self.tail().collect()
            else:
                return Cons(self.head(), self.tail().collect())

    def filter(self, f: Callable[[S], T]):
            if self.head() == LazyStop():
                return LazyCons(LazyStop(), lambda : self.tail().filter(f))
            return LazyCons(
                lambda : self.head() if f(self.head()) else LazyStop(),
                lambda : self.tail().filter(f)
            )

    def take(self, n):
        if n == 0:
            return LazyEmpty()
        if self.head == LazyStop():
            return lambda: self.tail().take(n)
        else:
            return LazyCons(self.head, lambda: self.tail().take(n - 1))
