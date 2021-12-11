from fppy.lazy_evaluate import lazy_val, lazy_property
from fppy.errors import NotVoidFunctionError
from dataclasses import dataclass
import pytest

@pytest.mark.lazy
def test_lazy_property(capfd):

    @dataclass
    class Circle:
        x: float
        y: float
        r: float

        @lazy_property
        def area(self):
            print("area compute")
            return self.r ** 2 * 3.14

    cir = Circle(0, 0, 1)
    cir.area
    stout1, _ = capfd.readouterr()
    assert stout1 == "area compute\n"
    cir.area
    stout2, _ = capfd.readouterr()
    assert stout2 == ""

@pytest.mark.lazy
def test_lazy_val(capfd):
    def f():
        print("f compute")
        return 1

    lazy_val.f = f
    stout1, _ = capfd.readouterr()
    assert stout1 == ""
    lazy_val.f
    stout2, _ = capfd.readouterr()
    assert stout2 == "f compute\n"
    lazy_val.f
    stout3, _ = capfd.readouterr()
    assert stout3 == ""

@pytest.mark.lazy
def test_lazy_val_not_valid_function():
    with pytest.raises(NotVoidFunctionError):
        lazy_val.g = 1
    
    def g(x):
        return x + 1
    with pytest.raises(NotVoidFunctionError):
        lazy_val.g = g
    
