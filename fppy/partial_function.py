from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, List, Tuple
from .errors import NoOtherCaseError

@dataclass
class _PartialCase:
    case_func: Callable
    case_list: List[Tuple[Callable, Callable]] = field(default_factory=list)

    def then(
            self,
            return_func: Callable
        ):
        return _PartialFunction(
            self.case_list + [(self.case_func, return_func)]
        )
    
@dataclass
class _PartialFunction:
    case_list:  List[Tuple[Callable, Callable]]= field(default_factory=list)
    
    def apply(
            self,
            value
        ):
        if len(self.case_list) == 0:
            raise NoOtherCaseError
        else:
            head = self.case_list[0]
            tail = self.case_list[1:]
            if head[0](value):
                return head[1](value)
            else:
                return _PartialFunction(tail).apply(value)

    def __call__(self, value):
        return self.apply(value)
    
    def is_defined_at(self, value) -> bool:
        """判断是否有定义
        """
        if len(self.case_list) == 0:
            return False
        else:
            head = self.case_list[0]
            tail = self.case_list[1:]
            if head[0](value):
                return True
            else:
                return (
                    _PartialFunction(tail)
                    .is_defined_at(value)
                )

    def case(self, case_func):
        return _PartialCase(
            case_func,
            self.case_list
        )
    
    def or_else(self, other:_PartialFunction):
        return _PartialFunction(
            self.case_list + other.case_list
        )
    
    def lift(self, value):
        from .option import Just, Nothing

        if self.is_defined_at(value):
            return Just(self.__call__(value))
        else:
            return Nothing

class PartialFunction:
    @staticmethod
    def case(case_func):
        return _PartialFunction().case(case_func)