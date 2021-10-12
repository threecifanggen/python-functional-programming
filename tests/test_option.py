from fppy.errors import NothingHasNoSuchMethod
from fppy.option import Just, Nothing
import pytest

@pytest.mark.option
def test_option_map():
    assert Just(1).map(lambda x: x + 1) == Just(2)

    with pytest.raises(Exception):
        None.map(lambda x: x + 1)

@pytest.mark.option
def test_option_flat_map():
    assert Just(1).flat_map(lambda x: Just(x + 1)) == Just(2)
    assert Just(1).flat_map(lambda _: Nothing()) == Nothing()

    with pytest.raises(TypeError):
        assert Just(1).flat_map(lambda x: x + 1)


@pytest.mark.option
def test_option_get():
    assert Just(1).get == 1
    
    with pytest.raises(NothingHasNoSuchMethod):
        assert Nothing().get

@pytest.mark.option
def test_option_get_or_else():
    assert Just(1).get_or_else(2) == 1
    assert Nothing().get_or_else(2) == 2

@pytest.mark.option
def test_option_collect():
    from fppy.partial_function import PartialFunction
    
    f = PartialFunction\
        .case(lambda x: x > 0)\
        .then(lambda x: x + 1)

    assert Just(1).collect(f) == Just(2)
    assert Nothing().collect(f) == Nothing()

@pytest.mark.option
def test_option_filter():
    assert Just(1).filter(lambda x: x > 0) == Just(1)
    assert Just(1).filter(lambda x: x < -1) == Nothing()
