"""用二元元组实现的列表
"""
from typing import Callable, Tuple
from .gt import S, T, GenericTypeVar


ListBase = GenericTypeVar[S]
EmptyListBase = Tuple[()]
ConsListBase = Callable[[], Tuple[S, ListBase[S]]]

empty_list_base = ()

def cons(head: S, tail: ListBase[S]) -> ConsListBase[S]:
    """基于二元元组实现的List

    Args:
        head (S): 头部元素
        tail (ListBase[S]): 尾部元素
    """
    def helper():
        return (head, tail)
    return helper

def cons_apply(*args: S) -> ConsListBase[S]:
    """一个方便的定义方式

    Returns:
        ConsListBase[S]: 返回结果
    """
    if len(args) == 0:
        return empty_list_base
    else:
        return cons(args[0], cons_apply(*args[1:]))


head: Callable[[ConsListBase[S]], S] = lambda cons_list: cons_list()[0]
head.__doc__ == """获取List第一个元素""" # pylint: disable=pointless-statement

tail: Callable[[ConsListBase[S]], S] = lambda cons_list: cons_list()[1]
tail.__doc__ == """截取第一个元素后的List"""  # pylint: disable=pointless-statement

def equal_cons(this: ListBase[S], that: ListBase[S]) -> bool:
    """判断两个list是否相等

    Args:
        this (ListBase[S]): 第一个list
        that (ListBase[S]): 第二个list

    Returns:
        bool: 返回第二个相等
    """
    if this == empty_list_base and that != empty_list_base:
        return False
    elif this != empty_list_base and that == empty_list_base:
        return False
    elif this == empty_list_base and that == empty_list_base:
        return True
    else:
        return head(this) == head(that) and equal_cons(tail(this), tail(that))

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
        return (
            f"({head(cons_list)}, "
            f"{print_cons_with_brackets(tail(cons_list))})"
        )

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
        return empty_list_base
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
        return empty_list_base
    else:
        hd, tl = head(cons_list), tail(cons_list)
        if f(hd):
            return cons(hd, filter_cons(f, tl))
        else:
            return filter_cons(f, tl)

def fold_left_cons(
    f: Callable[[T, S], T],
    init: T, cons_list: ListBase[S]
    ) -> ListBase[T]:
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
fold_left_cons_curry = lambda f: (
    lambda init: lambda cons_list: fold_left_cons(f, init, cons_list)
)
fold_left_cons_curry.__doc__="""科里化版本的fold_left_cons"""
