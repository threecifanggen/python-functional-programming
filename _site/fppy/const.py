"""常量定义
"""
import sys
from .errors import ConstError

class _const:
    """ `const` 模块是一个项目定义一堆常量的方式。

    Example:
        这个模块允许像常量一样引用：

        >>> from fppy import const
        >>>
        >>> const.a = 1
        >>> const.a
        1
        >>> const.a = 2
        # raise ConstError
    """

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise ConstError(f"Can't rebind const {name} with {value}")
        else:
            self.__dict__[name] = value


sys.modules[__name__] = _const()
