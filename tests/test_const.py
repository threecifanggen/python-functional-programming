from fppy import const
from fppy.errors import ConstError
import pytest

@pytest.mark.const
def test_const():
    const.a = 1
    assert const.a == 1

    with pytest.raises(ConstError):
        const.b = 1
        const.b = 2