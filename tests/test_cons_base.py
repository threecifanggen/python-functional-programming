from fppy.cons_list_base import *
from fppy.base import and_then
import pytest

@pytest.fixture(scope="session")
def ls1():
    return cons(1, cons(2, cons(3, ())))


@pytest.fixture(scope="session")
def ls2():
    return cons(1, cons(2, ()))


@pytest.fixture(scope="session")
def ls3():
    return cons(1, ())


@pytest.fixture(scope="session")
def ls4():
    return ()

@pytest.mark.cons_base
def test_cons_equal(ls1, ls2, ls3, ls4):
    assert equal_cons(
        cons_apply(1, 2, 3),
        ls1
    )
    assert not equal_cons(
        cons_apply(1, 2, 3),
        ls2
    )
    assert not equal_cons(
        cons_apply(1, 2, 3),
        ls4
    )
    assert equal_cons(
        cons_apply(1),
        ls3
    )


@pytest.mark.cons_base
def test_cons_apply(ls1, ls2, ls3, ls4):
    assert print_cons(cons_apply(1, 2, 3)) == print_cons(ls1)
    assert print_cons(cons_apply(1, 2)) == print_cons(ls2)
    assert print_cons(cons_apply(1)) == print_cons(ls3)
    assert print_cons(cons_apply()) == print_cons(ls4)
    assert print_cons(cons_apply(1, 2, 3, 4)) == ", ".join(list("1234")) + ", nil"


@pytest.mark.cons_base
def test_cons(ls1):
    assert head(ls1) == 1
    assert and_then(tail, tail, tail)(ls1) == ()
    assert and_then(tail, head)(ls1) == 2

@pytest.mark.cons_base
def test_fold_left_cons_curry(ls1, ls2, ls3, ls4):
    sum_cons = fold_left_cons_curry(lambda x, y: x + y)(0)
    assert sum_cons(ls4) == 0
    assert sum_cons(ls3) == 1
    assert sum_cons(ls2) == 3
    assert sum_cons(ls1) == 6
    
@pytest.mark.cons_base
def test_map_cons_base(ls1, ls2, ls3, ls4):
    add1 = map_cons_curry(lambda x: x + 1)
    assert print_cons(add1(ls1)) == "2, 3, 4, nil"
    assert print_cons(add1(ls2)) == "2, 3, nil"
    assert print_cons(add1(ls3)) == "2, nil"
    assert print_cons(add1(ls4)) == "nil"

@pytest.mark.cons_base
def test_filter_cons_base(ls1, ls2, ls3, ls4):
    filter_even = filter_cons_curry(lambda x: x % 2 == 1)
    assert print_cons(filter_even(ls1)) == "1, 3, nil"
    assert print_cons(filter_even(ls2)) == "1, nil"
    assert print_cons(filter_even(ls3)) == "1, nil"
    assert print_cons(filter_even(ls4)) == "nil"


@pytest.mark.cons_base
def test_collection_cons_base(ls1):
    assert and_then(
        map_cons_curry(lambda x: x + 1),
        filter_cons_curry(lambda x: x % 2 == 0),
        fold_left_cons_curry(lambda x, y: x + y)(0)
        )(ls1) == 6
