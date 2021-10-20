from fppy.cons_list import Empty, Cons
import pytest
from hypothesis import strategies as st, given

@pytest.fixture(scope="session")
def cons_list_1():
    return Cons.maker(1, 2, 3, 4)

@pytest.mark.cons_list
def test_cons_maker():
    assert Cons.maker(1, 2, 3) == Cons(1, Cons(2, Cons(3, Empty())))
    assert Cons.maker() == Empty()

@pytest.mark.cons_list
@given(cons_list_given=st.lists(st.integers()))
def test_cons_map(cons_list_given):
    assert Cons\
        .maker(*cons_list_given)\
        .map(lambda x: x + 1) == Cons.maker(
           *[i + 1 for i in cons_list_given]
        )

@pytest.mark.cons_list
@given(cons_list_given=st.lists(st.integers()))
def test_cons_filter(cons_list_given):
    assert Cons\
        .maker(*cons_list_given)\
        .filter(lambda x: x % 2 == 0) == Cons.maker(
           *[i for i in cons_list_given if i % 2 == 0]
        )

@pytest.mark.cons_list
@given(cons_list_given=st.lists(st.integers()))
def test_cons_fold_left(cons_list_given):
    assert Cons\
        .maker(*cons_list_given)\
        .fold_left(lambda x, y: x + y, 0) == sum(cons_list_given)
    
    assert Cons\
        .maker(*cons_list_given)\
        .fold_left(lambda x, y: x + str(y), "") == "".join([str(i) for i in cons_list_given])