"""Either类型
"""
from __future__ import annotations
from typing import Callable, Generic
from dataclasses import dataclass
from .gt import S, T
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
        cond_if: bool,
        right_res: Callable[[], T],
        left_res: Callable[[], S]
        ) -> _Either[S, T]:
        pass
