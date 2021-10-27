from typing import Callable, Tuple
from .gt import S, T, GenericTypeVar

VoidCallable = Callable[[], S]

def lazy_cons(head: VoidCallable[S], tail: VoidCallable[S] | Tuple):
    """基于二元元组的LazyList
    """
    return (head, tail)

def make_lazy_cons(*args: S) -> VoidCallable[S]:
    if len(args) == 0:
        return lambda : ()
    else:
        return lazy_cons(lambda: args[0], lambda: make_lazy_cons(*args[1:]))

head = lambda lls: lls[0]()
tail = lambda lls: lls[1]()

def iterate_lazy_cons(start: S):
    def helper(f: Callable[[S], S]):
        return lazy_cons(
            lambda: start, 
            lambda: iterate_lazy_cons(f(start))(f)
        )
    return helper

def filter_lazy_cons(f: Callable[[S], bool]):
    def helper(lls):
        return lazy_cons(
            lambda : head(lls) if head(lls) != () and f(head(lls)) else (),
            lambda : filter_lazy_cons(f)(tail(lls))
        )
    return helper

def collect_lazy_cons(lls):
    if tail(lls) == ():
        return (head(lls), ())
    elif head(lls) == ():
        return collect_lazy_cons(tail(lls))
    else:
        return (head(lls), collect_lazy_cons(tail(lls)))

def take_lazy_cons(n: int):
    def helper(lls):
        if n == 0:
            return ()
        elif head(lls) == ():
            return take_lazy_cons(n)(tail(lls))
        else:
            return (head(lls), take_lazy_cons(n - 1)(tail(lls)))
    return helper
