class Monad(object):

    @classmethod
    def id(cls, value):
        raise NotImplementedError()

    def flat_map(self, f):
        raise NotImplementedError()


class Maybe(Monad):

    def get(self):
        raise NotImplementedError()

    @classmethod
    def id(cls, value):
        return Just(value)

    def flat_map(self, f):
        if isinstance(self, Nothing):
            return self
        else:
            return f(self.get())


class Just(Maybe):
    def __init__(self, value):
        self._value = value

    def get(self):
        return self._value

    def __repr__(self):
        return 'Just({})'.format(self._value)


class Nothing(Maybe):
    def get(self):
        raise Exception("Cannot call get on Nothing!")

    def __repr__(self):
        return 'Nothing'
