from functools import reduce
from fppy.cons_list_base import *
from fppy.base import and_then
import pytest

@pytest.mark.cons_base
def test_cons():
    ls = cons(1, cons(1, cons(3, ())))
    assert head(ls) == 1
    assert and_then(tail, tail, tail)(ls) == ()
    assert and_then(tail, head)(ls) == 1

@pytest.mark.cons_base
def test_fold_left_cons_curry():
    ls1 = cons(1, cons(2, cons(3, ())))
    ls2 = cons(1, cons(2, ()))
    ls3 = cons(1, ())
    ls4 = ()
    sum_cons = fold_left_cons_curry(lambda x, y: x + y)(0)
    assert sum_cons(ls4) == 0
    assert sum_cons(ls3) == 1
    assert sum_cons(ls2) == 3
    assert sum_cons(ls1) == 6
    
@pytest.mark.cons_base
def test_map_cons_base():
    ls1 = cons(1, cons(2, cons(3, ())))
    ls2 = cons(1, cons(2, ()))
    ls3 = cons(1, ())
    ls4 = ()
    add1 = map_cons_curry(lambda x: x + 1)
    assert print_cons(add1(ls1)) == "2, 3, 4, nil"
    assert print_cons(add1(ls2)) == "2, 3, nil"
    assert print_cons(add1(ls3)) == "2, nil"
    assert print_cons(add1(ls4)) == "nil"

@pytest.mark.cons_base
def test_filter_cons_base():
    ls1 = cons(1, cons(2, cons(3, ())))
    ls2 = cons(1, cons(2, ()))
    ls3 = cons(1, ())
    ls4 = ()
    filter_even = filter_cons_curry(lambda x: x % 2 == 1)
    assert print_cons(filter_even(ls1)) == "1, 3, nil"
    assert print_cons(filter_even(ls2)) == "1, nil"
    assert print_cons(filter_even(ls3)) == "1, nil"
    assert print_cons(filter_even(ls4)) == "nil"


@pytest.mark.cons_base
def test_collection_cons_base():
    ls = cons(1, cons(2, cons(3, ())))
    assert and_then(
        map_cons_curry(lambda x: x + 1),
        filter_cons_curry(lambda x: x % 2 == 0),
        fold_left_cons_curry(lambda x, y: x + y)(0)
        )(ls) == 6