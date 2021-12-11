from dataclasses import dataclass
from typing import Generic, List
from .gt import S, T

@dataclass
class Try(Generic[S]):
    value: None | S = None
    state_list: List = []
    
    def of(self, value):
        return ()