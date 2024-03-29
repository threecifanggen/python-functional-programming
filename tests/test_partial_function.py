from fppy.partial_function import PartialFunction
from fppy.errors import NoOtherCaseError
import pytest


@pytest.mark.PartialFunction
def test_partial_function_init():
    (
        PartialFunction
        .case(lambda x: x > 1)
        .then(lambda x: x + 1)
    )
    
@pytest.mark.PartialFunction
def test_partial_function_apply():
    f = (
        PartialFunction
        .case(lambda x: x > 1)
        .then(lambda x: x + 1)
    )
    assert f.apply(2) == 3
    assert f(2) == 3

    with pytest.raises(NoOtherCaseError):
        f.apply(1)

@pytest.mark.PartialFunction
def test_partial_function_or_else():
    """测试偏函数的or_else功能
    """
    f = (
        PartialFunction
        .case(lambda x: x > 1)
        .then(lambda x: x + 1)
    )
    g = (
        PartialFunction
        .case(lambda x: x > -1)
        .then(lambda x: x + 2)
    )
    assert f.or_else(g).apply(1) == 3
    assert f.or_else(g).apply(2) == 3
    with pytest.raises(NoOtherCaseError):
        f.or_else(g).apply(-1)

@pytest.mark.PartialFunction
def test_partial_function_is_defined_at():
    """测试偏函数的is_defined_at功能
    """
    f = (
        PartialFunction
        .case(lambda x: x > 1)
        .then(lambda x: x + 1)
        .case(lambda x: x > 0)
        .then(lambda x: x * 2)
    )
    assert f.is_defined_at(1) == True
    assert f.is_defined_at(-1) == False


@pytest.mark.PartialFunction
def test_partial_function_lift():
    from fppy.option import Nothing, Just
    f = (
        PartialFunction
        .case(lambda x: x > 1)
        .then(lambda x: x + 1)
        .case(lambda x: x > 0)
        .then(lambda x: x * 2)
    )
    assert f.lift(1) == Just(2)
    assert f.lift(0) == Nothing