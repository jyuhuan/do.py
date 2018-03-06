from do.monads import MaybeMonad
from do.syntax import do, Return
from tests.monads.monad_test_case import MonadTestCase


class TestMaybe(MonadTestCase):

    def test_id(self):
        x = MaybeMonad.id('hello')
        self.assertIsInstance(x, str)
        self.assertEquals(x, 'hello')

    def test_flat_map(self):
        x = MaybeMonad.flat_map('hello', lambda s: len(s))
        self.assertIsInstance(x, int)
        self.assertEquals(x, 5)

        y = MaybeMonad.flat_map(None, lambda s: len(s))
        self.assertEquals(y, None)

    def test_usage_with_do(self):

        @do(MaybeMonad)
        def use_native_maybe_1():
            a = yield 5
            b = yield 4
            raise Return(a + b)

        c = use_native_maybe_1()
        self.assertEquals(c, 9)

        @do(MaybeMonad)
        def use_native_maybe_2():
            a = yield 5
            b = yield None
            raise Return(a + b)

        c = use_native_maybe_2()
        self.assertEquals(c, None)
