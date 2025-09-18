import pytest
from examples.add import add, subtract, divide


def test_add_success():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract_success():
    assert subtract(5, 3) == 2
    assert subtract(0, 0) == 0


def test_divide_success():
    assert divide(6, 3) == 2
    assert divide(1, 2) == 0.5


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)