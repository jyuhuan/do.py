from abc import *


class Monad(object):
    """
    A monad that facilitates the `do` syntactic sugar.
    """

    def __new__(cls, *args, **kwargs):
        raise AssertionError("A monad instance cannot be instantiated.")

    @staticmethod
    @abstractmethod
    def id(x):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def flat_map(mx, f):
        raise NotImplementedError()


class MaybeMonad(Monad):

    @staticmethod
    def id(x):
        return x

    @staticmethod
    def flat_map(mx, f):
        return None if mx is None else f(mx)


class IterableMonad(Monad):

    @staticmethod
    def id(x):
        yield x

    @staticmethod
    def flat_map(mx, f):
        for x in mx:
            for y in f(x):
                yield y
