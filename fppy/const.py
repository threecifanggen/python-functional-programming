from .errors import ConstError

class _const:
     def __setattr__(self, name, value):
         if name in self.__dict__:
            raise ConstError(f"Can't rebind const {name} with {value}")
         else:
             self.__dict__[name] = value

import sys
sys.modules[__name__] = _const()