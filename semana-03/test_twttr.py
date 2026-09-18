import pytest
from twttr import shorten

def test_str():
    assert shorten('Murcielago') == "Mrclg"
        
def test_numbers():
    assert shorten("CS50 is great") == "CS50 s grt"

def test_lowercase():
    assert shorten('restaurante') == "rstrnt"

def test_randomcases():
    assert shorten('MuRcIElaGO') == "MRclG"

def test_punctuations():
    assert shorten('Google.com is fascinating!') == 'Ggl.cm s fscntng!'
