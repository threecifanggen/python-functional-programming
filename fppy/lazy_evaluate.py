"""惰性求值
"""
from typing import Callable
from .errors import NotVoidFunctionError
from .gt import S

def lazy_property(func):
    """惰性属性修饰器。

    如我们可以定义下面一个 `Circle` 的类，定义其中
    计算面积的属性为惰性属性

    .. code-block:: python

        @dataclass
        class Circle:
            x: float
            y: float
            r: float

            @lazy_property
            def area(self):
                print("computing")
                return 3.14 * r * r

    调用时结果如下，可以发现仅第一次发生了计算：

    >>> cir = Circle(0, 1, 1)
    >>> cir.area
    computing
    3.14
    >>> cir.area
    3.14
    """
    attr_name = "_lazy_" + func.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    return _lazy_property

class LazyValue:
    """惰性值。

    惰性值使用一个

    Raises:
        NotVoidFunctionError : 如果带入的值不是一个无参数的函数，
            即 `Void -> S` 形式的函数，则报错。
    """

    def __setattr__(self, name: str, value: Callable[[], S]):
        if not callable(value) or value.__code__.co_argcount > 0:
            raise NotVoidFunctionError("value is not a void function")
        super(LazyValue, self).__setattr__(name, (value, False)) # pylint: disable=super-with-arguments

    def __getattribute__(self, name: str):
        try:
            _func, _have_called = super(LazyValue, self).__getattribute__(name) # pylint: disable=super-with-arguments
            if _have_called:
                return _func
            else:
                res = _func()
                super(LazyValue, self).__setattr__(name, (res, True)) # pylint: disable=super-with-arguments
                return res
        except:
            raise AttributeError(
                f"type object 'Lazy' has no attribute '{name}'"
            ) from Exception

lazy_val = LazyValue()
