import pytest
from bank import value

def test_starts_with_hello():
    assert value("Hello customer") == 0

def test_starts_with_h():
    assert value("Hey customer") == 20

def test_inappropiate_greet():
    assert value("What's up customer") == 100

def test_numbers():
    assert value("57") == 100

def test_empty_greet():
    assert value(" ") == 100