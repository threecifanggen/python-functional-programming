from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, TypeVar, Generic

S = TypeVar("S")
T = TypeVar("T")

@dataclass
class LazyVal(Generic[S]):
    val: S

    @property
    def get(self):
        return self.val

class ConsList(Generic[S]):
    pass

@dataclass
class Empty(ConsList):
    pass

@dataclass
class Cons(ConsList, Generic[S]):
    head: S
    tail: S

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
        
    

def map_cons_list(f: Callable[[S], T], cons_list: ConsList[S]) -> ConsList[T]:
    if cons_list == Empty():
        return Empty()
    else:
        return Cons(f(cons_list.head), map_cons_list(f, cons_list.tail))

def filter_cons_list(f: Callable[[S], bool], cons_list: ConsList[S]) -> ConsList[S]:
    if cons_list == Empty():
        return Empty()
    else:
        if f(cons_list.head):
            return Cons(cons_list.head, filter_cons_list(f, cons_list.tail))
        else:
            return filter_cons_list(f, cons_list.tail)
        
def fold_left_cons_list(f: Callable[[S, T], S], cons_list: ConsList[T], init: S) -> S:
    if cons_list.tail == Empty():
        return f(cons_list.head, init)
    elif cons_list == Empty():
        return init
    else:
        return fold_left_cons_list(f, cons_list.tail, f(init, cons_list.head))

def cons_list_maker(*args) -> Cons[S]:
    if len(args) == 0:
        return Empty()
    else:
        return Cons(args[0], cons_list_maker(*args[1:]))
