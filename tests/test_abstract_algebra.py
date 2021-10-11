from fppy.abstract_algebra import (
    Monoid
)
import pytest

@pytest.fixture(scope="module")
def SM():
    class SumMonoid(Monoid):
        def join(self, x, y):
            return x + y

        def unit(self):
            return 0
    return SumMonoid()

@pytest.mark.algebra
def test_sum(SM):
    m_sum = SM.mreduce
    assert m_sum([1, 2, 3]) == 6
    assert m_sum([]) == 0
    assert SM.join(1, 2) == 3
    assert SM.unit() == 0

@pytest.mark.algebra 
def test_thread_reduce_sum(SM):
    m_sum = SM.thread_reduce
    assert m_sum([1, 2, 3]) == 6
    assert m_sum([]) == 0
    
@pytest.mark.algebra
@pytest.mark.skip(reason="cannot pickle abc")
def test_process_reduce_sum(SM):
    m_sum = SM.process_reduce
    assert m_sum([1, 2, 3]) == 6
    assert m_sum([]) == 0

@pytest.mark.algebra
#@pytest.mark.skip(reason="cannot pickle abc")
def test_process_reduce_sum(SM):
    from pathos.threading import ThreadPool
    m_sum = SM.parrellel_reduce(ThreadPool)
    assert m_sum([1, 2, 3]) == 6
    assert m_sum([]) == 0
