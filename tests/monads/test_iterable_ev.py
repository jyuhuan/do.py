from collections import Iterable

from tests.monads.monad_test_case import MonadTestCase

from do.monads import IterableMonad
from do.syntax import do, Return


class TestIterable(MonadTestCase):

    def test_id(self):
        xs = IterableMonad.id(5)

        self.assertIsInstance(xs, Iterable)
        l = list(xs)
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0], 5)

    def test_flat_map(self):
        xs = IterableMonad.flat_map(['abc', 'def'], lambda s: list(s))

        self.assertIsInstance(xs, Iterable)

        xs_list = list(xs)
        self.assertEqual(len(xs_list), 6)
        self.assertEqual(xs_list[0], 'a')
        self.assertEqual(xs_list[1], 'b')
        self.assertEqual(xs_list[2], 'c')
        self.assertEqual(xs_list[3], 'd')
        self.assertEqual(xs_list[4], 'e')
        self.assertEqual(xs_list[5], 'f')

    def test_usage_with_do(self):

        @do(IterableMonad)
        def example_usage():
            x = yield ['abc', 'def']
            y = yield list(x)
            raise Return(y)

        xs = example_usage()
        xs_list = list(xs)

        self.assertEqual(len(xs_list), 6)
        self.assertEqual(len(xs_list), 6)
        self.assertEqual(xs_list[0], 'a')
        self.assertEqual(xs_list[1], 'b')
        self.assertEqual(xs_list[2], 'c')
        self.assertEqual(xs_list[3], 'd')
        self.assertEqual(xs_list[4], 'e')
        self.assertEqual(xs_list[5], 'f')
