from types import new_class
from typing import Callable, Generic
from .gt import S, T

ListBase = new_class("ListBase", (Generic[T], ), dict())

def cons(head: S, tail: S) -> ListBase[S]:
    """基于二元元组实现的List

    Args:
        head ([type]): [description]
        tail ([type]): [description]
    """
    def helper():
        return (head, tail)
    return helper
    
head: Callable[[ListBase[S]], S] = lambda cons_list: cons_list()[0]
tail: Callable[[ListBase[S]], S] = lambda cons_list: cons_list()[1]

def print_cons_with_brackets(cons_list: ListBase[S]) -> str:
    """打印ListBase的括号风格结果

    Args:
        cons_list (ListBase[S]): 需要打印的内容

    Returns:
        str: 返回可以打印的结果，用括号风格
    """
    if cons_list == ():
        return "()"
    else:
        return f"({head(cons_list)}, {print_cons_with_brackets(tail(cons_list))})"

def print_cons(cons_list: ListBase[S]) -> str:
    """打印ListBasr的逗点风格结果

    Args:
        cons_list (ListBase[S]): 需要打印的内容

    Returns:
        str: [description]
    """
    if cons_list == ():
        return "nil"
    else:
        return f"{head(cons_list)}, {print_cons(tail(cons_list))}"

def map_cons(f: Callable[[S], T], cons_list: ListBase[S]) -> ListBase[T]:
    """ListBase的map运算

    Args:
        f (ListBase[S]): 需要map的函数
        cons_list (ListBase[S]): 待处理的结果

    Returns:
        ListBase[T]: 结果
    """
    if cons_list == ():
        return ()
    else:
        return cons(f(head(cons_list)), map_cons(f, tail(cons_list)))

def filter_cons(f: Callable[[S], bool], cons_list: ListBase[S]) -> ListBase[S]:
    """ListBase的filter运算

    Args:
        f (Callable[[S], bool]): filter函数
        cons_list (ListBase[S]): 待处理的结果

    Returns:
        ListBase[S]: 结果
    """
    if cons_list == ():
        return ()
    else:
        hd, tl = head(cons_list), tail(cons_list)
        if f(hd):
            return cons(hd, filter_cons(f, tl))
        else:
            return tl

def fold_left_cons(f: Callable[[T, S], T], init: T, cons_list: ListBase[S]) -> ListBase[T]:
    """ListBase的fold_left函数

    Args:
        f (Callable[[T, S], T]): 二元函数
        cons_list (ListBase[S]): 待处理的list
        init (T): 初始值

    Returns:
        ListBase[T]: 结果
    """
    if cons_list == ():
        return init
    else:
        return fold_left_cons(f, f(init, head(cons_list)), tail(cons_list))

    
map_cons_curry = lambda f: lambda cons_list: map_cons(f, cons_list)
map_cons_curry.__doc__="""科里化版本的map_cons"""
filter_cons_curry = lambda f: lambda cons_list: filter_cons(f, cons_list)
filter_cons_curry.__doc__="""科里化版本的filter_cons"""
fold_left_cons_curry = lambda f: lambda init: lambda cons_list: fold_left_cons(f, init, cons_list)
fold_left_cons_curry.__doc__="""科里化版本的fold_left_cons"""
