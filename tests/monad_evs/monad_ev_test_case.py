from unittest import TestCase


class MonadEvTestCase(TestCase):
    """
    Any Monad evidence class will have to be tested using this base test.
    """

    def test_id(self): pass

    def test_flat_map(self): pass

    def test_usage_with_do(self): pass
