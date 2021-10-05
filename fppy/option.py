from __future__ import annotations

from abc import ABCMeta, abstractmethod, ABC
from enum import Enum, unique
from typing import Any, Callable, Dict, Optional, TypeVar, Union

S = TypeVar("S")
T = TypeVar("T")

@unique
class EitherBranch(Enum):
    left = 1
    right = 2

EB = EitherBranch

class Option(ABC):

    @abstractmethod
    def map(self, f):
        pass

    @abstractmethod
    def flatmap(self, f):
        pass

    @abstractmethod
    def error_map(self, f):
        pass

class ONone(Option):

    def map(self, f):
        return ONone()

    def flatmap(self, f):
        return ONone()

    def __repr__(self) -> str:
        return "None"

    def error_map(self, f):
        return ONone()


class OSome(Option):
    def __init__(
            self,
            value: S
        ):
        self.value = value

    def map(self, f: Callable[[S], T]) -> OSome[T]:
        return OSome(f(self.value))

    def error_map(self, f: Callable[[S], T]) -> OSome[T]:
        try:
            return OSome(f(self.value))
        except:
            return ONone()

    def flatmap(self, f: Callable[[S], Option[T]]) -> Option[T]:
        return f(self.value)

    def __repr__(self) -> str:
        return f"Some({self.value})"

    def get(self) -> S:
        return self.value


class Either(ABC):

    @abstractmethod
    def map(self, branch: EB):
        pass

    @abstractmethod
    def flatmap(self, branch: EB):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def error_map(self, f, error_handle):
        pass

class Left(Either):
    def __init__(
            self,
            value,
            main_branch: EB = EB.right
        ):
        self.value = value
        self.main_branch = main_branch
    
    def map(self, branch: EB):
        def helper(f: Callable[[S], T]) -> Union[Right, Left]:
            if branch == EB.left:
                return Left(f(self.value), self.main_branch)
            else:
                return self
        return helper

    
    def error_map(
            self,
            f: Callable[[S], T],
            error_handle: Optional[Callable[[Exception], Any]] = None,
            ):
        try:
            if _EB_DICT[self.main_branch.name] == self.__class__:
                return self.map(self.main_branch)(f)
            else:
                return self
        except Exception as e:
            if error_handle is None:
                return Right(e, self.main_branch)
            else:
                return Right(error_handle(e), self.main_branch)

    def flatmap(self, branch: EB):
        def helper(f: Callable[[S], Union[Left, Right]]) -> Union[Right, Left]:
            if branch == EB.left:
                return f(self.value)
            else:
                return self
        return helper

    def get(self):
        return self.value

    def __repr__(self) -> str:
        return f"Left({self.value})"


class Right(Either):
    def __init__(
            self,
            value: S,
            main_branch: EB = EB.right
        ):
        self.value = value
        self.main_branch = main_branch
    
    def map(self, branch: EB):
        def helper(f: Callable[[S], T]) -> Union[Right, Left]:
            if branch == EB.right:
                return Right(f(self.value), self.main_branch)
            else:
                return self
        return helper

    def error_map(
            self,
            f: Callable[[S], T],
            error_handle: Optional[Callable[[Exception], Any]] = None,
            ):
        try:
            if _EB_DICT[self.main_branch.name] == self.__class__:
                return self.map(self.main_branch)(f)
            else:
                return self
        except Exception as e:
            if error_handle is None:
                return Left(e, self.main_branch)
            else:
                return Left(error_handle(e), self.main_branch)
    
    def flatmap(self, branch: EB):
        def helper(f: Callable[[S], Union[Left, Right]]) -> Union[Right, Left]:
            if branch == EB.right:
                return f(self.value)
            else:
                return self
        return helper

    def get(self):
        return self.value

    def __repr__(self) -> str:
        return f"Right({self.value})"

_EB_DICT: Dict[str, Either] = {
    "left": Left,
    "right": Right
} 