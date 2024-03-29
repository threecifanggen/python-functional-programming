'''
Author: huangbaochen<huangbaochenwo@live.com>
Date: 2021-12-11 20:04:19
LastEditTime: 2021-12-11 21:46:16
LastEditors: huangbaochen<huangbaochenwo@live.com>
Description: 测试Try单子
No MERCY
'''
import pytest
from fppy.try_monad import Try, Success, Fail
from fppy.option import Just, Nothing

@pytest.mark.try_monad
def test_try_apply():
    assert Try.apply(1) == Success(1)
    assert Try(1) == Success(1)

@pytest.mark.try_monad
def test_try_unapply():
    assert Success.unapply(Success(1)) == Just(1)
    assert Fail.unapply(Fail(TypeError(), 1)) == Nothing()

    with pytest.raises(TypeError):
        Fail.unapply(1)

    with pytest.raises(TypeError):
        Fail.unapply(Success(1))

    with pytest.raises(TypeError):
        Success.unapply(1)

    with pytest.raises(TypeError):
        Success.unapply(Fail(Exception(), 1))

def test_try_monad_map():
    assert Success(1).map(lambda x: x + 1) == Success(2)
    assert Success(1).map(lambda x: x / 0) ==\
        Fail(ZeroDivisionError('division by zero'), 1)
    assert Fail(ZeroDivisionError('division by zero'),  1)\
        .map(lambda x: x + 1) ==\
        Fail(ZeroDivisionError('division by zero'),  1)

@pytest.mark.try_monad
def test_try_monad_flat_map():
    assert Success(1).flat_map(lambda x: Success(2)) == Success(2)
    assert Fail(ZeroDivisionError('division by zero'), 1)\
        .flat_map(lambda x: Success(1)) ==\
        Fail(ZeroDivisionError('division by zero'), 1)

    with pytest.raises(TypeError):
        Success(1).flat_map(lambda x: x + 1)

@pytest.mark.try_monad
def test_try_monad_eq():
    assert Fail(ZeroDivisionError('division by zero'), 1) ==\
        Fail(ZeroDivisionError('division by zero'), 1)

    assert Fail(ZeroDivisionError('division by'), 1) !=\
        Fail(ZeroDivisionError('division by zero'), 1)

    assert Fail(ZeroDivisionError('division by zero'), 0) !=\
        Fail(ZeroDivisionError('division by zero'), 1)

@pytest.mark.try_monad
def test_try_monad_get():
    assert Fail(ZeroDivisionError('division by zero'), 1)\
        .get().args ==\
        ZeroDivisionError('division by zero').args

    assert Success(1).get() == 1

    # pylint: disable=no-member
    assert Try("s").get() == "s"

@pytest.mark.try_monad
def test_try_monad_get_or_else():
    assert Fail(ZeroDivisionError('division by zero'),  1)\
        .get_or_else(2) == 2

    assert Success(1).get_or_else(2) == 1

@pytest.mark.try_monad
def test_try_monad_get_error_input():
    assert Fail(ZeroDivisionError('division by zero'),  1)\
        .get_error_input() == 1
