from typing import Iterable
from abc import ABC, abstractmethod
from functools import reduce
from itertools import takewhile


class LList:
    def __init__(
        self,
        x: Iterable,):
        self.iter_ = [i for i in x]

    def map(self, f):
        return LList(f(i) for i in self.iter_)
    
    def collect(self):
        return self.iter_


class Stream:
    def __init__(
        self,
        x: Iterable):
        self.iter_ = (i for i in x)
    
    def map(self, f):
        return stream(map(f, self.iter_))
    
    def reduce(self, f):
        return reduce(f, self.iter_)
    
    def foldleft(self, f, init):
        return reduce(f, self.iter_, init)

    def head(self):
        try:
            x = next(self.iter_)
        except:
            x = None
        return x
    
    def tail(self):
        try:
            x = next(self.iter_)
            return self
        except:
            return None
            
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
            raise
            print(x)
            return None
            
    def filter(self, f):
        return stream(filter(f, self.iter_))

    def len(self):
        return self.foldleft(lambda x, y: x + 1, 0) 
    
    def takewhile(self, f):
        return stream(takewhile(f, self.iter_))

    def take(self, n):
        return stream(enumerate(self.iter_)).takewhile(lambda x: x[0] < n).map(lambda x: x[1])
        
def stream(x: Iterable):
    return Stream(x)


class RawStream(ABC):
    @property
    def is_empty(self):
        pass

    @abstractmethod
    def collect(self):
        pass

    @abstractmethod
    def map(self, f):
        pass

    @abstractmethod
    def filter(self, f):
        pass

    @abstractmethod
    def foldleft(self, f, init):
        pass


class RawEmpty(RawStream):
    is_empty = True

    def collect(self):
        return []

    def map(self, f):
        return RawEmpty()

    def filter(self, f):
        return RawEmpty()

    def foldleft(self, f, init):
        return init
    

class RawCons(RawStream):
    is_empty = False

    def __init__(self,
            head,
            tail
        ):
        self.head = head
        self.tail = tail

    def collect(self):
        return [self.head()] + self.tail.collect()

    def map(self, f):
        return RawCons(lambda: f(self.head()), self.tail.map(f))

    def filter(self, f):
        if f(self.head()):
            return RawCons(self.head, self.tail.filter(f))
        else:
            return self.tail.filter(f)

    def reduce(self, f):
        if isinstance(self.tail, RawEmpty):
            return self.head()
        else:
            return f(self.head(), self.tail.reduce(f))

    def foldleft(self, f, init):
        return self.tail.foldleft(f, f(init, self.head()))

        
def to_stream(x: Iterable):
    if len(x) == 0:
        return RawEmpty()
    else:
        return RawCons(lambda: x[0], to_stream(x[1:]))

def raw_stream(*args):
    return to_stream(args)