"""惰性列表
"""
from typing import Iterable
from dataclasses import dataclass
from functools import reduce
from itertools import (
    islice,
    takewhile,
    accumulate,
    repeat,
    chain
)


@dataclass
class Nil:
    """列表结尾
    """

class LazyList:
    """惰性列表
    """
    def __init__(
        self,
        x: Iterable):
        self.iter_ = (i for i in x)

    def split_head(
        self
        ):
        """分割开头
        """
        try:
            x = next(self.iter_)
        except:
            x = Nil()
        return (x, self)

    def map(self, f):
        """map函数
        """
        return lazy_list(map(f, self.iter_))

    def reduce(self, f):
        """reduce函数
        """
        return reduce(f, self.iter_)

    def foldleft(self, f, init):
        """foldleft函数
        """
        return reduce(f, self.iter_, init)

    @staticmethod
    def from_iter(start):
        """按递推公式生成惰性列表函数
        """
        def helper(f):
            return LazyList(accumulate(repeat(start), lambda a, _: f(a)))
        return helper

    def collect(self):
        """collect函数
        """
        return list(self.iter_)

    def scan_left(self, f, init):
        """类似reduce，但将每个结果输出

        Attribute:
            f[Callable]: reduce函数
            init: 设定初始值
        """
        return LazyList(accumulate(chain([init], self.iter_), f))

    def find(self, f):
        """找到第一个符合f的元素
        """
        try:
            x = next(self.iter_)
            if f(x):
                return x
            else:
                return self.find(f)
        except:
            return Nil()

    def filter(self, f):
        """filter函数
        """
        return lazy_list(filter(f, self.iter_))

    def len(self):
        """len函数
        """
        return self.foldleft(lambda x, _: x + 1, 0) 

    def takewhile(self, f):
        """按f为True取数据到
        """
        return lazy_list(takewhile(f, self.iter_))

    def take(self, n):
        """获取前N个数据
        """
        return lazy_list(enumerate(self.iter_))\
            .takewhile(lambda x: x[0] < n)\
            .map(lambda x: x[1])

    def zip_with(self, other):
        """zip函数
        """
        if isinstance(other, LazyList):
            return LazyList(zip(self.iter_, other.iter_))
        elif isinstance(other, Iterable):
            return LazyList(zip(self.iter_, other))
        else:
            raise TypeError(
                "other is not a Iterable object "
                "or LazyList")

    def for_all(self, func):
        """所有值都符合func则返回True
        """
        return self.map(func).reduce(lambda x, y: x and y)

    def __add__(self, other):
        """两个列表添加
        """
        return self.concat(other)

    def concat(self, other):
        """两个列表添加
        """
        if isinstance(other, LazyList):
            return LazyList(chain(self.iter_, other.iter_))
        elif isinstance(other, Iterable):
            return LazyList(chain(self.iter_, other))
        else:
            raise TypeError(
                "other is not a Iterable object "
                "or LazyList")

    def drop(self, n):
        """删除前N个数
        """
        return LazyList(islice(self.iter_, n, None))

    @property
    def last(self):
        """获取最后一个值
        """
        return self.reduce(lambda _, y: y)


def lazy_list(x: Iterable):
    """生成LazyList
    """
    return LazyList(x)
