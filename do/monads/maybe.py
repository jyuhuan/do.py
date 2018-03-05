class Maybe(object):

    def get(self):
        raise NotImplementedError()

    def flat_map(self, f):
        return self if isinstance(self, Nothing) else f(self.get())


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
