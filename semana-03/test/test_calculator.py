import pytest
from calculator import square

def test_positive():
    assert square(2) == 4
    assert square(3) == 9

def test_negative():
    assert square(-2) == 4
    assert square(-3) == 9

def test_zero():
    assert square(0) == 0

def test_str():
    with pytest.raises(TypeError): # --> con la library de pytest se usa el .raises para indicar que si cierto error aparece, y luego se indica como proceder ante el error
        square("cat")
