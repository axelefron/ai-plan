from hola import hello

def test_default():
    assert hello() == "hello, world"

def test_argument():
    for name in ["Axel", "Sol"]:
        assert hello(name) == f"hello, {name}"