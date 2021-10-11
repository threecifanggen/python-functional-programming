from __future__ import annotations
from abc import ABCMeta, abstractmethod, ABC
from functools import reduce
from typing import Iterable
from _pytest.python_api import raises
from pathos.multiprocessing import ProcessPool
from pathos.abstract_launcher import AbstractWorkerPool
from pathos.threading import ThreadPool

class SemiGroup(ABC):
    @abstractmethod
    def join(self, x, y):
        pass


class Monoid(SemiGroup):
    @abstractmethod
    def unit(self):
        pass

    def parrellel_reduce(self, pool: AbstractWorkerPool, n: int=4):
        def helper(ls: Iterable):
            f = self.mreduce
            with pool(n) as p:
                l_split = self._split_list(ls, n)
                return f(p.imap(f, l_split))
        return helper

    def thread_reduce(self, ls: Iterable, n: int=4):
        f = self.mreduce
        with ThreadPool(n) as p:
            l_split = self._split_list(ls, n)
            return f(p.imap(f, l_split))

    def process_reduce(self, ls: Iterable, n: int=4):
        f = self.mreduce
        with ProcessPool(n) as p:
            l_split = self._split_list(ls, n)
            return f(p.imap(f, l_split))

    def mreduce(self, ls: Iterable):
        return reduce(self.join, ls, self.unit())
    
    def _split_list(self, l, n):
        k, j = divmod(len(l), n)
        return (l[i * k + min(i, j):(i + 1) * k + min(i + 1, j)] for i in range(n))


class Functor(ABC):
    @abstractmethod
    def map(self, f):
        pass


class Monad(Monoid, Functor):
    pass
