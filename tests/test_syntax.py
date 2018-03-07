from unittest import TestCase

from do.monads import MaybeMonad, IterableMonad
from do.syntax import do, Return
from do.exceptions import NoReturnException


class TestDo(TestCase):

    def test_no_return(self):
        """
        Tests a do-routine which does not contain a ``raise Return`` statement.
        Since this is not allowed, an exception is expected.
        """

        @do(MaybeMonad)
        def no_return():
            pass

        self.assertRaises(NoReturnException, lambda: no_return())

    def test_direct_return(self):
        """
        Tests a do-routine which directly returns a value without yielding other
        do-routine.
        """

        @do(MaybeMonad)
        def direct_return(x):
            raise Return(x)

        m = direct_return(5)
        self.assertEqual(m, 5)

    def test_yield_and_return(self):
        """
        Tests a do-routine which yields another do-routine first and then
        returns a value.
        """

        @do(MaybeMonad)
        def f(x):
            raise Return(x + 1)

        @do(MaybeMonad)
        def yield_and_return(x):
            y = yield f(x)
            z = y + 1
            raise Return(z)

        m = yield_and_return(1)

        self.assertEqual(m, 3)
