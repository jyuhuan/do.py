from do.monad_evs import MonadEv


class NativeMaybeEv(MonadEv):
    def id(self, value):
        return value

    def flat_map(self, optional, f):
        return f(optional) if optional is not None else None
