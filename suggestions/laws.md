<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
<script type="text/x-mathjax-config"> 
  MathJax.Hub.Config(
    {
      tex2jax: {
        inlineMath: [['$', '$']],
        displayMath: [['$$', '$$']]
        },
      messageStyle: "none" 
    }
  );
</script>

# 一些常用规则

## 数学法则


$(x:) y$表示$x::y$ 

### 数字类

$$x + y = y + x$$
$$x \times y = y \times x$$
$$x + (y + z) = (x + y) + z$$
$$x \times (y \times z) = (x \times y) \times z$$
$$x \times (y + z) = (x \times y) $$

### 函数式优化

$$(map(f).map(g)) xs = (map(f . g)) xs$$
$$f.(g.h) = (f.g).h$$
$$map(f)(xs++ys) = map(f)(xs) ++ map(f)(ys)$$
$$map(f) . concat = concat . map(map(f))$$

#### 幺半群(f, e)

$$foldr(f, e) = foldr(f, e)$$

#### 长度相关

$$len.(x:) = (1+).len$$
$$len. map(f) = len$$
$$len(xs++ys) == len(xs) + len(ys)$$
$$len.concat == sum.map(len)$$
$$sum(map(1+)(xs)) == len(xs) + sum(xs)$$
$$sum(map(n+)(xs)) == len(xs) * n + sum(xs)$$
$$len.segs = (1 + (n*n+n)/2)$$
