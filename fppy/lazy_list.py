from typing import Iterable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import reduce
from itertools import takewhile, accumulate, repeat


@dataclass
class Nil:
    pass

class LazyList:
    def __init__(
        self,
        x: Iterable):
        self.iter_ = (i for i in x)

    def split_head(
        self
        ):
        try:
            x = next(self.iter_)
        except:
            x = Nil()
        return (x, self)
    
    def map(self, f):
        return lazy_list(map(f, self.iter_))
    
    def reduce(self, f):
        return reduce(f, self.iter_)
    
    def foldleft(self, f, init):
        return reduce(f, self.iter_, init)

    @abstractmethod
    def from_iter(start):
        def helper(f):
            return LazyList(accumulate(repeat(start), lambda a, _: f(a)))
        return helper
            
    def collect(self):
        return list(self.iter_)
        
    def find(self, f):
        try:
            x = next(self.iter_)
            if f(x):
                return x
            else:
                return self.find(f)
        except:
            return Nil()
            
    def filter(self, f):
        return lazy_list(filter(f, self.iter_))

    def len(self):
        return self.foldleft(lambda x, _: x + 1, 0) 
    
    def takewhile(self, f):
        return lazy_list(takewhile(f, self.iter_))

    def take(self, n):
        return lazy_list(enumerate(self.iter_)).takewhile(lambda x: x[0] < n).map(lambda x: x[1])
        
def lazy_list(x: Iterable):
    return LazyList(x)
