from abc import *


class Monad(object):
    """
    A monad that facilitates the `do` syntactic sugar.
    """

    @abstractmethod
    def id(self, x):
        raise NotImplementedError()

    @abstractmethod
    def flat_map(self, mx, f):
        raise NotImplementedError()


class MaybeMonad(Monad):

    def id(self, x):
        return x

    def flat_map(self, mx, f):
        return None if mx is None else f(mx)


class IterableMonad(Monad):

    def id(self, x):
        return [x]

    def flat_map(self, mx, f):
        for x in mx:
            for y in f(x):
                yield y
