"""组合子
"""

# pylint: disable=unnecessary-lambda
Y = lambda f: ((lambda g: f(g(g)))(lambda g: f(lambda y: g(g)(y))))
Y.__doc__ = "Y组合子"

# pylint: disable=unnecessary-lambda
Z = lambda f: (lambda g: f(g(g)))(lambda g: f(lambda *y: g(g)(*y)))
Z.__doc__ = "Z组合子"
