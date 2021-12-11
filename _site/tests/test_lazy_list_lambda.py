"""测试lazy_list_lambda
"""
import pytest
from hypothesis import strategies as st, given
from fppy.lazy_list_lambda import *
from fppy.base import and_then

@pytest.mark.lazy_list_lambda
def test_lazy_list_lamdba_maker():
    assert collect_lazy_cons(make_lazy_cons(1, 2, 3)) == (1, (2, (3, ())))
    assert collect_lazy_cons(make_lazy_cons(1, 2, 3)) == collect_lazy_cons(
        lazy_cons(
            lambda: 1,
            lazy_cons(
                lambda: 2,
                lazy_cons(
                    lambda: 3,
                    ()
                )
            )
        )
    )

@pytest.mark.lazy_list_lambda
@given(xs=st.lists(st.integers()))
def test_lazy_list_lambda_map(xs):
    assert and_then(
        map_lazy_cons(lambda x: x + 1),
        collect_lazy_cons,
    )(make_lazy_cons(*xs)) == \
        collect_lazy_cons(make_lazy_cons(*[x + 1 for x in xs]))


@pytest.mark.lazy_list_lambda
@given(xs=st.lists(st.integers()))
def test_lazy_list_lambda_filter(xs):
    assert and_then(
        filter_lazy_cons(lambda x: x % 2 == 0),
        collect_lazy_cons,
    )(make_lazy_cons(*xs)) == collect_lazy_cons(
        make_lazy_cons(*[x for x in xs if x % 2 == 0]))


@pytest.mark.lazy_list_lambda
def test_lazy_list_lambda_take_and_iterate():
    assert and_then(
        take_lazy_cons(5),
        collect_lazy_cons
    )(iterate_lazy_cons(1)(lambda x: x + 1)) == collect_lazy_cons(
        make_lazy_cons(1, 2, 3, 4, 5)
    )


@pytest.mark.lazy_list_lambda
def test_lazy_list_lambda_fold_left():
    assert and_then(
        take_lazy_cons(5),
        fold_left_lazy_cons(lambda x, y: x + y)(0)
    )(iterate_lazy_cons(1)(lambda x: x + 1)) == 15
