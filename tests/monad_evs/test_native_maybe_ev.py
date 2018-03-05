from unittest import TestCase
from do.monad_evs.native_maybe_ev import NativeMaybeEv
from do.syntax import do, Return


class TestNativeMaybe(TestCase):

    def test_id(self):
        ev = NativeMaybeEv()
        x = ev.id('hello')
        self.assertIsInstance(x, str)
        self.assertEquals(x, 'hello')

    def test_flat_map(self):
        ev = NativeMaybeEv()

        x = ev.flat_map('hello', lambda s: len(s))
        self.assertIsInstance(x, int)
        self.assertEquals(x, 5)

        y = ev.flat_map(None, lambda s: len(s))
        self.assertEquals(y, None)

    def test_using_native_maybe_in_do(self):

        @do(NativeMaybeEv)
        def use_native_maybe_1():
            a = yield 5
            b = yield 4
            raise Return(a + b)

        c = use_native_maybe_1()
        self.assertEquals(c, 9)

        @do(NativeMaybeEv)
        def use_native_maybe_2():
            a = yield 5
            b = yield None
            raise Return(a + b)

        c = use_native_maybe_2()
        self.assertEquals(c, None)
