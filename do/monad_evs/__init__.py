class MonadEv(object):

    def id(self, value):
        raise NotImplementedError()

    def flat_map(self, monad, f):
        raise NotImplementedError()
