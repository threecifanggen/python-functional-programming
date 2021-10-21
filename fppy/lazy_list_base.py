"""从头开始实现的惰性列表
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic
from .gt import S, T
from .cons_list import ConsList, Cons

class LazyConsList(Generic[S]):
    """从头实现的惰性列表

    新建列表：

    >>> from fppy.lazy_list_base import LazyCons, LazyEmpty
    >>> LazyCons(1, LazyCons(2, LazyCons(3, LazyEmpt())))
    >>> LazyCons.maker(1, 2, 3) # 与上面的方法结果相同

    通过递推公式生成无穷列表：

    >>> LazyCons.from_iter(1)(lambda x: x + 1) # 生成正整数
    >>> LazyCons.from_iter(1)(lambda _: 1) # 生成无穷的1

    获取前10的元素，包括（无穷列表）：

    >>> LazyCons.from_iter(1)(lambda _: 1).take(10)

    其他方法包括： `map` ， `filter` ， `fold_left`
    """
    pass

@dataclass
class LazyEmpty(LazyConsList, Generic[S]):
    def map(self, _: Callable[[S], T]) -> LazyEmpty[S]:
        return self
    
    def collect(self) -> LazyEmpty[S]:
        return self
        
    def filter(self, _: Callable[[S], bool]) -> LazyEmpty[S]:
        return self


@dataclass
class LazyStop(LazyConsList, Generic[S]):
    pass


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
        if self.head() == LazyStop():
            return self.tail().collect()
        else:
            return Cons(self.head(), self.tail().collect())

    def filter(self, f: Callable[[S], bool]) -> LazyConsList[S]:
        # if self.head() == LazyStop():
        #     return LazyCons(LazyStop(), lambda : self.tail().filter(f))
        return LazyCons(
            lambda : self.head() if f(self.head()) else LazyStop(),
            lambda : self.tail().filter(f)
        )

    def take(self, n):
        if n == 0:
            return LazyEmpty()
        elif self.head() == LazyStop():
            return LazyCons(lambda: LazyStop(), lambda: self.tail().take(n))
        else:
            return LazyCons(self.head, lambda: self.tail().take(n - 1))
