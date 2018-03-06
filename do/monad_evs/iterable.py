from do.monad_evs import MonadEv


class IterableEv(MonadEv):

    def id(self, value):
        return IterableOfOneItem(value)

    def flat_map(self, xs, f):
        for x in xs:
            ys = f(x)
            for y in ys:
                yield y


class IterableOfOneItem(object):
    def __init__(self, item):
        self.item = item

    def __iter__(self):
        return IteratorOfOneItem(self.item)


class IteratorOfOneItem(object):
    def __init__(self, item):
        self.is_first = True
        self.item = item

    def next(self):
        if self.is_first:
            self.is_first = False
            return self.item
        else:
            raise StopIteration()
