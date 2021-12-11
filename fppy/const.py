'''
Author: huangbaochen<huangbaochenwo@live.com>
Date: 2021-12-11 15:00:54
LastEditTime: 2021-12-11 21:41:20
LastEditors: huangbaochen<huangbaochenwo@live.com>
Description: 常量
No MERCY
'''
from .errors import ConstError

class Const:
    """ `const` 模块是一个项目定义一堆常量的方式。

    Example:
        这个模块允许像常量一样引用：

        >>> from fppy.const import Const
        >>>
        >>> const = Const()
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
