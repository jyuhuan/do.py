def do_impl(gen, m, *args, **kwargs):
    boxes = gen(*args, **kwargs)

    def receive(box_content):
        try:
            box = boxes.send(box_content)
        except StopIteration:
            return m.id(None)
        except Return as r:
            return m.id(r.value)
        else:
            return box.flat_map(receive)

    return receive(None)


def do(m):
    def wrapper(f):
        def g(*args, **kwargs):
            return do_impl(f, m, *args, **kwargs)
        return g
    return wrapper


class Return(Exception):
    def __init__(self, value):
        super(Return, self).__init__()
        self.value = value
