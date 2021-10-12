from .errors import NotVoidFunctionError

def lazy_property(func):
    attr_name = "_lazy_" + func.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    return _lazy_property

class _LazyValue:

    def __setattr__(self, name, value):
        if not callable(value) or value.__code__.co_argcount > 0:
            raise NotVoidFunctionError("value is not a void function")
        super(_LazyValue, self).__setattr__(name, (value, False))      
        
    def __getattribute__(self, name: str):
        try:
            _func, _have_called = super(_LazyValue, self).__getattribute__(name)
            if _have_called:
                return _func
            else:
                res = _func()
                super(_LazyValue, self).__setattr__(name, (res, True))
                return res
        except:
            raise AttributeError(
                "type object 'Lazy' has no attribute '{}'"
                .format(name)
            )

lazy_val = _LazyValue()
