"""抽象代数模块
"""
from __future__ import annotations
from abc import abstractmethod, ABC
from functools import reduce
from typing import Iterable
from pathos.multiprocessing import ProcessPool
from pathos.abstract_launcher import AbstractWorkerPool
from pathos.threading import ThreadPool

class SemiGroup(ABC):
    """半群
    """
    @abstractmethod
    def join(self, x, y):
        """聚合操作
        """


class Monoid(SemiGroup, ABC):
    """幺半群
    """

    @property
    @abstractmethod
    def unit(self):
        """单位元
        """

    def parrellel_reduce(self, pool: AbstractWorkerPool, n: int=4):
        """并行计算的reduce
        """
        def helper(ls: Iterable):
            f = self.mreduce
            with pool(n) as p:
                l_split = Monoid._split_list(ls, n)
                return f(p.imap(f, l_split))
        return helper

    def thread_reduce(self, ls: Iterable, n: int=4):
        """基于线程的reduce
        """
        f = self.mreduce
        with ThreadPool(n) as p:
            l_split = Monoid._split_list(ls, n)
            return f(p.imap(f, l_split))

    def process_reduce(self, ls: Iterable, n: int=4):
        """进程的reduce

        TODO: 使用 `pathos` 测试失败，需要改进
        """
        f = self.mreduce
        with ProcessPool(n) as p:
            l_split = Monoid._split_list(ls, n)
            return f(p.imap(f, l_split))

    def mreduce(self, ls: Iterable):
        """普通的reduce
        """
        return reduce(self.join, ls, self.unit)

    @classmethod
    def _split_list(cls, l, n):
        """切分列表
        """
        k, j = divmod(len(l), n)
        return (
            l[i * k + min(i, j):(i + 1) * k + min(i + 1, j)]
                for i in range(n)
            )


class Functor(ABC):
    """函子
    """
    @abstractmethod
    def map(self, f):
        """map操作
        """


class Monad(Monoid, Functor, ABC):
    """单子
    """
