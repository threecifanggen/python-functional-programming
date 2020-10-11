from functools import reduce

def compose(*args):
    """数学中的compose

    >>> from fppy.base import compose
    >>> compose(lambda x: x+1, lambda x: x**2)(1)
    >>> 4

    """
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
        """执行函数
        """
        return self.f(*args, **kargs)
    
    @staticmethod
    def F_(f):
        """函数盒子/修饰器
        """
        return Function(f)

    def and_then(self, g):
        """先执行本身，再执行g
        """
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
