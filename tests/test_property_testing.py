from fppy.property_based_testing_tools import (
    int_generator,
    str_generator
)
import pytest

@pytest.mark.property
def test_int_generator():
    def add(x, y): return x + y
    # add(x, y) == add(y, x)
    # add(x, -y) == -add(-x, y)
    # add(x - 1, y) == add(x, y - 1) == add(x, y) - 1

    for i, j in zip(int_generator(), int_generator()):
        assert add(i, j) == add(j, i)
        assert add(i, -j) == -add(-i, j)
        assert add(i - 1, j) == add(i, j - 1) == add(i, j) - 1

@pytest.mark.property
def test_str_generator():
    def join_and_reverse(x, y): return (x + y)[::-1]
    # join_and_reverse(x, y) == join_and_reverse(y[::-1], x[::-1])[::-1]
    # join_and_reverse(x, y)[0] == y[-1] if len(y) > 0
    # join_and_reverse(x, y)[-1] == x[0] if len(x) > 0

    for x, y in zip(str_generator(), str_generator()):
        assert join_and_reverse(x, y) == join_and_reverse(y[::-1], x[::-1])[::-1]
        assert join_and_reverse(x, y)[0] == y[-1] if len(y) > 0 else True
        assert join_and_reverse(x, y)[-1] == x[0] if len(x) > 0 else True