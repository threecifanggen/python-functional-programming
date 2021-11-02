"""Either类型
"""
from __future__ import annotations
from typing import Callable, Generic, NoReturn
from dataclasses import dataclass
from .gt import S, T, T1
from .option import Just

@dataclass
class _Either(Generic[S, T]):
    value: S


@dataclass
class Right(_Either, Generic[S, T]):
    value: T

    @classmethod
    def unapply(right: Right[S, T]) -> Just[T]:
        pass

    def contains(self, x: T) -> bool:
        pass

    def filter_or_else(
        self,
        f: Callable[[T], bool],
        x: T
        ) -> Right[S, T]:
        pass

    def flat_map(
        self,
        f: Callable[[T], _Either[S, T]]
        ) -> _Either[S, T]:
        pass

    def map(
        self,
        f: Callable[[T], T1]
        ) -> Right[S, T1]:
        pass

    @property
    def is_left():
        return False
    
    @property
    def is_right():
        return True

    def for_each(
        self,
        f: Callable[[T], NoReturn]
        ) -> Right[S, T]:
        pass

    def for_all(
        self,
        f: Callable[[T], bool]
        ) -> bool:
        True

    def or_else(
        self,
        x: _Either[S, T]
        ) -> _Either[S, T]:
        pass

    def get_or_else(
        self,
        x: T
        ) -> T:
        pass


@dataclass
class Left(_Either, Generic[S, T]):
    value: S
 
    @classmethod
    def unapply(right: Right[S, T]) -> Just[T]:
        pass

    def contains(self, x: S) -> bool:
        pass

    def filter_or_else(
        self,
        f: Callable[[T], bool],
        x: T
        ) -> Right[S, T]:
        pass

    def flat_map(
        self,
        f: Callable[[T], _Either[S, T]]
        ) -> _Either[S, T]:
        pass

    def map(
        self,
        f: Callable[[T], T1]
        ) -> Left[S, T1]:
        pass

    @property
    def is_left():
        return True
    
    @property
    def is_right():
        return False

    def for_each(
        self,
        f: Callable[[T], NoReturn]
        ) -> Left[S, T]:
        pass

    def for_all(
        self,
        _: Callable[[T], bool]
        ) -> bool:
        return True

    def or_else(
        self,
        x: _Either[S, T]
        ) -> _Either[S, T]:
        pass

    def get_or_else(
        self,
        x: T
        ) -> T:
        pass
    

class Either(_Either, Generic[S, T]):
    value: T

    def __new__(self, value):
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
