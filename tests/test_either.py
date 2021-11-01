"""测试
"""
from _pytest.compat import assert_never
import py
import pytest
from fppy.either import Either, Left, Right
from fppy.option import Just

@pytest.mark.either
def test_either_cond():
    assert Either.cond(True, lambda : 1, lambda : "2") == Right(1)
    assert Either.cond(False, lambda: 1, lambda : "2") == Left("2")


@pytest.mark.either
def test_either_unapply():
    assert Right.unapply(Right(1)) == Just(1)
    with pytest.raises(TypeError):
        Right.unapply(Left(1))
    with pytest.raises(TypeError):
        Left.unapply(Right(1)) # require Left
    assert Left.unapply(Left(1)) == Just(1)

@pytest.mark.either
def test_either_exists():
    pass

@pytest.mark.either
def test_either_contain():
    assert Right(1).contain(2) == False
    assert Left(1).contain(2) == False
    assert Right(1).contains(1)
    assert Left(1).contains(1)

@pytest.mark.either
def test_either_filter_or_else():
    assert Right(1).filter_or_else(lambda x: x > 0, 3) == Right(1)
    assert Right(1).filter_or_else(lambda x: x < 0, 3) == Right(1)
    assert Left(1).filter_or_else(lambda x: x > 0, 3) == Right(3)


@pytest.mark.either
def test_either_flat_map():
    assert Right(1).flat_map(lambda x: Right(x + 1)) == Right(2)
    assert Right(1).flat_map(lambda x: Left(x + 1)) == Left(2)
    assert Left(1).flat_map(lambda x: Right(x + 1)) == Left(1)

@pytest.mark.either
def test_either_map():
    assert Right(1).map(str) == Right("1")
    assert Left(1).map(lambda x: x + 1) == Left(1)

@pytest.mark.either
def test_check_right():
    assert not Left(1).is_right
    assert not Right(1).is_left
    assert Left(1).is_left
    assert Right(1).is_right

@pytest.mark.either
def test_check_right():
    assert Right(1).for_each(print) == Right(1)
    assert Left(1).for_each(print) == Left(1)
