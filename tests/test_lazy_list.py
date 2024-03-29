from typing import TypeVar
from fppy.lazy_list import LazyList, Nil
from hypothesis import strategies as st, given
import pytest

@pytest.mark.LazyList
def test_lazy_list_collect():
    assert LazyList([1, 2, 3, 4]).collect() == [1, 2, 3, 4]
    
@pytest.mark.LazyList
def test_lazy_list_map_collect():
    assert (
        LazyList([1, 2, 3, 4])
        .map(lambda x: x + 1)
        .collect()
    ) == [2, 3, 4, 5]
    
@pytest.mark.LazyList
def test_lazy_list_take():
    assert (
        LazyList([1, 2, 3, 4])
        .take(3)
        .collect()
    ) == [1, 2, 3]

    (
        LazyList([1, 2, 3, 4])
        .takewhile(lambda x: x < 4)
        .collect()
    ) == [1, 2, 3]

@pytest.mark.LazyList
def test_lazy_list_find():
    assert (
        LazyList([1, 2, 3, 4])
        .find(lambda x: x > 2)
    ) == 3

    assert (
        LazyList([1, 2, 3, 4])
        .find(lambda x: x > 10)
    ) == Nil()

@pytest.mark.LazyList
def test_lazy_list_reduce():
    assert (
        LazyList([1, 2, 3, 4])
        .reduce(lambda x, y: x + y)
    ) == 10
    assert (
        LazyList([1, 2, 3, 4])
        .foldleft(lambda x, y: x + y, 1)
    ) == 11
    
@pytest.mark.LazyList
def test_lazy_list_len():
    assert (
        LazyList([1, 2, 3, 4])
        .len()
    ) == 4

@pytest.mark.LazyList
def test_lazy_list_scan_left():
    assert (
        LazyList([1, 2, 3, 4])
        .scan_left(lambda x, y: x + str(y), "0")
        .collect()
    ) == ["0", "01", "012", "0123", "01234"]
    assert (
        LazyList([1, 2, 3, 4])
        .scan_left(lambda x, y: x + y, 0)
        .collect()
    ) == [0, 1, 3, 6, 10]

@pytest.mark.LazyList
def test_lazy_list_filter():
    assert (
        LazyList([1, 2, 3, 4])
        .filter(lambda x: x % 2 == 0)
        .collect()
    ) == [2, 4]

@pytest.mark.LazyList
def test_lazy_list_split_head():
    hd, tl = LazyList([1, 2, 3, 4]).split_head()
    assert hd == 1
    assert tl.collect() == [2, 3, 4]

    hd, tl = LazyList([]).split_head()
    assert hd == Nil()

@pytest.mark.LazyList
def test_lazy_list_from():
    assert LazyList.from_iter(1)(lambda x: x + 1).take(4).collect() == [1, 2, 3, 4]


@pytest.mark.LazyList
@given(ls1=st.lists(st.integers()), ls2=st.lists(st.text()))
def test_lazy_list_zip(ls1, ls2):
    assert LazyList([1, 2, 3]).zip_with([2, 3, 4]).collect() == [
        (1, 2),
        (2, 3),
        (3, 4)
    ]
    assert LazyList(ls1).zip_with(LazyList(ls2)).collect() == list(
        zip(ls1, ls2)
    )
    with pytest.raises(TypeError):
        LazyList(ls1).zip_with(1)

@pytest.mark.LazyList
@given(ls1=st.lists(st.integers()), ls2=st.lists(st.integers()))
def test_lazy_list_concat(ls1, ls2):
    assert (LazyList(ls1) + LazyList(ls2)).collect() == ls1 + ls2
    assert (LazyList(ls1) + ls2).collect() == ls1 + ls2
    with pytest.raises(TypeError):
        LazyList(ls1) + 1
   
@pytest.mark.LazyList
def test_lazy_list_for_all():
    assert LazyList([1, 2, 3]).for_all(lambda x: x > 0) == True
    assert LazyList([1, 2, 3]).for_all(lambda x: x == 2) == False

@pytest.mark.LazyList
def test_lazy_list_drop():
    assert LazyList([1, 2, 3]).drop(2).collect() == [3]

@pytest.mark.LazyList
def test_lazy_list_last():
    assert LazyList([1, 2, 3]).last == 3