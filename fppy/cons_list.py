from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic
from .gt import S, T


class ConsList(Generic[S]):
    """类实现的列表

    如何新建：

    >>> Cons.maker(1, 2, 3, 4)

    列表操作：

    >>> Cons.maker(1, 2, 3, 4)\\
    >>>     .map(lambda x: x + 1)\\
    >>>     .filter(lambda x: x % 2 == 0)\\
    >>>     .fold_left(lambda x, y: x + y, 0) # 返回6
    """
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

