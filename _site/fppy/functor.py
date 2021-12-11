"""函子相关类
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic
from .gt import S, T

class Box:
    """Box类
    """

@dataclass
class BoxValue(Generic[S]):
    """Box值类
    """
    value: S

    def map(self, f: Callable[[S], T]) -> BoxValue[T]:
        """map
        """
        return BoxValue(f(self.value))

    @staticmethod
    def of(value: S) -> BoxValue[S]:
        """定义值
        """
        return BoxValue(value)


@dataclass
class BoxFunction(Generic[S, T], Box):
    """Box函数类
    """
    func: Callable[[S], T]

    def fmap(self, value: S) -> BoxValue[T]:
        """套用函数
        """
        return BoxValue(self.func(value))
