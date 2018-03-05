from unittest import TestCase

from do.monads.maybe import Just
from do.monad_evs.maybe_ev import MaybeEv
from do.syntax import do, Return
from do.exceptions import NoReturnException


class TestDo(TestCase):

    def test_no_return(self):
        """
        Tests a do-routine which does not contain a ``raise Return`` statement.
        Since this is not allowed, an exception is expected.
        """

        @do(MaybeEv)
        def no_return():
            pass

        self.assertRaises(NoReturnException, lambda: no_return())

    def test_direct_return(self):
        """
        Tests a do-routine which directly returns a value without yielding other
        do-routine.
        """
        @do(MaybeEv)
        def direct_return(x):
            raise Return(x)

        m = direct_return(5)
        self.assertIsInstance(m, Just)
        self.assertEqual(m.get(), 5)

    def test_yield_and_return(self):
        """
        Tests a do-routine which yields another do-routine first and then
        returns a value.
        """

        @do(MaybeEv)
        def f(x):
            raise Return(x + 1)

        @do(MaybeEv)
        def yield_and_return(x):
            y = yield f(x)
            z = y + 1
            raise Return(z)

        m = yield_and_return(1)

        self.assertIsInstance(m, Just)
        self.assertEquals(m.get(), 3)
