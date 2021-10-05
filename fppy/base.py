from functools import reduce


def compose(*args):
    """数学中的compose

    >>> from fppy.base import compose
    >>> compose(lambda x: x+1, lambda x: x**2)(1)
    >>> 4

    """
    return reduce(lambda f, g: lambda x: g(f(x)), args)

def and_then(*args):
    """和compose采用不同的fold方向的函数
    """
    return reduce(lambda f, g: lambda x: f(g(x)), args)

class _Function:
    """加强版函数
    
    ## 使用方法
    
    """
    
    def __init__(
            self,
            f,
            name=None
        ):
        self.f = f
        if name is None:
            self.name = f.__name__
        else:
            self.name = name

    def __call__(
            self,
            *args,
            **kargs
        ):
        """执行函数
        """
        return self.f(*args, **kargs)

    def apply(
            self,
            *args,
            **kargs
        ):
        """应用函数 = 执行函数
        """
        return self.f(*args, **kargs)
    
    @staticmethod
    def F_(f):
        """函数盒子/修饰器
        """
        return _Function(f, f.__name__)

    def and_then(self, g):
        """先执行本身，再执行g
        """
        temp_g = g.f if isinstance(g, _Function) else g
        def helper(*args, **kargs):
            return temp_g(self.f(*args, **kargs))
        return _Function(helper)

    def compose(self, g):
        temp_g = g.f if isinstance(g, _Function) else g
        def helper(*args, **kargs):
            return self.f(temp_g(*args, **kargs))
        return _Function(helper)

    def map(self, l, to_lazy = False):
        if to_lazy:
            return map(self.f, l)
        else:
            return list(map(self.f, l))

F_ = _Function.F_
