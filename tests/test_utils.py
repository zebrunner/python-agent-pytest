from pytest_zebrunner.utils import Singleton


def test_sigleton() -> None:
    class TestClass(metaclass=Singleton):
        pass

    obj1 = TestClass()
    obj2 = TestClass()

    assert obj1 is obj1._Singleton__instance  # type: ignore
    assert obj1 is obj1._Singleton__instance  # type: ignore
    assert obj1 is obj2


def test_singleton_kwargs() -> None:
    class TestClass(metaclass=Singleton):
        def __init__(self, arg1: str, arg2: str):
            self.arg1 = arg1
            self.arg2 = arg2

    obj = TestClass(arg1="arg1", arg2="arg2")
    assert obj.arg1 == "arg1"
    assert obj.arg2 == "arg2"


def test_singleton_args() -> None:
    class TestClass(metaclass=Singleton):
        def __init__(self, arg1: str, arg2: str):
            self.arg1 = arg1
            self.arg2 = arg2

    obj = TestClass("arg1", "arg2")
    assert obj.arg1 == "arg1"
    assert obj.arg2 == "arg2"
