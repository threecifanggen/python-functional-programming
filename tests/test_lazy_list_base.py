"""测试从头实现的惰性列表
"""
import pytest
from hypothesis import strategies as st, given
from fppy.lazy_list_base import LazyCons, LazyEmpty


@pytest.mark.lazy_list_base
def test_lazy_list_base_maker():
    assert LazyCons(1, LazyCons(2, LazyCons(3, LazyEmpty()))).collect() == \
        LazyCons.maker(1, 2, 3).collect()


@pytest.mark.lazy_list_base
def test_lazy_list_base_from_iter():
    assert LazyCons.from_iter(1)(lambda x: x + 1).take(3).collect() == \
        LazyCons.maker(1, 2, 3).collect()
    assert LazyCons.from_iter(1)(lambda x: x + 1)\
        .filter(lambda x: x % 2 == 0)\
        .take(3)\
        .collect() ==\
        LazyCons.maker(2, 4, 6).collect()


@pytest.mark.lazy_list_base
@given(ll=st.lists(st.integers()))
def test_lazy_list_base_map(ll):
    assert LazyCons.maker(*ll).map(lambda x: x + 1).collect() == \
        LazyCons.maker(*[i + 1 for i in ll]).collect()


@pytest.mark.lazy_list_base
@given(ll=st.lists(st.integers()))
def test_lazy_list_base_filter(ll):
    assert LazyCons.maker(*ll).filter(lambda x: x % 2 == 0).collect() == \
        LazyCons.maker(*[i for i in ll if i % 2 == 0]).collect()
