"""Either类型
"""
from __future__ import annotations
from abc import ABC
from typing import Callable, Generic, NoReturn
from dataclasses import dataclass
from .gt import S, T, T1
from .option import Just

@dataclass
class _Either(ABC, Generic[S, T]):
    """Either的Base
    """
    value: S


@dataclass
class Right(_Either, Generic[S, T]):
    """Right类
    """
    value: T

    @classmethod
    def unapply(cls, right: Right[S, T]) -> Just[T]:
        """uapply
        """
        if isinstance(right, Right):
            return Just(right.value)
        else:
            raise TypeError("Right.unapply's parameter "
            "must be an instance of Right")

    def contains(self, x: T) -> bool:
        """判断是否含有数据
        """
        return self.value == x

    def exists(
        self,
        f: Callable[[T], bool]) -> bool:
        """判断是否存在符合f的元素
        """
        return f(self.value)

    def filter_or_else(
        self,
        f: Callable[[T], bool],
        x: S
        ) -> _Either[S, T]:
        """过滤
        """
        if f(self.value):
            return self
        else:
            return Left(x)

    def flat_map(
        self,
        f: Callable[[T], _Either[S, T]]
        ) -> _Either[S, T]:
        """flat_map
        """
        res = f(self.value)
        if isinstance(res, _Either):
            return res
        else:
            raise TypeError(
                "f must return an Either Object"
            )

    def map(
        self,
        f: Callable[[T], T1]
        ) -> Right[S, T1]:
        """map
        """
        return Right(f(self.value))

    @property
    def is_left(self):
        """判断是否是left
        """
        return False

    @property
    def is_right(self):
        """判断是否是right
        """
        return True

    def for_each(
        self,
        f: Callable[[T], NoReturn]
        ) -> Right[S, T]:
        """运行副作用
        """
        f(self.value)
        return self

    def for_all(
        self,
        f: Callable[[T], bool]
        ) -> bool:
        """判断是否符合f
        """
        if f(self.value):
            return True
        else:
            return False

    def or_else(
        self,
        _: _Either[S, T]
        ) -> _Either[S, T]:
        """获取值
        """
        return self

    def get_or_else(
        self,
        _: T
        ) -> T:
        """获取值
        """
        return self.value


@dataclass
class Left(_Either, Generic[S, T]):
    """Left对象
    """
    value: S

    @classmethod
    def unapply(cls, left: Right[S, T]) -> Just[T]:
        """unapply
        """
        if isinstance(left, Left):
            return Just(left.value)
        else:
            raise TypeError("Left.unapply's parameter "
            "must be an instance of Left")

    def contains(self, x: S) -> bool:
        """判断是否含有数据
        """
        return self.value == x

    def exists(
        self,
        _: Callable[[T], bool]) -> bool:
        """判断是否存在符合f的元素
        """
        return False

    def filter_or_else(
        self,
        _: Callable[[T], bool],
        __: S
        ) -> Left[S, T]:
        """过滤
        """
        return self

    def flat_map(
        self,
        _: Callable[[T], _Either[S, T]]
        ) -> _Either[S, T]:
        """flat_map
        """
        return self

    def map(
        self,
        _: Callable[[T], T1]
        ) -> Left[S, T1]:
        """map
        """
        return self

    @property
    def is_left(self):
        """判断是否是left
        """
        return True

    @property
    def is_right(self):
        """判断是否是Right
        """
        return False

    def for_each(
        self,
        _: Callable[[T], NoReturn]
        ) -> Left[S, T]:
        """运行副作用
        """
        return self

    def for_all(
        self,
        _: Callable[[T], bool]
        ) -> bool:
        """判断是否成立
        """
        return True

    def or_else(
        self,
        x: _Either[S, T]
        ) -> _Either[S, T]:
        """获取值
        """
        return x

    def get_or_else(
        self,
        x: T
        ) -> T:
        """获取值
        """
        return x


class Either(_Either, Generic[S, T]):
    """Either的同名对象
    """
    value: T

    def __new__(cls, value):
        """新建
        """
        return Right(value)

    def apply(self, value) -> Right[S, T]:
        """应用
        """
        return Right(value)

    @classmethod
    def cond(
        cls,
        cond_if: bool,
        right_res: T,
        left_res: S
        ) -> _Either[S, T]:
        """判断如果是返回Right否则返回Left
        """
        if cond_if:
            return Right(right_res)
        else:
            return Left(left_res)
