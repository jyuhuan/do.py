from unittest import TestCase


class MonadTestCase(TestCase):
    """
    Any Monad typeclass will have to be tested using this base test.
    """

    def test_id(self): pass

    def test_flat_map(self): pass

    def test_usage_with_do(self): pass
