from fppy.abstract_algebra import (
    Monoid
)
import pytest

@pytest.fixture(scope="module")
def SM():
    class SumMonoid(Monoid):
        @staticmethod
        def join(x, y):
            return x + y

        @staticmethod
        def unit():
            return 0
    return SumMonoid

def test_sum(SM):
    m_sum = SM.mreduce(SM)
    assert m_sum([1, 2, 3]) == 6
    assert m_sum([]) == 0
    assert SM.join(1, 2) == 3
    assert SM.unit() == 0
    
def test_thread_reduce_sum(SM):
    m_sum = SM.thread_reduce(SM)
    assert m_sum([1, 2, 3]) == 6
    assert m_sum([]) == 0
    
@pytest.mark.skip(reason="cannot pickle abc")
def test_process_reduce_sum(SM):
    m_sum = SM.process_reduce(SM)
    assert m_sum([1, 2, 3]) == 6
    assert m_sum([]) == 0