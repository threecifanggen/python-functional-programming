# fppy

开发状态：

![coverage](badge/cov-badge.svg) ![open-issues](https://img.shields.io/github/issues/threecifanggen/python-functional-programming) ![close-issues](https://img.shields.io/github/issues-closed/threecifanggen/python-functional-programming) ![version](https://img.shields.io/github/v/release/threecifanggen/python-functional-programming?include_prereleases)

依赖：

![Python](https://img.shields.io/badge/Python-3.8-green?logo=python) ![Python](https://img.shields.io/badge/pathos-0.2.6-green) ![Python](https://img.shields.io/badge/drill-1.2.0-green)

一个基于`python`的函数式编程类库，仅做学习使用。主要功能如下：

- [x] 常量定义
- [x] 惰性求值/惰性属性
- [ ] 抽象代数
- [x] 常用组合子
- [x] 惰性列表
- [ ] 偏函数
- [ ] 基于性质测试(Property-based Testing)
- [x] 更多功能的函数装饰器
- [x] Option类
- [ ] State类
- [ ] Either类

## 快速功能预览

### 函数修饰器

```python
from fppy.base import F_

@F_
def f(x):
    return x + 1

>>> f(1)
2
>>> f.apply(1)
2
>>> f.and_then(lambda x: x ** 3)(1) # (x + 1) ** 3
8
>>> f.compose(lambda x: x ** 3)(1) # (x ** 3) + 1
1
>>> f.map([1, 2, 3])
[2, 3, 4]
```

### 常量定义

```python
from fppy import const

>>> const.a = 1
>>> const.a
1
>>> const.a = 2
# Error
```

### 惰性列表

一个可以实现`map`、`reduce`等操作的惰性列表

#### 1. 从头定义

```python
from fppy.lazy_list import LazyList

# 定义正整数无穷列表
ll = LazyList.from_iter(2)(lambda x: x + 2)

# 从List对象定义
ll = LazyList([1, 2, 3])

# 从生成器、迭代器定义
x = (i for i in range(100))
ll = LazyList(x)
```

#### 2. map、filter、collect

```python
LazyList([1, 2, 3])\
    .map(lambda x: x + 1)\
    .filter(lambda x: x % 2 == 0)\
    .collect() # 返回[2, 4]
```

#### 3. 其他

其他方法参考文档。

### 常见组合子

#### 1. Y组合子

下面的例子是计算阶乘：

```python
from fppy.combinator import Y

fac = Y(lambd f: lambda x: 1 if (x ==0) else x * f(x - 1))
```

#### 2. Z组合子

下面是计算指数函数的Z组合子实现

```python
from fppy.combinator import Z

power = Z(lambda f: lambda x, n: 1 if (n == 0) else x * f(x, n - 1))
```

### 偏函数

这里的偏函数是指Partial Function，即定义域取不完整的函数；而不是高阶函数中的Partial Applied Function的概念。

定义一个如下函数：

- 如果`x > 0`，则计算`1 / x`
- 如果`x < 0`，则计算`log(-x)`

```python
from math import log
from fppy.partail_function import PartialFunction
# 直接定义
pf = PartialFunction\
    .case(lambda x: x > 0)\
    .then(lambda x: 1 / x)\
    .case(lambda x: x < 0)\
    .then(lambda x: log(-x))

## 计算
pf.apply(1) # 返回1
pf.apply(-1) # 返回0
pf.apply(0) # 返回NoOtherCaseError

## 判断是否在某点有定义
pf.is_defined_at(0.4) # 返回True
pf.is_defined_at(0) # 返回False
```

我们还可以使用`or_else`来组合偏函数，比如上面的函数可以如下实现：

```python
pf_greater_then_0 = PartialFunction\
    .case(lambda x: x > 0)\
    .then(lambda x: 1 / x)

pf_less_then_0 = PartialFunction\
    .case(lambda x: x < 0)\
    .then(lambda x: log(-x)

pf = pf_greater_then_0.or_else(pf_less_then_0)
```

### 惰性求值

#### 1. 惰性属性

```python
from fppy.lazy_evaluate import lazy_property

@dataclass
class Circle:
    x: float
    y: float
    r: float

    @lazy_property
    def area(self):
        print("area compute")
        return self.r ** 2 * 3.14
```

以上定义了一个圆的类，具体获取`area`时，仅第一次会计算（通过打印`"area compute"`显示）。

#### 2. 惰性值

`Python`没有代码块的概念，所以必须把惰性求值过程包在一个函数内，以下是调用方法：

```python
from fppy.lazy_evaluate import lazy_val

def f():
    print("f compute")
    return 12

lazy_val.a = f
```

调用结果下：

```python
>>> lazy_val.a
f compute
12
>>> lazy_val.a
12
```

这就表示仅第一次调用时发生了计算。

### 错误处理

### 1. Option

```python
from fppy.option import Just, Nothing

>>> Just(1).map(lambda x: x + 1)
Just(2)
>>> Just(1).flat_map(lambda x: Just(x * 3))
Just(3)
>>> Just(1).get
1
>>> Just(1).get_or_else(2)
1
>>> Just(1).filter(lambda x: x < 0)
Nothing()
>>> Just(1).filter(lambda x: x > 0)
Just(1)
```

与偏函数合用会有很多妙处：

```python
from math import log
from fppy.partail_function import PartialFunction

pf = PartialFunction\
    .case(lambda x: x > 0)\
    .then(lambda x: 1 / x)\
    .case(lambda x: x < 0)\
    .then(lambda x: log(-x))


>>> pf.lift(1)
Just(1)
>>> pf.lift(0)
Nothing()
>>> Just(1).collect(pf)
Just(1)
>>> Just(0).collect(pf)
Nothing

>>> Just(1).collect(pf)
Just(1.)
>>> Just(1).collect(pf).map(lambda x: int(x) - 1)
Just(-1)
>>> Just(1).collect(pf).map(lambda x: int(x) - 1).collect(pf)
Just(0)
>>> Just(1).collect(pf).map(lambda x: int(x) - 1).collect(pf).collect(pf)
Nothing()
>>> Just(1).collect(pf).map(lambda x: int(x) - 1).collect(pf).collect(pf).collect(pf)
Nothing()
>>>Just(1).collect(pf).map(lambda x: int(x) - 1).collect(pf).collect(pf).collect(pf).get_or_else(2)
2

```

### 2. Either

(待完善)


