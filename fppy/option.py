from __future__ import annotations
from dataclasses import dataclass
from abc import abstractmethod
from typing import Callable, TypeVar

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
    def getOrElse(self, v):
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
        return Nothing

    def getOrElse(self, v):
        return v

    def filter(self, f: Callable[[S], Option[T]]) -> Option[T]:
        return Nothing

@dataclass
class Just(Option):
    value: S

    def map(self, f: Callable[[S], T]) -> Option[T]:
        return Just(f(self.value))

    def flat_map(self, f: Callable[[S], Option[T]]) -> Option[T]:
        return f(self.value)

    @property
    def get(self):
        return self.value

    def collect(self, pf):
        return pf.lift(self.value)

    def getOrElse(self, v):
        return self.value

    def filter(self, f: Callable[[S], Option[T]]) -> Option[T]:
        if f(self.value):
            return self
        else:
            return Nothing