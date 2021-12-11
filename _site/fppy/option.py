from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic
from fppy.errors import NothingHasNoSuchMethod
from .gt import S, T

@dataclass
class Option:
    """Option类型
    """

@dataclass
class Nothing(Option, Generic[S]):
    """空类型
    """

    def collect(self, pf):
        """计算

        Args:
            pf (PartialFunction): 一个偏函数

        Returns:
            Nothing: 返回空
        """
        return Nothing()

    def get_or_else(self, v: S) -> S:
        """获取数据如果没有返回 `v`

        Args:
            v (S): 默认值

        Returns:
            S: 返回值
        """
        return v

    def filter(self, f: Callable[[S], Option[T]]) -> Option[T]:
        """过滤函数

        Args:
            f (Callable[[S], Option[T]]): 带入过滤条件

        Returns:
            Option[T]: 返回值
        """
        return Nothing()

    @property
    def get(self):
        """直接获取方法

        Raises:
            NothingHasNoSuchMethod: 获取不到任何值的报错
        """
        raise NothingHasNoSuchMethod("Nothing has no get method")

@dataclass
class Just(Option, Generic[S]):
    value: S

    def map(self, f: Callable[[S], T]) -> Option[T]:
        return Just(f(self.value))

    def flat_map(self, f: Callable[[S], Option[T]]) -> Option[T]:
        res = f(self.value)
        if isinstance(res, Option):
            return res
        else:
            raise TypeError("result is not an Option object")

    @property
    def get(self) -> S:
        return self.value

    def collect(self, pf):
        return pf.lift(self.value)

    def get_or_else(self, v: S):
        return self.value

    def filter(self, f: Callable[[S], Option[T]]) -> Option[T]:
        if f(self.value):
            return self
        else:
            return Nothing()