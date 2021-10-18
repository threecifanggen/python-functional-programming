from fppy.functor import BoxFunction, BoxValue, Box
import pytest
from hypothesis import strategies as st, given

@pytest.mark.functor
@given(x=st.integers())
def test_box(x):
    assert BoxValue.of(1).map(lambda x: x + 1) == BoxValue(2)
    assert BoxFunction(lambda x: x + 1).fmap(1) == BoxValue(2)
    assert BoxFunction(lambda x: x + 1).fmap(x) == BoxValue(x + 1)
    assert BoxValue.of(x).map(lambda x: x + 1) == BoxValue(x + 1)