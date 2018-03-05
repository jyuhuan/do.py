from do.exceptions import NoReturnException


def _do_impl(gen, m, *args, **kwargs):

    try:
        boxes = gen(*args, **kwargs)
        if boxes is None:
            raise NoReturnException()
    except Return as r:
        return m.id(r.value)
    else:

        def receive(box_content):
            try:
                box = boxes.send(box_content)
            except StopIteration:
                raise NoReturnException()
            except Return as r:
                return m.id(r.value)
            else:
                return m.flat_map(box, receive)

        return receive(None)


def do(m):
    def wrapper(f):
        def g(*args, **kwargs):
            return _do_impl(f, m(), *args, **kwargs)
        return g
    return wrapper


class Return(Exception):
    def __init__(self, value):
        super(Return, self).__init__()
        self.value = value
