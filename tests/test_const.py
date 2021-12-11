'''
Author: huangbaochen<huangbaochenwo@live.com>
Date: 2021-12-11 15:00:47
LastEditTime: 2021-12-11 21:40:11
LastEditors: huangbaochen<huangbaochenwo@live.com>
Description: 常量测试
No MERCY
'''
import pytest
from fppy.const import Const
from fppy.errors import ConstError


@pytest.mark.const
def test_const():
    """测试常量
    """
    c = Const()
    c.a = 1
    assert c.a == 1

    with pytest.raises(ConstError):
        c.b = 1
        c.b = 2
