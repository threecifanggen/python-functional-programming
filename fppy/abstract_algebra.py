from __future__ import annotations
from abc import ABCMeta, abstractmethod, ABC
from functools import reduce
from pathos.multiprocessing import ProcessingPool
from pathos.threading import ThreadPool

class SemiGroup(ABC):
    @staticmethod
    @abstractmethod
    def join(x, y):
        pass

class Monoid(SemiGroup):
    @staticmethod
    @abstractmethod
    def unit():
        pass

    @staticmethod
    def thread_reduce(m: Monoid, n: int=4):
        f = Monoid.mreduce(m)
        def helper(l: list):
            with ThreadPool(n) as p:
                l_split = Monoid.split_list(l, n)
                return f(p.imap(f, l_split))
        return helper

    @staticmethod
    def process_reduce(m: Monoid, n: int=4):
        f = Monoid.mreduce(m)
        def helper(l: list):
            with ProcessingPool(n) as p:
                l_split = Monoid.split_list(l, n)
                return f(p.imap(f, l_split))
        return helper

    @abstractmethod
    def mreduce(m: Monoid):
        def helper(l: list):
            return reduce(m.join, l, m.unit())
        return helper
    
    @abstractmethod
    def split_list(l, n):
        k, j = divmod(len(l), n)
        return (l[i * k + min(i, j):(i + 1) * k + min(i + 1, j)] for i in range(n))
class Functor(ABC):
    @staticmethod
    @abstractmethod
    def map(self, f):
        pass

class Monad(Monoid, Functor):
    pass

