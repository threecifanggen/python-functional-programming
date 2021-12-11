"""抽象代数测试
"""
import pytest
from pathos.threading import ThreadPool
from fppy.abstract_algebra import (
    Monoid,
    SemiGroup
)

@pytest.fixture(scope="module")
def SM():
    """新建测试类
    """
    class SumMonoid(Monoid):
        """求和幺半群
        """
        def join(self, x, y):
            return x + y

        @property
        def unit(self):
            return 0

    return SumMonoid()

@pytest.mark.algebra
def test_sum(SM):
    """测试求和
    """
    m_sum = SM.mreduce
    assert m_sum([1, 2, 3]) == 6
    assert m_sum([]) == 0
    assert SM.join(1, 2) == 3
    assert SM.unit == 0

@pytest.mark.algebra
def test_thread_reduce_sum(SM):
    """测试线程reduce
    """
    m_sum = SM.thread_reduce
    assert m_sum([1, 2, 3]) == 6
    assert m_sum([]) == 0

@pytest.mark.algebra
# @pytest.mark.skip(reason="cannot pickle abc")
def test_process_reduce_sum(SM):
    """测试进程reduce

    TODO: Pickle失败，需要完善
    """
    with pytest.raises(Exception):
        m_sum = SM.process_reduce
        assert m_sum([1, 2, 3]) == 6
        assert m_sum([]) == 0

@pytest.mark.algebra
#@pytest.mark.skip(reason="cannot pickle abc")
def test_parrellel_reduce_sum(SM):
    """测试并行的reduce
    """
    m_sum = SM.parrellel_reduce(ThreadPool)
    assert m_sum([1, 2, 3]) == 6
    assert m_sum([]) == 0

@pytest.mark.algebra
def test_semi_group():
    """测试半群
    """
    class AddSemiGroup(SemiGroup):
        """加法半群
        """
        def join(self, x, y):
            return x + y

    add = AddSemiGroup()
    assert add.join(1, 2) == 3
