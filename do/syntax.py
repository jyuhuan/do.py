from do.exceptions import NoReturnException


def do(m):
    def wrapper(f):
        def g(*args, **kwargs):
            return _do_impl(f, m(), *args, **kwargs)
        return g
    return wrapper


def _do_impl(gen, m, *args, **kwargs):
    """Runs the generator of monads.

    This method takes into consideration the fact that the ``flat_map(m, f)``
    method of some monads may use invoke the ``f`` argument multiple times (for
    example, the list monad).

    Ported from the ``Do.Multi`` of Fantasy Do [1].

    [1] https://github.com/russellmcc/fantasydo
    """
    try:
        boxes = gen(*args, **kwargs)
        if boxes is None:
            raise NoReturnException()
    except Return as r:
        return m.id(r.value)
    else:
        def receive(box_content, state):
            boxes = gen(*args, **kwargs)
            for it in state:
                boxes.send(it)
            try:
                box = boxes.send(box_content)
            except StopIteration:
                raise NoReturnException()
            except Return as r:
                return m.id(r.value)
            else:
                return m.flat_map(box, lambda x: receive(x, state + [box_content]))

        return receive(None, [])


class Return(Exception):
    def __init__(self, value):
        super(Return, self).__init__()
        self.value = value
