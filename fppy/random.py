from __future__ import annotations
from dataclasses import dataclass
from abc import abstractmethod
from collections import ABC
from typing import Callable, Tuple, TypeVar
from .lazy_list import LazyList

S = TypeVar("S")
T = TypeVar("T")
Rand = TypeVar("Rand")


class RNG(ABC):

    @abstractmethod
    def next_int(self) -> Tuple[int, RNG]:
        pass

@dataclass
class SimpleRNG(RNG):
    seed: int
    def next_int(self) -> Tuple[int, SimpleRNG]:
        new_seed = (self.seed * 0x5DEECE66D + 0xB) & 0xFFFFFFFFFFFF
        next_RNG = SimpleRNG(new_seed)
        n = int(new_seed >> 16)
        return (n, next_RNG)

def curry_simple_rng(seed: int):
    def helper():
        new_seed = (seed * 0x5DEECE66D + 0xB) & 0xFFFFFFFFFFFF
        next_func= curry_simple_rng(new_seed)
        n = int(new_seed >> 16)
        return (n, next_func)
    return helper

# Rand = GenericAlias(Callable[[RNG], Tuple[S, RNG]], S)

rand_int: Rand[int] = SimpleRNG.next_int


def unit(s: S) -> Rand[S]:
    return lambda rng: (s, rng)

def map(rand: Rand[S], f: Callable[[S], T]):
    def helper(rng: RNG):
        res, rng2 = rand(rng)
        return (f(res), rng2)
    return helper

rand_non_negative_int: Rand[int] = map(rand_int, abs)
rand_non_negative_even: Rand[int] = map(rand_int, lambda x: x - x % 2)
rand_float: Rand[int] = map(rand_int, lambda x: x / 2 ** 32)

def rng_lazy_list(count: int | None = None, seed: int = 1234):
    int_start, rng_start = SimpleRNG(seed=seed).next_int()
    if count is None:
        return LazyList\
            .from_iter((int_start, rng_start))\
                (lambda x: SimpleRNG(x[0]).next_int())\
            .map(lambda x: x[0])
    else:
        return LazyList\
            .from_iter((int_start, rng_start))\
                (lambda x: SimpleRNG(x[0]).next_int())\
            .map(lambda x: x[0])\
            .take(count)

def rand_lazy_list(count: int | None = None, seed: int = 1234):
    start = rand_int(SimpleRNG(seed))
    if count is None:
        return LazyList\
            .from_iter(start)(lambda x: rand_non_negative_int(x[1]))\
            .map(lambda x: x[0])
    else:
        return LazyList\
            .from_iter(start)(lambda x: rand_non_negative_int(x[1]))\
            .map(lambda x: x[0])\
            .take(count)

def curry_random_lazy_list(count: int | None = None, seed: int = 1234):
    start = curry_simple_rng(seed)()
    if count is None:
        return LazyList\
            .from_iter(start)(lambda x: x[1]())\
            .map(lambda x: x[0])
    else:
        return LazyList\
            .from_iter(start)(lambda x: x[1]())\
            .map(lambda x: x[0])\
            .take(count)

