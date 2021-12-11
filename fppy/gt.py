'''
Author: huangbaochen<huangbaochenwo@live.com>
Date: 2021-12-11 15:00:48
LastEditTime: 2021-12-11 21:23:16
LastEditors: huangbaochen<huangbaochenwo@live.com>
Description: 基本类型
No MERCY
'''
from typing import Generic, TypeVar

S0 = TypeVar("S0")
S = TypeVar("S")
T = TypeVar("T")
T1 = TypeVar("T1")
U = TypeVar("U")

class GenericTypeVar(Generic[S]):
    """泛型类

    方便直接定义值的类型
    """
