from functools import reduce

def compose(*args):
    return reduce(lambda f, g: lambda x: g(f(x)), args)

def and_then(*args):
    return reduce(lambda f, g: lambda x: f(g(x)), args)

class Function:
    def __init__(
            self,
            f
        ):
        self.f = f

    def __call__(
            self,
            *args,
            **kargs
        ):
        return self.f(*args, **kargs)
    
    @staticmethod
    def F_(f):
        return Function(f)

    
    def and_then(self, g):
        temp_g = g.f if isinstance(g, Function) else g
        def helper(*args, **kargs):
            return temp_g(self.f(*args, **kargs))
        return Function(helper)

    def compose(self, g):
        temp_g = g.f if isinstance(g, Function) else g
        def helper(*args, **kargs):
            return self.f(temp_g(*args, **kargs))
        return Function(helper)

    def map(self, l, to_lazy = False):
        if to_lazy:
            return map(self.f, l)
        else:
            return list(map(self.f, l))

F_ = Function.F_
