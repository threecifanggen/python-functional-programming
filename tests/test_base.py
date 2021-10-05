from fppy.base import F_, compose, and_then
import pytest

@pytest.mark.Function
def test_function_attribute():
    """测试函数属性
    """
    @F_
    def f(x):
        return x + 1
    
    assert f.name == 'f'

    g = F_(lambda x: x * 2)
    
    assert g.name == '<lambda>'

@pytest.mark.Function
def test_apply():
    """测试函数应用
    """
    @F_
    def f(x):
        return x + 1
    
    assert f(1) == 2
    assert f.apply(1) == 2
    
@pytest.mark.Function
def test_function_and_then():
    """测试and_then函数
    """
    f = F_(lambda x: x + 1)
    assert f.and_then(lambda x: x * 2)(2) == 6

@pytest.mark.Function
def test_function_compose():
    """测试compose
    """
    f = F_(lambda x: x + 1)
    assert f.compose(lambda x: x * 2)(2) == 5

@pytest.mark.Function
def test_function_map():
    """测试map
    """
    f = F_(lambda x: x + 1)
    assert f.map([1, 2, 3]) == [2, 3, 4]
    assert f.map([1, 2, 3], True) != [2, 3, 4]
    assert list(f.map([1, 2, 3], True)) == [2, 3, 4]

def test_compose_and_then():
    f = lambda x: x + 1
    g = lambda x: x * 2
    h = lambda x: x ** 3
    
    assert compose(f, g, h)(1) == 3
    assert and_then(f, g, h)(1) == 64