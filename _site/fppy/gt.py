from typing import Generic, TypeVar

S0 = TypeVar("S0")
S = TypeVar("S")
T = TypeVar("T")
T1 = TypeVar("T1")

class GenericTypeVar(Generic[S]):
    """泛型类

    方便直接定义值的类型
    """
