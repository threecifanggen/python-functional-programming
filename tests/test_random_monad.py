"""测试所有无副作用的Monad
"""
from hypothesis import (
    strategies as st,
    given
)
import pytest
from fppy.random_monad import (
    random_float_generator,
    random_ascii_generator,
    random_ascii_generator_2,
    random_float_generator_2,
    random_int_generator,
    random_val
)
from fppy.lazy_list import LazyList


@pytest.mark.random
@given(i=st.integers().filter(lambda x: 0 <= x <= 65535))
def test_randown_generator(i):
    take_n_list = lambda x, n: LazyList(x).take(n).collect()
    assert take_n_list(random_ascii_generator_2(i), 10) ==\
        take_n_list(random_ascii_generator(i), 10) == \
        take_n_list(random_val(i, "ascii"), 10)
    assert take_n_list(random_float_generator_2(i), 10) ==\
        take_n_list(random_float_generator(i), 10) == \
        take_n_list(random_val(i, "float"), 10)
    assert  take_n_list(random_int_generator(i), 10)== \
        take_n_list(random_val(i, "int"), 10)
