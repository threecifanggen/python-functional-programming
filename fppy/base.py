"""基础函数
"""
from __future__ import annotations
from functools import reduce
from typing import Any, Callable, Generic, Iterable
from .gt import S0, S, T, T1

def I(x: S) -> S:
    """Identity函数

    Args:
        x (S): 任意函数、值、对象、类

    Returns:
        S: 返回本身
    """
    return x


def compose(*args: Callable) -> Callable:
    """数学中的compose

    >>> from fppy.base import compose
    >>> compose(lambda x: x+1, lambda x: x**2)(1)
    >>> 4

    """
    return reduce(lambda f, g: lambda x: f(g(x)), args)


def and_then(*args: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """和compose采用不同的fold方向的函数
    """
    return reduce(lambda f, g: lambda x: g(f(x)), args)

class _Function(Generic[S, T]):
    """加强版函数
    """
    f: Callable[[S], T]

    def __init__(
            self,
            f: Callable[[S], T],
            name: str | None = None
        ):
        self.f = f
        if name is None:
            self.name = f.__name__
        else:
            self.name = name

    def __call__(
            self,
            *args,
            **kargs
        ) -> T:
        """执行函数
        """
        return self.f(*args, **kargs)

    def apply(
            self,
            *args,
            **kargs
        ) -> T:
        """应用函数 = 执行函数
        """
        return self.f(*args, **kargs)

    @staticmethod
    def F_(f: Callable[[S], T]) -> _Function[S, T]:
        """函数盒子/修饰器
        """
        return _Function(f, f.__name__)

    def and_then(
        self, g: Callable[[T], T1] | _Function[T, T1]
        ) -> _Function[S, T1]:
        """先执行本身，再执行g
        """
        temp_g = g.f if isinstance(g, _Function) else g
        def helper(*args, **kargs):
            return temp_g(self.f(*args, **kargs))
        return _Function(helper)

    def compose(
        self,
        g: Callable[[S0], S] | _Function[S0, S]
        ) -> _Function[S0, T]:
        """compose函数
        """
        temp_g = g.f if isinstance(g, _Function) else g
        def helper(*args, **kargs):
            return self.f(temp_g(*args, **kargs))
        return _Function(helper)

    def map(
        self,
        l: Iterable[S],
        to_lazy: bool = False
        ) -> Iterable[T]:
        """map函数
        """
        if to_lazy:
            return map(self.f, l)
        else:
            return list(map(self.f, l))

F_: Callable[[Callable[[S], T]], _Function[S, T]] = _Function.F_

F_.__doc__ = """"函数修饰器。

这是一个增强版的函数修饰器，可以做到和一般函数一样的使用，
但是可以链式地串联其他函数。

>>> from fppy.base import F_
>>> @F_
>>> def f(x):
>>>     return x + 1
>>>
>>> f_composed = f(x).and_then(lambda x: x + 2)
>>> f_composed(1)
3
>>> f_composed = f(x).compose(lambda x: x * 3)
>>> f_composed(2)
7


Methods:
    _Function.apply: 应用
    _Function.compose: 数学上的compose结合函数
    _Function.and_then: compose相反的操作
    _Function.map: 将函数运用到一个可迭代(`Iterable`)的对象上
"""
