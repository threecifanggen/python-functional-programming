from __future__ import annotations
from dataclasses import dataclass
from abc import abstractmethod
from typing import Callable, TypeVar
from fppy.errors import NothingHasNoSuchMethod

T = TypeVar('T')
S = TypeVar('S')

@dataclass
class Option:
    
    @abstractmethod
    def map(self, f: Callable[[S], T]) -> Option[T]:
        pass

    @abstractmethod
    def flat_map(self, f: Callable[[S], Option[T]]) -> Option[T]:
        pass
    
    @property
    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def get_or_else(self, v):
        pass

    @abstractmethod
    def collect(self, pf):
        pass

    @abstractmethod
    def filter(self, f: Callable[[S], Option[T]]) -> Option[T]:
        pass

@dataclass
class Nothing(Option):
    
    def collect(self, pf):
        return Nothing()

    def get_or_else(self, v):
        return v

    def filter(self, f: Callable[[S], Option[T]]) -> Option[T]:
        return Nothing()

    @property
    def get(self):
        raise NothingHasNoSuchMethod("Nothin has no get method")

@dataclass
class Just(Option):
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
    def get(self):
        return self.value

    def collect(self, pf):
        return pf.lift(self.value)

    def get_or_else(self, v):
        return self.value

    def filter(self, f: Callable[[S], Option[T]]) -> Option[T]:
        if f(self.value):
            return self
        else:
            return Nothing()