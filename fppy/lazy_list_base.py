"""从头开始实现的惰性列表
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic
from .gt import S, T
from .cons_list import ConsList, Cons, Empty

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


@dataclass
class LazyEmpty(LazyConsList, Generic[S]):
    """空的惰性列表
    """
    def map(self, _: Callable[[S], T]) -> LazyEmpty[S]:
        """空惰性列表的map
        """
        return self

    def collect(self) -> LazyEmpty[S]: # plint: disable:no-self-use
        """空惰性列表的collect
        """
        return Empty()

    def filter(self, _: Callable[[S], bool]) -> LazyEmpty[S]:
        """空惰性列表的filter
        """
        return self


@dataclass
class LazyStop(LazyConsList, Generic[S]):
    """用来设定过滤点的工具
    """


@dataclass
class LazyCons(LazyConsList, Generic[S]):
    """LazyCons
    """
    head: Callable[[], S]
    tail: Callable[[], LazyConsList[S]]

    def __init__(
        self,
        head: S | Callable[[], S],
        tail: LazyConsList | Callable[[], LazyConsList[S]]
        ):
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
        """惰性列表创建函数
        """
        if len(args) == 0:
            return LazyEmpty()
        else:
            return LazyCons(args[0], cls.maker(*args[1:]))

    @classmethod
    def from_iter(cls, start: S) -> Callable[[Callable[[S], S]], LazyCons[S]]:
        """使用递推公式创建惰性列表
        """
        def helper(f: Callable[[S], S]) -> LazyCons[S]:
            return LazyCons(start, lambda: cls.from_iter(f(start))(f))
        return helper

    def map(self, f: Callable[[S], T]) -> LazyConsList[T]:
        """map函数
        """
        return LazyCons(lambda: f(self.head()), lambda : self.tail().map(f))

    def collect(self) -> ConsList[S]:
        """求值
        """
        if self.head() == LazyStop():
            return self.tail().collect()
        else:
            return Cons(self.head(), self.tail().collect())

    def filter(self, f: Callable[[S], bool]) -> LazyConsList[S]:
        """filter
        """
        # if self.head() == LazyStop():
        #     return LazyCons(LazyStop(), lambda : self.tail().filter(f))
        return LazyCons(
            lambda : self.head() if f(self.head()) else LazyStop(),
            lambda : self.tail().filter(f)
        )

    def take(self, n):
        """获取惰性列表前几个元素
        """
        if n == 0:
            return LazyEmpty()
        elif self.head() == LazyStop():
            return LazyCons(lambda: LazyStop(), lambda: self.tail().take(n)) # pylint: disable=unnecessary-lambda
        else:
            return LazyCons(self.head, lambda: self.tail().take(n - 1))
