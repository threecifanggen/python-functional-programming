from typing import Generic, TypeVar

S0 = TypeVar("S0")
S = TypeVar("S")
T = TypeVar("T")
T1 = TypeVar("T1")

class GenericTypeVar(Generic[S]):
    pass