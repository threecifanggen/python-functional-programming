from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic
from .gt import S, T

class Box:
    pass

@dataclass
class BoxValue(Generic[S]):
    value: S

    def map(self, f: Callable[[S], T]) -> BoxValue[T]:
        return Box(f(self.value))

    @staticmethod
    def of(value: S) -> BoxValue[S]:
        return BoxValue(value)


@dataclass
class BoxFunction(Generic[S, T], Box):
    func: Callable[[S], T]

    def fmap(self, value: S) -> BoxValue[T]:
        return BoxValue(self.func(value))
