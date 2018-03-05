from do.monad_evs import MonadEv
from do.monads.maybe import Maybe, Nothing, Just


class MaybeEv(MonadEv):

    def id(self, value):
        return Just(value)

    def flat_map(self, maybe, f):
        return maybe.flat_map(f)
