def lazy_cons(head, tail):
    """基于二元元组的LazyList
    """
    return (head, tail)

def make_lazy_cons(*args):
    if len(args) == 0:
        return ()
    else:
        return lazy_cons(lambda: args[0], lambda: make_lazy_cons(*args[1:]))

head = lambda lls: lls[0]() if callable(lls[0]) else lls[0]
tail = lambda lls: lls[1]() if callable(lls[1]) else lls[1]

def iterate_lazy_cons(start):
    """生成LazyList
    """
    def helper(f):
        return lazy_cons(
            lambda: start,
            lambda: iterate_lazy_cons(f(start))(f)
        )
    return helper

def filter_lazy_cons(f):
    def helper(lls):
        if lls == ():
            return ()
        else:
            return lazy_cons(
                lambda : head(lls) if head(lls) != () and f(head(lls)) else (),
                lambda : filter_lazy_cons(f)(tail(lls))
            )
    return helper

def collect_lazy_cons(lls):
    if lls == ():
        return ()
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

def map_lazy_cons(f):
    def helper(lls):
        if lls == ():
            return ()
        elif head(lls) == ():
            return lazy_cons(
                lambda: (),
                lambda: map_lazy_cons(f)(tail(lls))
            )
        else:
            return lazy_cons(
                lambda: f(head(lls)),
                lambda: map_lazy_cons(f)(tail(lls))
            )
    return helper

def fold_left_lazy_cons(f):
    def bring_start(start):
        def helper(lls):
            if lls == ():
                return start
            elif head(lls) == ():
                return fold_left_lazy_cons(f)(start)(tail(lls))
            else:
                return fold_left_lazy_cons(f)(f(start, head(lls)))(tail(lls))
        return helper
    return bring_start
