"""测试常量
"""
import pytest
from fppy import const
from fppy.errors import ConstError


@pytest.mark.const
def test_const():
    """测试常量
    """
    const.a = 1
    assert const.a == 1

    with pytest.raises(ConstError):
        const.b = 1
        const.b = 2
