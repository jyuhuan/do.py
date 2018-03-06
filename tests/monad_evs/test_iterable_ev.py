from collections import Iterable

from tests.monad_evs.monad_ev_test_case import MonadEvTestCase

from do.monad_evs import IterableEv
from do.syntax import do, Return


class TestIterableEv(MonadEvTestCase):

    def test_id(self):
        ev = IterableEv()
        xs = ev.id(5)

        self.assertIsInstance(xs, Iterable)
        self.assertEquals(len(list(xs)), 1)
        self.assertEquals(list(xs)[0], 5)

    def test_flat_map(self):
        ev = IterableEv()
        xs = ev.flat_map(['abc', 'def'], lambda s: list(s))

        self.assertIsInstance(xs, Iterable)

        xs_list = list(xs)
        self.assertEquals(len(xs_list), 6)
        self.assertEquals(xs_list[0], 'a')
        self.assertEquals(xs_list[1], 'b')
        self.assertEquals(xs_list[2], 'c')
        self.assertEquals(xs_list[3], 'd')
        self.assertEquals(xs_list[4], 'e')
        self.assertEquals(xs_list[5], 'f')

    def test_usage_with_do(self):

        class SomeIterable(object):
            def __iter__(self):
                return ['abc', 'def'].__iter__()

        @do(IterableEv)
        def example_usage():
            x = yield SomeIterable()
            y = yield list(x)
            raise Return(y)

        xs = example_usage()
        xs_list = list(xs)

        self.assertEquals(len(xs_list), 6)
        self.assertEquals(len(xs_list), 6)
        self.assertEquals(xs_list[0], 'a')
        self.assertEquals(xs_list[1], 'b')
        self.assertEquals(xs_list[2], 'c')
        self.assertEquals(xs_list[3], 'd')
        self.assertEquals(xs_list[4], 'e')
        self.assertEquals(xs_list[5], 'f')
