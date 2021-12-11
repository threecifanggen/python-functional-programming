'''
Author: huangbaochen<huangbaochenwo@live.com>
Date: 2021-12-11 15:00:15
LastEditTime: 2021-12-11 21:28:16
LastEditors: huangbaochen<huangbaochenwo@live.com>
Description: Try单子
No MERCY
'''
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic

from fppy.option import Just, Nothing
from .gt import S, T


class _Try(Generic[S, T]):
    """Try 单子抽象类
    """

@dataclass
class Fail(_Try[S, T]):
    """失败类
    """
    error: Exception
    value: S | None = None

    @classmethod
    def unapply(cls, x: Fail[S, T]) -> Nothing:
        """unapply方法，转为option对象
        """
        if not isinstance(x, Fail):
            raise TypeError(
                'Fail.unapply需使用Fail为参数，实际是',
                f'{type(x)}'
                )
        else:
            return Nothing()

    # pylint: disable=unused-argument
    def map(self, func: Callable[[S], T]) -> Success[S, T] | Fail[S, T]:
        """map方法
        """
        return self

    # pylint: disable=unused-argument
    def flat_map(
        self,
        func: Callable[[S], _Try]) -> _Try:
        """flat_map方法
        """
        return self

    def __eq__(self, __o: object) -> bool:
        """重写等于逻辑
        """
        return (
            self.error.args == __o.error.args
        ) and (
            self.value == __o.value
        )

    def get(self):
        """获取错误类型
        """
        return self.error

    def get_or_else(self, other: S) -> S:
        """获取值
        """
        return other

    def get_error_input(self) -> T:
        """获取报错时的输入
        """
        return self.value

@dataclass
class Success(_Try[S, T]):
    """成功类
    """
    value: S | None = None

    @classmethod
    def unapply(cls, x: Success[S, T]) -> Just:
        """unapply方法，转为option对象
        """
        if not isinstance(x, Success):
            raise TypeError(
                'Success.unapply需使用Success为参数，实际是',
                f'{type(x)}'
            )
        else:
            return Just(x.value)

    def map(self, func: Callable[[S], T]) -> Success[T] | Fail[S]:
        """map方法
        """
        try:
            return Success(func(self.value))
        # pylint: disable=broad-except
        except Exception as e:
            return Fail(e, self.value)

    def flat_map(
        self,
        func: Callable[[S], _Try[S, T]]) -> _Try[S, T]:
        """flat_map方法
        """
        res = func(self.value)
        if not isinstance(res, _Try):
            raise TypeError(
                'flat_map需返回一个Try对象，但实际上返回了',
                f'{type(res)}'
            )
        else:
            return res

    def get(self):
        """获取值
        """
        return self.value

    # pylint: disable=unused-argument
    def get_or_else(self, other: S):
        """获取值
        """
        return self.value

class Try(_Try[S, T]):
    """Try同名类（为了实现apply）
    """
    def __new__(cls, x: S) -> Success[S, T]:
        """应用
        """
        return Success(x)

    @classmethod
    def apply(cls, x: S) -> Success[S, T]:
        """应用
        """
        return Success(x)
