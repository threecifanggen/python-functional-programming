"""测试组合子
"""
import pytest
from fppy.combinator import Y, Z

@pytest.mark.combinator
def test_Y_combinator():
    """测试Y组合子
    """
    power_of_2 = Y(lambda f: lambda x: 1 if (x == 0) else 2 * f(x - 1))
    assert power_of_2(3) == 8
    assert power_of_2(1) == 2

@pytest.mark.combinator
def test_Z_combinator():
    """测试Z组合子
    """
    power = Z(lambda f: lambda x, n: 1 if (n == 0) else x * f(x, n - 1))
    assert power(2, 3) == 8
    assert power(2, 1) == 2
